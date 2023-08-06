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
import torch
import torch.nn as nn
import torch.distributed as dist

from typing import List
from parallelformers.utils import rsetattr
from parallelformers.parallel import TensorReplacer


class ParallelEngine(object):

    def __init__(
        self,
        gpus: List[int],
        custom_policy_cls,
        custom_cross_policy_cls,
        backend: str = "nccl",
    ):
        """
        Model parallel processing engine using DeepSpeed's module injection

        Args:
            gpus (List[int]): list of gpu ids
            backend (str): distributed backend
        """

        self.gpus = gpus
        self.custom_policy_cls = custom_policy_cls
        self.custom_cross_policy_cls = custom_cross_policy_cls
        self.mp_group = self.create_process_group(backend)
        # Create process group for model parallelization.

    def parallelize(
        self,
        model: nn.Module,
        fp16: bool,
    ):
        """
        Do parallelize using DeepSpeed's module injection

        Args:
            model (nn.Module): Huggingface pre-trained transformer model.
            model_type (str): model type you inputted (encoder, decoder, seq2seq)
            fp16: (bool): whether use FP16 or not.
        """
        super().__init__()
        assert not next(model.parameters()).is_cuda, \
            "Model should be on CPU before parallelization. It is more memory-efficient."

        replacer = TensorReplacer(
            model=model,
            fp16=fp16,
            mp_group=self.mp_group,
            mp_size=len(self.gpus),
            custom_policy_cls=self.custom_policy_cls,
            custom_cross_policy_cls=self.custom_cross_policy_cls,
        )

        # Replace Huggingface layer to Magatron layer.
        replacer.replace_module()
        if replacer.cross_policy_cls:
            replacer.replace_cross_attention_module()

        # Lazy GPU memory allocation (Only cpu tensors are loaded onto all gpus)
        # It's more memory-efficient than original implementation of DeepSpeed.
        for k, v in dict(model.state_dict()).items():
            if not v.is_cuda:
                if torch.is_tensor(v):
                    rsetattr(
                        model,
                        k + ".data",
                        v.to(torch.cuda.current_device()),
                    )

        return model

    def create_process_group(self, backend: str):
        """
        Create Pytorch distributed process group

        Args:
            backend (str): distributed backend

        Returns:
            (new_group): process group
        """
        if not dist.is_initialized():
            dist.init_process_group(backend=backend)

        torch.cuda.set_device(int(os.getenv("LOCAL_RANK", "0")))
        new_group = dist.new_group([i for i in self.gpus])

        return new_group
