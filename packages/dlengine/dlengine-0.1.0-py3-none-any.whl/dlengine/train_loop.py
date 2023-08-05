# encoding: utf-8
"""
credit:
https://github.com/facebookresearch/detectron2/blob/master/detectron2/engine/train_loop.py
"""

import logging
import time
import weakref

import numpy as np
import torch
from torch.nn.parallel import DistributedDataParallel
from typing import Dict
from . import comm
from .utils.events import EventStorage, get_event_storage


__all__ = ["HookBase", "TrainerBase", "SimpleTrainer"]


class HookBase:
    """
    Base class for hooks that can be registered with :class:`TrainerBase`.
    Each hook can implement 6 methods. The way they are called is demonstrated
    in the following snippet:
    .. code-block:: python
        hook.before_train()
        for epoch in range(start_epoch, end_epoch):
            hook.before_epoch()
            for i in range(steps_per_epoch):
                hook.before_step()
                trainer.run_step()
                hook.after_step()
            hook.after_epoch()
        hook.after_train()
    Notes:
        1. In the hook method, users can access `self.trainer` to access more
           properties about the context (e.g., current iteration).
        2. A hook that does something in :meth:`before_step` can often be
           implemented equivalently in :meth:`after_step`.
           If the hook takes non-trivial time, it is strongly recommended to
           implement the hook in :meth:`after_step` instead of :meth:`before_step`.
           The convention is that :meth:`before_step` should only take negligible time.
           Following this convention will allow hooks that do care about the difference
           between :meth:`before_step` and :meth:`after_step` (e.g., timer) to
           function properly.
    Attributes:
        trainer: A weak reference to the trainer object. Set by the trainer when the hook is
            registered.
    """

    def before_train(self):
        """
        Called before the first iteration.
        """
        pass

    def after_train(self):
        """
        Called after the last iteration.
        """
        pass

    def before_epoch(self):
        """
        Called before each epoch
        """
        pass

    def after_epoch(self):
        """
        Called after each epoch
        """
        pass

    def before_step(self):
        """
        Called before each iteration.
        """
        pass

    def after_step(self):
        """
        Called after each iteration.
        """
        pass


class TrainerBase:
    """
    Base class for iterative trainer with hooks.
    The only assumption we made here is: the training runs in two loops, the epoch loop
    and the step loop in a epoch loop.
    A subclass can implement what the loop is.
    We made no assumptions about the existence of dataloader, optimizer, model, etc.
    Attributes:
        epoch(int): the current epoch.
        start_epoch(int): The epoch to start with.
            By convention the minimum possible value is 0.
        end_epoch(int): The epoch to end training.
        iters_per_epoch(int): the total iteration steps in a epoch.
        iter(int): the current iteration.
        start_iter(int): The iteration to start with.
            By convention the minimum possible value is 0.
        end_iter(int): The iteration to end training.
        storage(EventStorage): An EventStorage that's opened during the course of training.
    """

    def __init__(self):
        self._hooks = []

        self.epoch = 0
        self.start_epoch = 0
        self.end_epoch = 0
        self.iters_per_epoch = 0

        # iter is global, not iter in per epoch
        self.start_iter = 0
        self.end_iter = 0
        self.iter = 0

        self.storage = None

    def register_hooks(self, hooks):
        """
        Register hooks to the trainer. The hooks are executed in the order
        they are registered.
        Args:
            hooks (list[Optional[HookBase]]): list of hooks
        """
        hooks = [h for h in hooks if h is not None]
        for h in hooks:
            assert isinstance(h, HookBase)
            # To avoid circular reference, hooks and trainer cannot own each other.
            # This normally does not matter, but will cause memory leak if the
            # involved objects contain __del__:
            # See http://engineering.hearsaysocial.com/2013/06/16/circular-references-in-python/
            h.trainer = weakref.proxy(self)
        self._hooks.extend(hooks)

    def train(self, start_epoch: int = 0, end_epoch: int = 0, iters_per_epoch: int = 0):
        """
        Args:
            start_iter, max_iter (int): See docs above
        """
        logger = logging.getLogger(__name__)
        logger.info("Starting training from iteration {}".format(start_epoch))
        assert iters_per_epoch > 0, "steps_per_epoch: {} is invalid".format(iters_per_epoch)

        self.epoch = start_epoch
        self.start_epoch = start_epoch
        self.end_epoch = end_epoch
        self.iters_per_epoch = iters_per_epoch

        self.iter = self.start_epoch * iters_per_epoch
        self.start_iter = self.start_epoch * iters_per_epoch
        self.end_iter = self.end_epoch * iters_per_epoch

        with EventStorage(start_iter=self.start_iter, start_epoch=self.start_epoch, end_epoch=self.end_epoch, iters_per_epoch=self.iters_per_epoch) as self.storage:
            try:
                self.before_train()
                for self.epoch in range(start_epoch, end_epoch):
                    self.before_epoch()
                    for i in range(self.iters_per_epoch):
                        self.iter = self.epoch * self.iters_per_epoch + i
                        self.before_step()
                        self.run_step()
                        self.after_step()
                    self.after_epoch()
            except Exception:
                logger.exception("Exception during training:")
            finally:
                self.after_train()

    def before_train(self):
        for h in self._hooks:
            h.before_train()

    def after_train(self):
        for h in self._hooks:
            h.after_train()

    def before_epoch(self):
        for h in self._hooks:
            h.before_epoch()

    def after_epoch(self):
        for h in self._hooks:
            h.after_epoch()
        self.storage.epoch_step()

    def before_step(self):
        for h in self._hooks:
            h.before_step()

    def after_step(self):
        for h in self._hooks:
            h.after_step()
        # this guarantees, that in each hook's after_step, storage.iter == trainer.iter
        self.storage.step()

    def run_step(self):
        raise NotImplementedError

    @property
    def iter_in_epoch(self):
        if self.iters_per_epoch == 0:
            return -1
        return self.iter % self.iters_per_epoch


