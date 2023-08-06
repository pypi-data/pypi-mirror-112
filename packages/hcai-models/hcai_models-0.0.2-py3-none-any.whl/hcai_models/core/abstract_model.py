from abc import ABC, abstractmethod, abstractproperty
from hcai_models.core.ssi_compat import SSIModel, SSIBridgeModel
from hcai_models.core.registered_model import RegisteredModel

class Model(ABC, RegisteredModel):
    """
    Abstract base class for all models.
    Specifies general functionality of the models and ensures compatibility with the interface for external calls.
    """

    def __init__(self, *args, input_shape, output_shape, include_top=False, weights=None, output_activation_function='softmax', optimizer='adam', loss='mse', **kwargs):
        self.input_shape = input_shape
        self.include_top = include_top
        self.weights = weights
        self.output_shape = output_shape
        self.output_activation_function = output_activation_function
        self.optimizer = optimizer
        self.loss = loss
        self.model = self._build_model()
        self.info = self._info()

    def is_ssi_model(self):
        return issubclass(self.__class__, SSIModel)

    def is_ssi_bridge_model(self):
        return issubclass(self.__class__, SSIBridgeModel)

    @abstractmethod
    def preprocess_input(self, ds):
        """
        Preprocesses the input data. Only use for static preprocessing that should be repleciated once the model is fully trained (e.g input normalization)
        :return:
        """
        raise NotImplemented()

    @abstractmethod
    def compile(self, optimizer, loss, metrics):
        """
       Fixes the models training parameter: loss, metrics and optimizer
       :return:
       """
        raise NotImplemented()

    @abstractmethod
    def set_weights(self, weights):
        """
        Sets the weights of a model.
        :param weights: Dictionary in the form of layer_name : weights
        :return:
        """
        raise NotImplemented()

    @abstractmethod
    def load_weights(self, filepath):
        """
        Loads weights the weights of a model
        :return:
        """
        raise NotImplemented()

    @abstractmethod
    def fit(self, *args, **kwargs):
        """
        Fits the model on the provided data
        :return:
        """
        raise NotImplemented()

    # Private Methods
    @abstractmethod
    def _build_model(self):
        """
        Builds the model as specified by the set class parameters and set self.model
        :return:
        """
        raise NotImplemented()

    @abstractmethod
    def _info(self):
        """
        Returns additional information for the model
        :return:
        """
        raise NotImplemented()
