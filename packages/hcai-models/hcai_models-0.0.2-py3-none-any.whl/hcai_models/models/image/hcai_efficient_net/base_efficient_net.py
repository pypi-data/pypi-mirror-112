from tensorflow.keras.applications.efficientnet import preprocess_input
from hcai_models.core.abstract_image_model import ImageModel
from hcai_models.core.keras_model import KerasModel
from tensorflow import keras
from tensorflow.keras.models import Model
from tensorflow.keras.applications.efficientnet import EfficientNetB7 as KerasEfficientNetB7
from tensorflow.keras.layers import Dense

_DESCRIPTION = """
Convolutional Neural Networks (ConvNets) are commonly developed at a fixed resource budget, and then scaled up for better accuracy if more resources are available. 
In this paper, we systematically study model scaling and identify that carefully balancing network depth, width, and resolution can lead to better performance. 
Based on this observation, we propose a new scaling method that uniformly scales all dimensions of depth/width/resolution using a simple yet highly effective compound coefficient. We demonstrate the effectiveness of this method on scaling up MobileNets and ResNet. 
To go even further, we use neural architecture search to design a new baseline network and scale it up to obtain a family of models, called EfficientNets, which achieve much better accuracy and efficiency than previous ConvNets.
"""

_CITATION = """
@inproceedings{tan2019efficientnet,
  title={Efficientnet: Rethinking model scaling for convolutional neural networks},
  author={Tan, Mingxing and Le, Quoc},
  booktitle={International Conference on Machine Learning},
  pages={6105--6114},
  year={2019},
  organization={PMLR}
}
"""

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
