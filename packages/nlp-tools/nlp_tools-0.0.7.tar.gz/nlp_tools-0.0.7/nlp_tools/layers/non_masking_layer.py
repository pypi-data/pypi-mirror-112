from tensorflow.keras.layers import Layer
import nlp_tools

class NonMaskingLayer(Layer):
    def __init__(self,**kwargs):
        self.supports_masking = True
        super(NonMaskingLayer,self).__init__(**kwargs)

    def build(self, input_shape):
        pass

    def compute_mask(self, inputs, mask=None):
        return None
    def call(self,x,mask=None):
        return x
nlp_tools.custom_objects['NonMaskingLayer'] = NonMaskingLayer