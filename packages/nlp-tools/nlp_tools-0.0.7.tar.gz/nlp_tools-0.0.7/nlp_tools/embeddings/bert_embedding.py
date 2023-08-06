import os
from typing import Dict,Any

from nlp_tools.embeddings.transformer_embedding import TransformerEmbedding

class BertEmbedding(TransformerEmbedding):
    """
    BertEmbedding is a simple wrapped class of TransformerEmbedding.
    If you need load other kind of transformer based language model, please use the TransformerEmbedding.
    """

    def to_dict(self) -> Dict[str, Any]:
        info_dic = super(BertEmbedding, self).to_dict()
        return info_dic

    def __init__(self,
                 model_folder: str = None,
                 model_type='bert',
                 **kwargs: Any):
        """

        Args:
            model_folder: path of checkpoint folder.
            kwargs: additional params
        """
        if model_folder:
            if model_type == 'electra':
                config_path = os.path.join(model_folder, 'bert_config.json')
                checkpoint_path = os.path.join(model_folder, 'electra_base')
            else:
                config_path = os.path.join(model_folder, 'bert_config.json')
                checkpoint_path = os.path.join(model_folder, 'bert_model.ckpt')
            kwargs['checkpoint_path'] = checkpoint_path
            kwargs['config_path'] = config_path
        kwargs['model_type'] = model_type
        super(BertEmbedding, self).__init__(**kwargs)



