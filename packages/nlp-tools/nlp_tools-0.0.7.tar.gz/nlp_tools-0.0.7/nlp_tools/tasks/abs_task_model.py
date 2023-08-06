import json
import os
import pathlib
from abc import ABC, abstractmethod
from typing import Dict, Any, TYPE_CHECKING, Union

import tensorflow as tf

import nlp_tools
from nlp_tools.embeddings import ABCEmbedding
from nlp_tools.logger import logger
from nlp_tools.utils import load_data_object
from nlp_tools.tokenizer.base_tokenizer import ABCTokenizer


class ABCTaskModel(ABC):

    def __init__(self) -> None:
        self.tf_model: tf.keras.Model = None
        self.embedding: ABCEmbedding = None
        self.hyper_parameters: Dict[str, Any]
        self.max_sequence_length: int = None
        self.text_processor=None
        self.label_processor=None
        self.model_node_names:dict
        self.hyper_parameters = {}

    def to_dict(self) -> Dict[str, Any]:
        model_json_str = self.tf_model.to_json()

        return {
            'tf_version': tf.__version__,
            'nlp_tools_version':nlp_tools.__version__,
            '__class_name__': self.__class__.__name__,
            '__module__': self.__class__.__module__,
            'config': {
                'hyper_parameters': self.hyper_parameters,  # type: ignore
                'max_sequence_length': self.max_sequence_length  # type: ignore
            },
            'embedding': self.embedding.to_dict(),  # type: ignore
            'text_processor': self.text_processor.to_dict(),
            'label_processor': self.label_processor.to_dict(),
            'tf_model': json.loads(model_json_str),
            'model_node_names':self.model_node_names
        }

    @classmethod
    def default_hyper_parameters(cls) -> Dict[str, Dict[str, Any]]:
        """
        The default hyper parameters of the model dict, **all models must implement this function.**

        You could easily change model's hyper-parameters.

        For example, change the LSTM unit in BiLSTM_Model from 128 to 32.

            >>> from nlp_tools.tasks.classification import BiLSTM_Model
            >>> hyper = BiLSTM_Model.default_hyper_parameters()
            >>> print(hyper)
            {'layer_bi_lstm': {'units': 128, 'return_sequences': False}, 'layer_output': {}}
            >>> hyper['layer_bi_lstm']['units'] = 32
            >>> model = BiLSTM_Model(hyper_parameters=hyper)

        Returns:
            hyper params dict
        """
        raise NotImplementedError

    def save(self, model_path: str) -> str:
        pathlib.Path(model_path).mkdir(exist_ok=True, parents=True)
        model_path = os.path.abspath(model_path)

        # 将inputs和outputs 节点的name保存下来
        self.model_node_names = self.get_input_and_output_names_from_model()

        with open(os.path.join(model_path,'model_config.json'), 'w',encoding='utf-8') as f:
            f.write(json.dumps(self.to_dict(),indent=2,ensure_ascii=False))
            f.close()

        tf.keras.models.save_model(self.tf_model,os.path.join(model_path,'model_weights'))
        logger.info('model saved to {}'.format(os.path.abspath(model_path)))
        return model_path

    @classmethod
    def load_model(cls,model_path:str,**kwargs):
        model_config_path = os.path.join(model_path,'model_config.json')
        model_config = json.loads(open(model_config_path,'r',encoding='utf-8').read())

        model_config['config']['text_processor'] = load_data_object(model_config['text_processor'])
        model_config['config']['label_processor'] = load_data_object(model_config['label_processor'])
        model_config['config']['embedding'] = load_data_object(model_config['embedding'])
        model = load_data_object(model_config)
        model.tf_model = tf.keras.models.load_model(os.path.join(model_path,'model_weights'),custom_objects=nlp_tools.custom_objects)
        return model

    @abstractmethod
    def build_model(self,
                    x_data: Any,
                    y_data: Any) -> None:
        raise NotImplementedError


    def get_input_and_output_names_from_model(self):
        '''从模型中获取到输入和输出的node 的名称'''
        input_names = [node.op.name for node in self.tf_model.inputs]
        output_names = [node.op.name for node in self.tf_model.outputs]
        node_names_dict = {}
        node_names_dict['inputs'] = input_names
        node_names_dict['outputs'] = output_names
        return node_names_dict