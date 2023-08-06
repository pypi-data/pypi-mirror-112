# encoding: utf-8


import collections
import operator
from typing import Dict, List, Any, Optional, Union

import numpy as np
import tqdm
from tensorflow.keras.preprocessing.sequence import pad_sequences

from nlp_tools.generators import CorpusGenerator
from nlp_tools.logger import logger
from nlp_tools.processors.abc_label_processor import ABCLabelProcessor
from nlp_tools.types import TextSamplesVar


class NerLabelProcessor(ABCLabelProcessor):
    """
    Generic processors for the sequence samples.
    """

    def to_dict(self) -> Dict[str, Any]:
        data = super(NerLabelProcessor, self).to_dict()
        data['config'].update({
            'embedding_max_position': self.embedding_max_position,
            'max_sentence_length':self.max_sentence_length
        })
        return data

    def __init__(self,
                 **kwargs: Any) -> None:
        """

        Args:
            vocab_dict_type: initial vocab dict type, one of `text` `labeling`.
            **kwargs:
        """
        super(NerLabelProcessor, self).__init__(**kwargs)
        self._initial_vocab_dic = {
            "[PAD]": 0
        }



    def update_length_info(self,embedding_max_position=None,max_sentence_length=None):
        self.embedding_max_position = embedding_max_position
        self.max_sentence_length = max_sentence_length

    def build_vocab_generator(self,
                              generators: List[CorpusGenerator]) -> None:
        if not self.vocab2idx:
            vocab2idx = self._initial_vocab_dic
            token2count: Dict[str, int] = {}
            for gen in generators:
                for _, label in tqdm.tqdm(gen, desc="Preparing label dict"):
                    ## ner任务下面，label 应该是一个list
                    assert type(label) == list
                    for token in label:
                        count = token2count.get(token, 0)
                        token2count[token] = count + 1

            sorted_token2count = sorted(token2count.items(),
                                        key=operator.itemgetter(1),
                                        reverse=True)
            token2count = collections.OrderedDict(sorted_token2count)
            for token, token_count in token2count.items():
                vocab2idx[token] = len(vocab2idx)
            self.vocab2idx = vocab2idx
            self.idx2vocab = dict([(v, k) for k, v in self.vocab2idx.items()])

            top_k_vocab = [k for (k, v) in list(self.vocab2idx.items())[:10]]
            logger.debug(f"--- Build label finished, Total: {len(self.vocab2idx)} ---")
            logger.debug(f"Top-10: {top_k_vocab}")




    def transform(self,samples: TextSamplesVar,seq_length=None) -> np.ndarray:
        if not seq_length:
            seq_length = self.max_sentence_length

        if seq_length == None:
            seq_length = max([len(i) for i in samples]) + 2
        if self.embedding_max_position is not None and self.embedding_max_position < seq_length:
            seq_length = self.embedding_max_position



        numerized_samples = []
        for seq in samples:
            if len(seq) > seq_length-2:
                seq = seq[:seq_length-2]
            seq = [self.token_pad] + seq + [self.token_pad]
            numerized_samples.append([self.vocab2idx[token] for token in seq])

        sample_index = pad_sequences(numerized_samples, seq_length, padding='post', truncating='post')
        label_ids = np.array(sample_index)
        return label_ids

    def inverse_transform(self,
                          labels: Union[List[List[int]], np.ndarray],
                          lengths: List[int] = None,
                          **kwargs: Any) -> List[List[str]]:
        result = []
        for index, seq in enumerate(labels):
            labels_ = [self.idx2vocab[idx] for idx in seq]

            if lengths is not None:
                labels_ = labels_[1:lengths[index] + 1]
            else:
                labels_ = labels_[1:-1]
            result.append(labels_)
        return result





if __name__ == "__main__":
    pass
