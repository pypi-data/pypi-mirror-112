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
import traceback
import torch.multiprocessing as mp
import torch

from torch import nn
from copy import deepcopy
from typing import List
from contextlib import suppress
from parallelformers.parallel import ParallelProcess


class parallelize(object):

    def __init__(
        self,
        model: nn.Module,
        fp16: bool,
        gpus: List[int],
        master_addr: str = "127.0.0.1",
        master_port: int = 29500,
        backend="nccl",
        daemon: bool = True,
        hijack_methods=None,
        custom_policy_cls=None,
        custom_cross_policy_cls=None,
        verbose: str = None,
        init_method="spawn",
    ):
        """
        Parallelformers end-point interface object

        Args:
            model (nn.Module): Huggingface pre-trained transformer model.
            fp16: (bool): whether use FP16 or not.
            gpus (List[int]): list of GPU ids (e.g. 4GPU => [0, 1, 2, 3])
            master_addr (str): master process address for process communication
            master_port (int): master process port for process communication
            backend (str): distributed backend
            daemon (bool): whether make process daemon or not (default=True)
            verbose (bool): logging current gpu states (one of ['detail', 'simple', None]
        """

        os.environ["MKL_SERVICE_FORCE_INTEL"] = 'GNU'
        mp.set_sharing_strategy('file_system')

        # Using fork often leads to deadlock.
        if mp.get_start_method() != init_method:
            with suppress(Exception):
                mp.set_start_method(init_method, force=True)

        if hijack_methods is None:
            hijack_methods = self.builtin_methods()

        if fp16:
            model = model.half()

        self.model = model
        self.fp16 = fp16
        self.gpus = gpus
        self.backend = backend
        self.daemon = daemon
        self.verbose = verbose
        self.custom_policy_cls = custom_policy_cls
        self.custom_cross_policy_cls = custom_cross_policy_cls
        self._init_environments(master_addr, master_port)

        self.processes = []
        self.parallel_mutexes = []
        self.inference_mutexes = []
        self.inputs_queues = []
        self.outputs_queues = []

        self.orig_methods = {}
        for attr in hijack_methods:
            if hasattr(self.model, attr):
                fn = getattr(self.model, attr)
                self.orig_methods[attr] = fn

        self._parallelize()
        for attr in hijack_methods:
            if hasattr(self.model, attr):
                self._hijack_methods(attr)

        self._memory_logger = [
            "memory_reserved",
            "memory_allocated",
            "memory_cached",
        ]

        for attr in self._memory_logger:
            self._inject_methods(attr)

    def _init_environments(
        self,
        master_addr: str,
        master_port: int,
    ):
        """
        Initialize environment variables

        Args:
            master_addr (str): master process address for process communication
            master_port (int): master process port for process communication
        """
        os.environ["MASTER_ADDR"] = str(master_addr)
        os.environ["MASTER_PORT"] = str(master_port)
        os.environ["WORLD_SIZE"] = str(len(self.gpus))

    def _hijack_methods(self, attr_name):
        setattr(
            self.model,
            attr_name,
            lambda *inputs, **kwargs: self._hijack(
                inputs=inputs,
                kwargs=kwargs,
                func=attr_name,
            ),
        )

    def _inject_methods(self, method):
        setattr(
            self.model, method, lambda: self._hijack(
                inputs='dummy',
                kwargs={'dummy': 'dummy'},
                func=method,
            ))

    @staticmethod
    def builtin_methods():
        return [
            "generate",
            "forward",
            "to",
            "cpu",
            "cuda",
        ]

    def _deparallelize(self):
        for k, v in self.orig_methods.items():
            setattr(self.model, k, v)

        for method in self._memory_logger:
            setattr(self.model, method, None)

        for process in self.processes:
            process.join()

        torch.cuda.synchronize()
        torch.cuda.empty_cache()

    def _parallelize(self):
        """
        Create processes for model parallelization and parallel inference
        """

        try:
            for rank in self.gpus:
                parallel_mutex = mp.Event()
                inference_mutex = mp.Event()
                self.parallel_mutexes.append(parallel_mutex)
                self.inference_mutexes.append(inference_mutex)

                inputs_queue = mp.Queue()
                outputs_queue = mp.Queue()
                self.inputs_queues.append(inputs_queue)
                self.outputs_queues.append(outputs_queue)

                process = ParallelProcess(
                    rank=rank,
                    model=self.model,
                    fp16=self.fp16,
                    gpus=self.gpus,
                    inputs_queue=inputs_queue,
                    outputs_queue=outputs_queue,
                    parallel_mutex=parallel_mutex,
                    inference_mutex=inference_mutex,
                    custom_policy_cls=self.custom_policy_cls,
                    custom_cross_policy_cls=self.custom_cross_policy_cls,
                    backend=self.backend,
                    verbose=self.verbose,
                    orig_methods=self.orig_methods,
                )

                process.daemon = self.daemon
                # When the main process done, all processes should frees resources.
                # So default value is True, but change it according to your needs.

                process.start()
                self.processes.append(process)

            for p_mutex in self.parallel_mutexes:
                p_mutex.wait()

        except:
            traceback.print_exc()
            self._deparallelize()

    def _hijack(self, inputs, kwargs, func):
        try:
            for i_mutex, i_queue in zip(
                    self.inference_mutexes,
                    self.inputs_queues,
            ):
                i_queue.put((inputs, kwargs, func))
                i_mutex.set()
                # producer part

            if func in ["to", "cpu", "cuda"]:
                self._deparallelize()

                if func == "cpu":
                    self.model = self.model.cpu(*inputs, **kwargs)
                elif func == "cuda":
                    self.model = self.model.cuda(*inputs, **kwargs)
                else:
                    self.model = self.model.to(*inputs, **kwargs)

                return self.model
            else:
                outputs = []
                for o_queue in self.outputs_queues:
                    output = o_queue.get()
                    # consumer part

                    _output = []
                    if isinstance(output, tuple):
                        for o in output:
                            if torch.is_tensor(o):
                                _o = o.clone().to("cpu")
                            else:
                                _o = deepcopy(o)
                            _output.append(_o)
                    else:
                        if torch.is_tensor(output):
                            _output = output.clone().to("cpu")
                        else:
                            _output = deepcopy(output)

                    del output
                    outputs.append(_output)

                if func not in self._memory_logger:
                    return outputs[0]
                else:
                    return dict(outputs)

        except:
            traceback.print_exc()
            self._deparallelize()

    def setattr_to_model(self, key, val):
        for process in self.processes:
            setattr(process.model, key, val)

    def getattr_from_model(self, key):
        return [getattr(process.model, key) for process in self.processes]
