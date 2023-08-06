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
import torch.distributed as dist


class TensorSlicer(object):

    def __init__(self, mp_group: int):
        """
        Args:
            mp_group (torch.distributed.ProcessGroupNCCL): Distributed group for model parallelism
        """
        if dist.is_initialized() and mp_group is not None:
            self.gpu_index = dist.get_rank(group=mp_group)
            self.world_size = int(os.getenv("WORLD_SIZE"))
        else:
            self.gpu_index = 0
            self.world_size = 1

    def _slice_tensor(self, tensor, attributes, dim, is_bias):
        if not tensor:
            return [None]

        n_fused_list, convolution_list = [], []
        for (k_tensor, v_tensor), (k_attr, v_attr) in zip(
                tensor.items(),
                attributes.items(),
        ):
            if k_tensor == k_attr:
                n_fused, is_conv = v_attr
                n_fused_list.append(n_fused)
                convolution_list.append(is_conv)

        tensor = list(tensor.values())
        slices = []

        for proj_layer, n_fused, is_conv in zip(
                tensor,
                n_fused_list,
                convolution_list,
        ):
            device = torch.cuda.current_device()
            dim = dim if not is_conv or is_bias else abs(dim - 1)
            n_fused = 1 if not n_fused else n_fused

            proj_layer = proj_layer.chunk(
                n_fused * self.world_size,
                dim=dim,
            )

            if n_fused > 1:
                ranks = (len(proj_layer) + self.world_size -
                         1) // self.world_size
                proj_layer = [
                    proj_layer[i * self.world_size:(i + 1) * self.world_size]
                    for i in range(ranks)
                ]
                proj_layer = list(
                    map(lambda x: torch.cat([*x], dim=-1), zip(*proj_layer)))

            proj_layer = proj_layer[self.gpu_index].to(device)
            slices.append(proj_layer)

        return tuple(slices)

    def _slice(self, policy_inputs, dim, slice_bias, attributes):
        weight, bias = policy_inputs
        w_attr, b_attr = attributes
        weight = self._slice_tensor(
            weight,
            w_attr,
            dim,
            is_bias=False,
        )

        if slice_bias:
            bias = self._slice_tensor(
                bias,
                b_attr,
                0,
                is_bias=True,
            )
        else:
            bias = tuple(bias.values())

        return weight, bias

    def column_slice(
        self,
        policy_inputs,
        attributes,
    ):
        return self._slice(
            policy_inputs,
            dim=0,
            slice_bias=True,
            attributes=attributes,
        )

    def row_slice(
        self,
        policy_inputs,
        attributes,
    ):
        return self._slice(
            policy_inputs,
            dim=1,
            slice_bias=False,
            attributes=attributes,
        )