class SimpleTrainer(TrainerBase):
    """
    A simple trainer for the most common type of task:
    single-cost single-optimizer single-data-source iterative optimization,
    optionally using data-parallelism.
    It assumes that every step, you:

    1. Compute the loss with a data from the data_loader.
    2. Compute the gradients with the above loss.
    3. Update the model with the optimizer.

    All other tasks during training (checkpointing, logging, evaluation, LR schedule)
    are maintained by hooks, which can be registered by :meth:`TrainerBase.register_hooks`.

    If you want to do anything fancier than this,
    either subclass TrainerBase and implement your own `run_step`,
    or write your own training loop.
    """

    def __init__(self, model, data_loader, optimizer):
        """
        Args:
            model: a torch Module. Takes a data from data_loader and returns a
                dict of losses.
            data_loader: an iterable. Contains data to be used to call model.
            optimizer: a torch optimizer.
        """
        super().__init__()

        """
        We set the model to training mode in the trainer.
        However it's valid to train a model that's in eval mode.
        If you want your model (or a submodule of it) to behave
        like evaluation during training, you can overwrite its train() method.
        """
        model.train()

        self.model = model
        self.data_loader = data_loader
        self._data_loader_iter = iter(data_loader)
        self.optimizer = optimizer
        self.model.trainer = weakref.proxy(self)
        if isinstance(model, DistributedDataParallel):
            self.model.module.trainer = weakref.proxy(self)
        self.data_loader.trainer = weakref.proxy(self)
        self.optimizer.trainer = weakref.proxy(self)

    def run_step(self):
        """
        Implement the standard training logic described above.
        """
        assert self.model.training, "[SimpleTrainer] model was changed to eval mode!"
        start = time.perf_counter()
        """
        If you want to do something with the data, you can wrap the dataloader.
        """
        data = next(self._data_loader_iter)
        data_time = time.perf_counter() - start

        """
        If you want to do something with the losses, you can wrap the model.
        """
        loss_dict = self.model(data)
        losses = sum(loss_dict.values())

        """
        If you need to accumulate gradients or do something similar, you can
        wrap the optimizer with your custom `zero_grad()` method.
        """
        self.optimizer.zero_grad()
        losses.backward()

        self._write_metrics(loss_dict, data_time)

        """
        If you need gradient clipping/scaling or other processing, you can
        wrap the optimizer with your custom `step()` method. But it is
        suboptimal as explained in https://arxiv.org/abs/2006.15704 Sec 3.2.4
        """
        self.optimizer.step()

    def _write_metrics(self, loss_dict: Dict[str, torch.Tensor], data_time: float):
        """
        Args:
            loss_dict (dict): dict of scalar losses
            data_time (float): time taken by the dataloader iteration
        """
        device = next(iter(loss_dict.values())).device

        # # Use a new stream so these ops don't wait for DDP or backward
        # with torch.cuda.stream(torch.cuda.Stream() if device.type == "cuda" else None):
        metrics_dict = {k: v.detach().cpu().item() for k, v in loss_dict.items()}
        metrics_dict["data_time"] = data_time

        # Gather metrics among all workers for logging
        # This assumes we do DDP-style training, which is currently the only
        # supported method in detectron2.
        all_metrics_dict = comm.gather(metrics_dict)

        if comm.is_main_process():
            storage = get_event_storage()

            # data_time among workers can have high variance. The actual latency
            # caused by data_time is the maximum among workers.
            data_time = np.max([x.pop("data_time") for x in all_metrics_dict])
            storage.put_scalar("data_time", data_time)
            # average the rest metrics
            metrics_dict = {
                k: np.mean([x[k] for x in all_metrics_dict]) for k in all_metrics_dict[0].keys()
            }
            total_losses_reduced = sum(metrics_dict.values())
            if not np.isfinite(total_losses_reduced):
                raise FloatingPointError(
                    f"Loss became infinite or NaN at iteration={self.iter}!\n"
                    f"loss_dict = {metrics_dict}"
                )
            storage.put_scalar("total_loss", total_losses_reduced)
            if len(metrics_dict) > 1:
                storage.put_scalars(**metrics_dict)

