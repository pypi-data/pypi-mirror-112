import codecs
import json
from typing import Dict,List,Any,Optional
from bert4keras.models import build_transformer_model
from nlp_tools.embeddings.abc_embedding import ABCEmbedding

class TransformerEmbedding(ABCEmbedding):
    """
    TransformerEmbedding is based on bert4keras.
    The embeddings itself are wrapped into our simple embedding interface so that they can be used like any other embedding.
    """
    def to_dict(self) -> Dict[str, Any]:
        info_dic = super(TransformerEmbedding, self).to_dict()
        info_dic['config']['model_type'] = self.model_type
        info_dic['config']['max_position'] = self.max_position
        info_dic['config']['config_path'] = self.config_path
        info_dic['config']['checkpoint_path'] = self.checkpoint_path
        info_dic['config']['bert_application'] = self.bert_application
        info_dic['config']['keep_tokens'] = self.bert_application
        return info_dic

    def __init__(self,
                 config_path=None,
                 checkpoint_path: str =None,
                 model_type: str = 'bert',
                 bert_application='encoder',
                 keep_tokens = None,
                 max_position=512,
                 **kwargs: Any):
        """

        Args:
            vocab_path: vocab file path, example `vocab.txt`
            config_path: model config path, example `config.json`
            checkpoint_path: model weight path, example `model.ckpt-100000`
            model_type: transfer model type, {bert, albert, nezha, gpt2_ml, t5}
            kwargs: additional params
        """
        super(TransformerEmbedding, self).__init__(**kwargs)

        self.checkpoint_path = checkpoint_path
        self.config_path = config_path

        self.model_type = model_type
        self.keep_tokens = keep_tokens
        self.bert_application = bert_application

        self.max_position = max_position


        self.with_pool = kwargs.get("with_pool",False)
        # with open(config_path, 'r') as f:
        #     config = json.loads(f.read())
        #     if 'max_position' in config:
        #         self.max_position = config['max_position']
        #     else:
        #         self.max_position = config.get('max_position_embeddings')

        #super(TransformerEmbedding, self).__init__(**kwargs)



    def build_embedding_model(self) -> None:
        if self.model_type == 'electra':
            bert_model = build_transformer_model(config_path=self.config_path,
                                                 checkpoint_path=self.checkpoint_path,
                                                 model=self.model_type,
                                                 application=self.bert_application,
                                                 keep_tokens=self.keep_tokens,  # 只保留keep_tokens中的字，精简原字表
                                                 )
        else:
            bert_model = build_transformer_model(config_path=self.config_path,
                                                 checkpoint_path=self.checkpoint_path,
                                                 model=self.model_type,
                                                 application=self.bert_application,
                                                 keep_tokens=self.keep_tokens,  # 只保留keep_tokens中的字，精简原字表
                                                 with_pool = self.with_pool
                                                 )
        self.embed_model = bert_model
        self.embedding_size = bert_model.output.shape[-1]



