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

import torch.nn as nn
from typing import Any
from parallelformers.parallel import TensorSlicer
from parallelformers.policies import AutoPolicy
from parallelformers.utils import rsetattr, rhasattr, rgetattr


class TensorReplacer(object):

    def __init__(
        self,
        model: nn.Module,
        mp_group: Any,
        fp16: bool,
        mp_size: int,
        custom_policy_cls,
        custom_cross_policy_cls,
    ):
        """
        Tensor Replacer object to replace Huggingface's layer into Megatron layer.

        Args:
            model (nn.Module): Huggingface pre-trained transformer model
            mp_group (Any): process group for model parallelism
            fp16: (bool): Whether use FP16 or not.
            custom_policy_cls (Policy): custom policy object (default=None)
            custom_cross_policy_cls (CrossAttentionDecoderPolicy): custom cross.py attention decdoer policy object (default=None)

        """
        self.model = model
        self.mp_group = mp_group
        self.fp16 = fp16
        self.mp_size = mp_size
        self.config = model.config
        self.policy_cls = custom_policy_cls
        self.cross_policy_cls = custom_cross_policy_cls
        self.slicer = TensorSlicer(self.mp_group)
        self.varname = "layer"

    def replace_module(self):
        if not self.policy_cls:
            self._auto_policy()

        replace_modules = self.policy_cls.replace_modules()
        replace_modules_names = [cls_name for cls_name in replace_modules]

        return self._replace_module(
            self.model,
            self.policy_cls,
            replace_modules,
            replace_modules_names,
        )

    def replace_cross_attention_module(self):
        if self.cross_policy_cls:
            replace_modules = self.cross_policy_cls.replace_modules()
            replace_modules_names = [cls_name for cls_name in replace_modules]

            return self._replace_module(
                self.model,
                self.cross_policy_cls,
                replace_modules,
                replace_modules_names,
            )

    def _auto_policy(self):
        auto = AutoPolicy()
        policy_cls = auto.get_policy(self.model)

        assert policy_cls is not None, \
            f"{self.model.__class__.__qualname__} is not supported yet.\n" \
            f"Currently we support {[i.__qualname__ for i in auto.available().keys()]}.\n" \
            f"To apply to unsupported models, you need to create a custom Policy object."

        if isinstance(policy_cls, tuple) or isinstance(policy_cls, list):
            self.policy_cls, self.cross_policy_cls = policy_cls
        else:
            self.policy_cls = policy_cls

    def _replace_module(
        self,
        model,
        policy_cls,
        replace_modules,
        replace_modules_names,
    ):

        for name, child in model.named_children():
            if child.__class__ == policy_cls.original_layer_class():
                policy = policy_cls(layer=child)

                for k, v in policy.replace_arguments(
                        self.config,
                        int(os.getenv("WORLD_SIZE")),
                ).items():
                    rsetattr(policy, f"{self.varname}.{k}", v)

                rsetattr(
                    model,
                    name,
                    self._make_megatron_layer(policy),
                )

            elif child.__class__.__qualname__ in replace_modules_names:
                for cls_name, cls in replace_modules.items():
                    if child.__class__.__qualname__ == cls_name:
                        for key in cls.__dict__.keys():
                            if rhasattr(child.__class__, key):
                                rsetattr(child.__class__, key,
                                         rgetattr(cls, key))

            else:
                self._replace_module(
                    child,
                    policy_cls,
                    replace_modules,
                    replace_modules_names,
                )

        return model

    def _preprocess(self, function_output, policy):
        weight_dict, bias_dict, weight_attr_dict, bias_attr_dict = {}, {}, {}, {}

        for i, layer_params in enumerate(function_output):
            w = layer_params.weight
            b = layer_params.bias
            replace = layer_params.replace
            n_fused = layer_params.n_fused
            conv = layer_params.is_convolution

            if w:
                w_layer = rgetattr(policy, f"{self.varname}.{w}")
                weight_dict[f"{self.varname}.{w}"] = w_layer
                weight_attr_dict[f"{self.varname}.{w}"] = (n_fused, conv)

                orig_layer_name = ".".join(w.split(".")[:-1])
                orig_layer = rgetattr(
                    policy,
                    f"{self.varname}.{orig_layer_name}",
                )

            if b:
                b_layer = rgetattr(policy, f"{self.varname}.{b}")
                bias_dict[f"{self.varname}.{b}"] = b_layer
                bias_attr_dict[f"{self.varname}.{b}"] = (n_fused, conv)

                orig_layer_name = ".".join(b.split(".")[:-1])
                orig_layer = rgetattr(
                    policy,
                    f"{self.varname}.{orig_layer_name}",
                )

            if not w and not b:
                raise Exception("both weight and bias are empty !")

            if replace is not None:
                orig_layer.__class__ = replace
                orig_layer.mp_group = self.mp_group

        return weight_dict, bias_dict, weight_attr_dict, bias_attr_dict

    def _set_parameters(
        self,
        policy,
        weight_name,
        bias_name,
        weight_param,
        bias_param,
        suffix="data",
    ):
        for name, param in zip(weight_name, weight_param):
            rsetattr(policy, f"{name}.{suffix}", param)
            self._set_layer_size(policy, name, param.size())

        for name, param in zip(bias_name, bias_param):
            rsetattr(policy, f"{name}.{suffix}", param)

        return policy

    @staticmethod
    def _set_layer_size(policy, name, size):
        layer_name = ".".join(f"{name}".split(".")[:-1])
        if rhasattr(policy, f"{layer_name}.nf"):
            rsetattr(
                policy,
                f"{layer_name}.nf",
                size[1],
            )
        else:
            for name in ["channels", "features"]:
                if name == "channels":
                    direction = ["in", "out"]
                else:
                    direction = ["out", "in"]
                for i, direction in enumerate(direction):
                    if rhasattr(policy, f"{layer_name}.{direction}_{name}"):
                        rsetattr(
                            policy,
                            f"{layer_name}.{direction}_{name}",
                            size[i],
                        )

    def _make_megatron_layer(self, policy):
        attn_qkvw, attn_qkvb, attn_qkvw_attr, attn_qkvb_attr = self._preprocess(
            policy.attn_qkv(),
            policy,
        )
        attn_outw, attn_outb, attn_outw_attr, attn_outb_attr = self._preprocess(
            policy.attn_out(),
            policy,
        )
        mlp_inw, mlp_inb, mlp_inw_attr, mlp_inb_attr = self._preprocess(
            policy.mlp_in(),
            policy,
        )
        mlp_outw, mlp_outb, mlp_outw_attr, mlp_outb_attr = self._preprocess(
            policy.mlp_out(),
            policy,
        )

        policy = self._set_parameters(
            policy,
            attn_qkvw,
            attn_qkvb,
            *self.slicer.column_slice(
                (attn_qkvw, attn_qkvb),
                (attn_qkvw_attr, attn_qkvb_attr),
            ),
        )

        policy = self._set_parameters(
            policy,
            attn_outw,
            attn_outb,
            *self.slicer.row_slice(
                (attn_outw, attn_outb),
                (attn_outw_attr, attn_outb_attr),
            ),
        )

        policy = self._set_parameters(
            policy,
            mlp_inw,
            mlp_inb,
            *self.slicer.column_slice(
                (mlp_inw, mlp_inb),
                (mlp_inw_attr, mlp_inb_attr),
            ),
        )

        policy = self._set_parameters(
            policy,
            mlp_outw,
            mlp_outb,
            *self.slicer.row_slice(
                (mlp_outw, mlp_outb),
                (mlp_outw_attr, mlp_outb_attr),
            ),
        )

        return policy.layer
