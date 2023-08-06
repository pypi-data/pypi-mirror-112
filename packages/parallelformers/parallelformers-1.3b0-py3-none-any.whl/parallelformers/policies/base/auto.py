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

from transformers import (
    GPTNeoPreTrainedModel,
    BertPreTrainedModel,
    BartPretrainedModel,
    BlenderbotPreTrainedModel,
    DebertaPreTrainedModel,
    TransfoXLPreTrainedModel,
    RobertaPreTrainedModel,
    AlbertPreTrainedModel,
    GPT2PreTrainedModel,
    CTRLPreTrainedModel,
    DebertaV2PreTrainedModel,
    OpenAIGPTPreTrainedModel,
    ElectraPreTrainedModel,
    BlenderbotSmallPreTrainedModel,
    DistilBertPreTrainedModel,
)

from parallelformers.policies import (
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
)


class AutoPolicy:

    def get_policy(self, model):
        for k, v in self.available().items():
            if isinstance(model, k):
                return v

        return None

    @staticmethod
    def available():
        return {
            GPTNeoPreTrainedModel: GPTNeoPolicy,
            BertPreTrainedModel: BertPolicy,
            BartPretrainedModel: (
                BartEncoderPolicy,
                BartDecoderPolicy,
            ),
            BlenderbotPreTrainedModel: (
                BlenderbotEncoderPolicy,
                BlenderbotDecoderPolicy,
            ),
            DebertaPreTrainedModel: DebertaPolicy,
            TransfoXLPreTrainedModel: TransfoXLPolicy,
            RobertaPreTrainedModel: RobertaPolicy,
            AlbertPreTrainedModel: AlbertPolicy,
            GPT2PreTrainedModel: GPT2Policy,
            CTRLPreTrainedModel: CTRLPolicy,
            DebertaV2PreTrainedModel: DebertaV2Policy,
            OpenAIGPTPreTrainedModel: OpenAIGPTPolicy,
            ElectraPreTrainedModel: ElectraPolicy,
            BlenderbotSmallPreTrainedModel: (
                BlenderbotSmallEncoderPolicy,
                BlenderbotSmallDecoderPolicy,
            ),
            DistilBertPreTrainedModel: DistilBertPolicy,
        }
