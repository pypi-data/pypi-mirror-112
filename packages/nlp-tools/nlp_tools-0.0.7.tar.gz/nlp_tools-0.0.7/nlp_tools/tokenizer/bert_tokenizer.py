from typing import Dict,Any

from nlp_tools.tokenizer.base_tokenizer import ABCTokenizer
from bert4keras.tokenizers import load_vocab,Tokenizer






class BertTokenizer(Tokenizer,ABCTokenizer):

    """
    Bert Like Tokenizer, ref: https://github.com/CyberZHG/keras-bert/blob/master/keras_bert/tokenizer.py

    """
    def to_dict(self) -> Dict[str, Any]:
        data = super(BertTokenizer, self).to_dict()
        data['config']['token_dict'] = self._token_dict
        data['config']['do_lower_case'] = self._do_lower_case
        data['config']['simplified'] = self.simplified
        data['config']['keep_tokens'] = self.keep_tokens
        data['config']['max_position'] = self.max_position
        return data

    def __init__(self,token_dict=None, do_lower_case=False,simplified=False,keep_tokens = None,max_position = 512):
        self.simplified = simplified
        self.keep_tokens = keep_tokens
        self.max_position = max_position
        self.token_dict = token_dict
        self.do_lower_case = do_lower_case
        if type(token_dict) != dict:
            if simplified:
                self.token_dict, self.keep_tokens = load_vocab(
                    dict_path=token_dict,
                    simplified=simplified,
                    startswith=['[PAD]', '[UNK]', '[CLS]', '[SEP]'],
                )
            else:
                self.token_dict = load_vocab(
                    dict_path=token_dict,
                )
        super(BertTokenizer,self).__init__(token_dict=self.token_dict,do_lower_case=self.do_lower_case)


    def tokenize(self, text, maxlen=None,**kwargs):
        if not maxlen:
            maxlen = self.max_position
        elif maxlen > self.max_position:
            maxlen = self.max_position

        if type(text) == str:
            text = super(BertTokenizer, self).tokenize(text,maxlen=maxlen)
        elif type(text) == list:
            if len(text) > maxlen -2:
                text = text[:maxlen-2]

            # 如果不以cls开头，则需要补充cls
            if text[0] != '[CLS]':
                text = ['[CLS]'] + text + ['[SEP]']
        return text

    def encode(self,
                text,
                second_text=None,
                maxlen=None,
                pattern='S*E*E',
                truncate_from='right'):
        assert type(text) in [list, str]
        if maxlen and maxlen > self.max_position:
            maxlen = self.max_position

        text = self.tokenize(text)
        tokens, segment_ids = super(BertTokenizer, self).encode(text, maxlen=maxlen,second_text=second_text,pattern=pattern,truncate_from=truncate_from)
        return tokens, segment_ids

    def id_to_token(self, id):
        return super(BertTokenizer, self).id_to_token(id)

if __name__ == '__main__':
    import os
    bert_model_path = r'/home/qiufengfeng/nlp/pre_trained_model/chinese_L-12_H-768_A-12/chinese_L-12_H-768_A-12/'
    bert_model_token_path = os.path.join(bert_model_path, 'vocab.txt')
    bert_tokenizer = BertTokenizer(bert_model_token_path)
    print(bert_tokenizer.tokenize("[CLS]"))