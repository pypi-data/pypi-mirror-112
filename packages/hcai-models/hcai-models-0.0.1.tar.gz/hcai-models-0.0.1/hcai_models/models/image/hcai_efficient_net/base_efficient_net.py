from tensorflow.keras.applications.efficientnet import preprocess_input
from hcai_models.core.abstract_image_model import ImageModel
from hcai_models.core.keras_model import KerasModel
from tensorflow import keras
from tensorflow.keras.models import Model
from tensorflow.keras.applications.efficientnet import EfficientNetB7 as KerasEfficientNetB7
from tensorflow.keras.layers import Dense


DENSE_KERNEL_INITIALIZER = {
        'class_name': 'VarianceScaling',
        'config': {
            'scale': 1. / 3.,
            'mode': 'fan_out',
            'distribution': 'uniform'
        }
    }


class EfficientNet(ImageModel, KerasModel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def get_preprocess_input(self):
        """
        Efficientnet does not need any preprocessing since the preprocessing happens is included in the layers of the network.
        :return:
        """
        return preprocess_input


    def preprocess_input(self, ds):
        """

        :param ds:
        :return:
        """
        return ds

    def _efficient_net_model(self, base_model):

        if self.include_top:
            return base_model

        inputs = keras.Input(self.input_shape)
        x = base_model(inputs)
        pred = Dense(self.output_shape,
                  activation=self.output_activation_function,
                  kernel_initializer=DENSE_KERNEL_INITIALIZER,
                  name='predictions')(x)

        model = Model(inputs=inputs, outputs=pred)
        return model
