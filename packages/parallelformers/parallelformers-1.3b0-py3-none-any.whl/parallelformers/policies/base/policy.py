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

from abc import abstractmethod, ABC
from dataclasses import dataclass
from typing import Any


@dataclass
class Layer:
    weight: Any = None
    bias: Any = None
    n_fused: Any = None
    replace: Any = None
    is_convolution: Any = None


class Policy(ABC):

    def __init__(self, layer):
        """
        Tensor replacement policy object for Transformer Layer
        """

        super().__init__()
        self.layer = layer

    @staticmethod
    def replace_arguments(config, world_size):
        """
        Arguments dictionary for replacement.

        Returns:
            {
                "param_name_1": reset_value_1,
                "param_name_2": reset_value_2,
                "param_name_3": reset_value_3,
                ...
                "param_name_n": reset_value_n,
            }
        """
        return {}

    @staticmethod
    def replace_modules():
        """
        Classes (modules) dictionary for replacement.

        Returns:
            {
                orig_class_name_1: reset_module_class_1,
                orig_class_name_2: reset_module_class_2,
                orig_class_name_3: reset_module_class_3,
                ...
                orig_class_name_4: reset_module_class_n,
            }
        """
        return {}

    @staticmethod
    @abstractmethod
    def attn_qkv():
        """
        Attention query, key, value projection layer

        Returns:
            List[Layer]: List of layer object
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def attn_out():
        """
        Attention output projection layer

        Returns:
            List[Layer]: List of layer object
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def mlp_in():
        """
        h -> 4h mlp layer

        Returns:
            List[Layer]: List of layer object
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def mlp_out():
        """
        4h -> h mlp layer

        Returns:
            List[Layer]: List of layer object
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def original_layer_class():
        """
        Returns:
            original layer class that has attention and mlp layer
            - e.g. BertLayer, GPT2Block, BartEncoderLayer, ...
        """
        raise NotImplementedError
