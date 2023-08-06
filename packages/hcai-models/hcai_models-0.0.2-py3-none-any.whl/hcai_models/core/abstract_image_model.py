from hcai_models.core.abstract_model import Model


class ImageModel(Model):
    """
    Abstract base class for image models.
    Specifies specific functionality of image models and ensures compatibility with the interface for external calls.
    """

    in_width = 300
    in_height = 300
    in_depth = 3

    def __init__(self, *args, in_width=None, in_height=None, in_depth=None, **kwargs):
        if not 'input_shape' in kwargs.keys():
            if not in_width:
                print('Warning! No image width has been set. Using default of {}'.format(self.in_width))
            if not in_height:
                print('Warning! No image width has been set. Using default of {}'.format(self.in_height))
            if not in_depth:
                print('Warning! No image width has been set. Using default of {}'.format(self.in_depth))

            input_shape = (self.in_width, self.in_height, self.in_depth)
        super().__init__(*args, **kwargs)
