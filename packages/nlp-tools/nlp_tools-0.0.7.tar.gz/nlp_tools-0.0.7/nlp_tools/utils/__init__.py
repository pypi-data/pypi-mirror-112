import warnings
import tensorflow as tf
from typing import TYPE_CHECKING,Union
from tensorflow.keras.utils import CustomObjectScope

from nlp_tools import  custom_objects
from nlp_tools.utils.serialize import load_data_object
from nlp_tools.utils.data import get_list_subset
from nlp_tools.utils.data import unison_shuffled_copies
from nlp_tools.utils.multi_label import MultiLabelBinarizer



def custom_object_scope() -> CustomObjectScope:
    return tf.keras.utils.custom_object_scope(custom_objects)

