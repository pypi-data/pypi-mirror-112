"""Convenience functions to access and mange registered models"""
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





