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
import torch
import torch.distributed as dist
from torch import Tensor, nn
from torch.nn import Linear
from transformers.modeling_utils import Conv1D


class ParallelModule(nn.Module):

    def __init__(self):
        super().__init__()
        self.mp_group = None


class AllReduceLinear(Linear, ParallelModule):

    def __init__(self, in_features: int, out_features: int):
        super().__init__(in_features, out_features)

    def forward(self, input: Tensor) -> Tensor:
        outputs = input.matmul(self.weight.t())

        if self.mp_group is not None and dist.get_world_size(
                group=self.mp_group) > 1:

            dist.all_reduce(
                outputs,
                group=self.mp_group,
            )

        if self.bias is not None:
            outputs += self.bias

        return outputs


class AllReduceConv1D(Conv1D, ParallelModule):

    def forward(self, x):
        size_out = x.size()[:-1] + (self.nf,)
        outputs = torch.mm(x.view(-1, x.size(-1)), self.weight)

        if self.mp_group is not None and dist.get_world_size(
                group=self.mp_group) > 1:

            dist.all_reduce(
                outputs,
                group=self.mp_group,
            )

        if self.bias is not None:
            outputs += self.bias

        return outputs.view(*size_out)
