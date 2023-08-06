"""Accessing registered datasets"""
from hcai_models.core import registered_model as register

def build_model(name, builder_kwargs):
    """
    Returns the builder class of the model for the given name if registered.
    If the model has not been registered a module not found exception is raised.
    """

    # If the model is registered as abstract model, not all abstract functions have been implemented.
    if name in register._ABSTRACT_MODEL_REGISTRY.keys():
        try:
            register._ABSTRACT_MODEL_REGISTRY[name]()
        except Exception as ex:
            print('Error instantiating model: {}'.format(ex))
            exit()

    if not name in register._MODEL_REGISTRY.keys():
        raise ModuleNotFoundError('No model with name {} has been imported.'.format(name))
    return register._MODEL_REGISTRY[name](**builder_kwargs)


def load(name=None,
         builder_kwargs=None):
    """
    Convenience function to load a model
    :param name: The identifier of the model. Should be equal to the class name of the implemented model.
    :param builder_kwargs: Keyword arguments that specify the configuration of the model.
    :param kwargs:
    :return: Instance of the model.
    """
    if builder_kwargs is None:
        builder_kwargs = {}

    model = build_model(name, builder_kwargs)
    return model


