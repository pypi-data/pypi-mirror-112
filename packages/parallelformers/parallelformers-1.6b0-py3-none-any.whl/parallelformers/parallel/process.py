# Copyright 2021 TUNiB inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import types
import traceback
import torch
import torch.nn as nn
import torch.multiprocessing as mp

from copy import deepcopy
from inspect import signature
from typing import List
from parallelformers.parallel import ParallelEngine


class ParallelProcess(mp.Process):

    _memory_logger = {
        "memory_summary": torch.cuda.memory_summary,
        "memory_reserved": torch.cuda.memory_reserved,
        "memory_cached": torch.cuda.memory_reserved,
        "memory_allocated": torch.cuda.memory_allocated,
    }

    def __init__(
        self,
        model: nn.Module,
        fp16: bool,
        rank: int,
        gpus: List[int],
        inputs_queue: mp.Queue,
        outputs_queue: mp.Queue,
        parallel_mutex: mp.Event,
        inference_mutex: mp.Event,
        custom_policy_cls,
        custom_cross_policy_cls,
        verbose: str,
        backend: str,
        orig_methods: dict,
    ):
        """
        Process of model parallelization and parallel inference

        Args:
            model (nn.Module): model weights
            fp16: (bool): whether use FP16 or not.
            rank (int): current GPU rank
            gpus (List[int]): list of gpu ids
            inputs_queue (mp.Queue): input data queue from user
            outputs_queue (mp.Queue): output data queue from model
            parallel_mutex (mp.Event): mutex object to notify parallelization state
            inference_mutex (mp.Event): mutex object to notify inference state
            verbose (str): turn on gpu summary
            backend (str): distributed process backend
        """
        super().__init__()
        self._set_environ(rank)
        self.model = model
        self.fp16 = fp16
        self.gpus = gpus
        self.inputs_queue = inputs_queue
        self.outputs_queue = outputs_queue
        self.parallel_mutex = parallel_mutex
        self.inference_mutex = inference_mutex
        self.custom_policy_cls = custom_policy_cls
        self.custom_cross_policy_cls = custom_cross_policy_cls
        self.verbose = verbose
        self.backend = backend
        self.orig_methods = orig_methods

    def _set_environ(self, rank):
        os.environ["RANK"] = str(rank)
        os.environ["LOCAL_RANK"] = str(rank)

    def _destroy(self):
        for k, v in self.orig_methods.items():
            setattr(self.model, k, v)

        for method in self._memory_logger:
            setattr(self.model, method, None)

        torch.cuda.synchronize()
        torch.cuda.empty_cache()

    @torch.no_grad()
    def _observe(self, model):
        while True:
            try:
                self.inference_mutex.wait()
                self.inference_mutex.clear()
                device = torch.cuda.current_device()

                # consumer part
                inputs, kwargs, function = self.inputs_queue.get()
                inputs_, kwargs_, fn_name = [], {}, deepcopy(function)

                for i in inputs:
                    if torch.is_tensor(i):
                        i = i.clone().to(device)
                        inputs_.append(i)
                    else:
                        inputs_.append(deepcopy(i))

                for k in kwargs:
                    if torch.is_tensor(kwargs[k]):
                        kwg = kwargs[k].clone().to(device)
                        kwargs_[k] = kwg
                    else:
                        kwargs_[k] = deepcopy(kwargs[k])

                if fn_name not in self._memory_logger:
                    function_ = getattr(model, fn_name)
                    n_params = len(signature(function_).parameters)

                    if n_params > 0:
                        outputs = function_(
                            *inputs_,
                            **kwargs_,
                        )
                    else:
                        outputs = function_()
                else:
                    device_name = f"cuda:{device}"
                    outputs = (device_name, str(self._memory_logger[fn_name](device)))

                # release memory
                del inputs
                del kwargs
                del function

                # Post-processing for process communication
                if fn_name in ["cuda", "cpu", "to"]:
                    break

                if isinstance(outputs, types.GeneratorType):
                    outputs = list(outputs)

                # producer part
                self.outputs_queue.put(outputs)

                # remove input tensors
                for i in range(len(inputs_)):
                    if torch.is_tensor(inputs_[i]):
                        inputs_[i] = inputs_[i].cpu()

                for k in kwargs_:
                    if torch.is_tensor(kwargs_[k]):
                        kwargs_[k] = kwargs_[k].cpu()

                del inputs_
                del kwargs_

            except:
                traceback.print_exc()
                break

    @torch.no_grad()
    def run(self) -> None:
        engine = ParallelEngine(
            gpus=self.gpus,
            backend=self.backend,
            custom_policy_cls=self.custom_policy_cls,
            custom_cross_policy_cls=self.custom_cross_policy_cls,
        )

        try:
            self.model = engine.parallelize(self.model, self.fp16)
            self.parallel_mutex.set()

            if self.verbose:
                if self.verbose is True or self.verbose.lower() == 'simple':
                    device = torch.cuda.current_device()
                    print(
                        f"GPU {device} alloc: {torch.cuda.memory_allocated(device)}"
                    )
                    print(
                        f"GPU {device} cached: {torch.cuda.memory_reserved(device)}"
                    )
                    print()

                elif self.verbose.lower() == 'detail':
                    print(torch.cuda.memory_summary())
                    print()

            self._observe(self.model)
            self._destroy()

        except:
            traceback.print_exc()
            self._destroy()
