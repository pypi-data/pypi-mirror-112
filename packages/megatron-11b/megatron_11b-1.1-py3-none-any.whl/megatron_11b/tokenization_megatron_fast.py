# coding=utf-8
# Copyright The Fairseq Authors and The HuggingFace Inc. team. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tokenization classes for Megatron."""
from transformers.utils import logging
from transformers.models.bart.tokenization_bart_fast import BartTokenizerFast
from .tokenization_megatron import MegatronTokenizer


logger = logging.get_logger(__name__)

# vocab and merges same as roberta
PRETRAINED_VOCAB_FILES_MAP = {
    "vocab_file": {
        "megatron-11b": "https://huggingface.co/roberta-large/resolve/main/vocab.json",
    },
    "merges_file": {
        "megatron-11b": "https://huggingface.co/roberta-large/resolve/main/merges.txt",
    },
}

PRETRAINED_POSITIONAL_EMBEDDINGS_SIZES = {
    "megatron-11b": 1024,
}


class MegatronTokenizerFast(BartTokenizerFast):
    r"""
    Construct a "fast" Megatron tokenizer (backed by HuggingFace's `tokenizers` library).

    :class:`~transformers.MegatronTokenizerFast` is identical to :class:`~transformers.BartTokenizerFast` and runs
    end-to-end tokenization: punctuation splitting and wordpiece.

    Refer to superclass :class:`~transformers.BartTokenizerFast` for usage examples and documentation concerning
    parameters.
    """

    pretrained_vocab_files_map = PRETRAINED_VOCAB_FILES_MAP
    max_model_input_sizes = PRETRAINED_POSITIONAL_EMBEDDINGS_SIZES
    slow_tokenizer_class = MegatronTokenizer
