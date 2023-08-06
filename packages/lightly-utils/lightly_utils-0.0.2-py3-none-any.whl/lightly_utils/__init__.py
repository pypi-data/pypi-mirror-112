"""Lightly Utils"""


# Copyright (c) 2021. Lightly AG and its affiliates.
# All Rights Reserved

__name__ = 'lightly_utils'
__version__ = '0.0.2'


try:
    # See (https://github.com/PyTorchLightning/pytorch-lightning)
    # This variable is injected in the __builtins__ by the build
    # process. It used to enable importing subpackages of skimage when
    # the binaries are not built
    __LIGHTLY_UTILS_SETUP__
except NameError:
    __LIGHTLY_UTILS_SETUP__ = False


if __LIGHTLY_UTILS_SETUP__:
    # set up lightly_utils
    msg = f'Partial import of {__name__}=={__version__} during build process.'
    print(msg)
else:
    from lightly_utils import image_processing
