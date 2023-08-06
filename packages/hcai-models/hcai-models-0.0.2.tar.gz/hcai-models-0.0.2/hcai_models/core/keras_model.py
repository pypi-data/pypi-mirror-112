"""Class to forward the abstract functions required by the abstract_model class to the keras api.
Keras models can inherit the methods implemented by this class to avoid duplicating boilerplate code.
"""

from hcai_models.core.abstract_model import Model

class KerasModel(Model):

    def compile(self, optimizer, loss, metrics):
        """
        Fixes the models training parameter: loss, metrics and optimizer
        :return:
        """
        self.model.compile(optimizer=optimizer, loss=loss, metrics=metrics)

    def set_weights(self, weights):
        """
        Resets the weights of a model
        :return:
        """
        raise NotImplementedError()
        #TODO: Implement

    def load_weights(self, file_path):
        self.model.load_weights(
            file_path, by_name=False, skip_mismatch=False, options=None
        )

    def fit(self, *args, **kwargs):
        """
        Fixes the models training parameter: loss, metrics and optimizer
        :return:
        """
        self.model.fit(x=x, y=y, **kwargs)
