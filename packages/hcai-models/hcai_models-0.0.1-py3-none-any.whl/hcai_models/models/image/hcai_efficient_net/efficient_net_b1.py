from tensorflow.keras.applications.efficientnet import EfficientNetB1 as KerasEfficientNetB1
from hcai_models.models.image.hcai_efficient_net.base_efficient_net import EfficientNet

class EfficientNetB1(EfficientNet):

    def _model(self):
        base_model = KerasEfficientNetB1(input_shape=self.input_shape,
                                         include_top=self.include_top,
                                         weights=self.weights)
        return self._efficient_net_model(base_model)

    def _info(self):
        return ''
