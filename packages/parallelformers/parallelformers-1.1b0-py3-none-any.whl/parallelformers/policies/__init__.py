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

from parallelformers.policies.ctrl import CTRLPolicy
from parallelformers.policies.deberta_v2 import DebertaV2Policy
from parallelformers.policies.distil_bert import DistilBertPolicy
from parallelformers.policies.electra import ElectraPolicy
from parallelformers.policies.gpt_neo import GPTNeoPolicy
from parallelformers.policies.bert import BertPolicy
from parallelformers.policies.bart import BartEncoderPolicy, BartDecoderPolicy
from parallelformers.policies.blenderbot import BlenderbotDecoderPolicy, BlenderbotEncoderPolicy
from parallelformers.policies.blenderbot_small import BlenderbotSmallDecoderPolicy, BlenderbotSmallEncoderPolicy
from parallelformers.policies.deberta import DebertaPolicy
from parallelformers.policies.openai import OpenAIGPTPolicy
from parallelformers.policies.transfo_xl import TransfoXLPolicy
from parallelformers.policies.roberta import RobertaPolicy
from parallelformers.policies.albert import AlbertPolicy
from parallelformers.policies.gpt2 import GPT2Policy
from parallelformers.policies.base.auto import AutoPolicy

__all__ = {
    GPTNeoPolicy,
    BertPolicy,
    BartEncoderPolicy,
    BartDecoderPolicy,
    BlenderbotEncoderPolicy,
    BlenderbotDecoderPolicy,
    DebertaPolicy,
    TransfoXLPolicy,
    RobertaPolicy,
    AlbertPolicy,
    GPT2Policy,
    CTRLPolicy,
    DebertaV2Policy,
    OpenAIGPTPolicy,
    ElectraPolicy,
    BlenderbotSmallEncoderPolicy,
    BlenderbotSmallDecoderPolicy,
    DistilBertPolicy,
    AutoPolicy,
}
