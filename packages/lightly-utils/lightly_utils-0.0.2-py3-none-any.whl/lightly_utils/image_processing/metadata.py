"""Extract metadata from image"""

# Copyright (c) 2021. Lightly AG and its affiliates.
# All Rights Reserved

import io
from PIL import Image, ImageFilter

import numpy as np

from lightly_utils.image_processing._data import _DataObject


MAX_PIXEL_VALUE = 255.


def _pixel_mean(np_img: np.ndarray):
    """Return mean of each channel.
    """
    return np_img.mean(axis=(0, 1))


def _pixel_std(np_img: np.ndarray):
    """Return standard deviation of each channel.
    """
    return np_img.std(axis=(0, 1))


def _sum_of_values(np_img: np.ndarray):
    """Return the sum of the pixel values of each channel.
    """
    return np_img.sum(axis=(0, 1))


def _sum_of_squares(np_img: np.ndarray):
    """Return the sum of the squared pixel values of each channel.
    """
    return (np_img ** 2).sum(axis=(0, 1))


def _shape(np_img: np.ndarray):
    """Shape of the image as np.ndarray.
    """
    return np_img.shape


def _signal_to_noise_ratio(img: Image, axis: int = None, ddof: int = 0):
    """Calculate the signal to noise ratio of the image.
    """
    np_img = np.asanyarray(img)
    mean = np_img.mean(axis=axis)
    std = np_img.std(axis=axis, ddof=ddof)
    return float(np.where(std == 0., 0, mean / std))


def _sharpness(img: Image):
    """Calculate the sharpness of the image using a Laplacian Kernel.
    """
    img_bw = img.convert('L')
    filtered = img_bw.filter(
        ImageFilter.Kernel(
            (3, 3),
            # Laplacian Kernel:
            (-1, -1, -1, -1, 8, -1, -1, -1, -1),
            1,
            0,
        )
    )
    return np.std(filtered)


def _size_in_bytes(img: Image):
    """Return the size of the image in bytes.
    """
    img_file = io.BytesIO()
    img.save(img_file, format='png')
    return img_file.tell()


def _is_corrupted(img: Image):
    """Tries to load the image to see if it's corrupted.
    """
    try:
        img.load()
        return False, ''
    except Exception as e:
        return True, str(e)


class Metadata(_DataObject):
    """Metadata class for a PIL image.

    The `to_dict` function allows to get the data as a serializable dictionary.

    Attributes:
        mean:
            Mean of the pixel values of the image.
        std:
            Standard deviation of the pixel values of the image.
        sumOfValues:
            Sum of the pixel values of the image.
        sumOfSquares:
            Sum of the squared pixel values of the image.
        shape:
            Shape of the image.
        snr:
            Signal to noise ratio of the image.
        sharpness:
            Sharpness of the image.
        sizeInBytes:
            Size of the image in bytes.

    Examples:
        >>> with Image.open('my-image.jpg', 'r') as image:
        >>>     metadata = Metadata(image)
        >>>     metadata_dict = metadata.to_dict() # use this to send as json

    """

    def __init__(self, image: Image):

        # check if the file is corrupted
        self.is_corrupted, self.corruption = _is_corrupted(image)
        if self.is_corrupted:
            return

        # create a numpy version of the image
        numpy_image = np.array(image) / MAX_PIXEL_VALUE

        # Check the image dimensions
        number_image_dimensions = len(numpy_image.shape)
        if number_image_dimensions == 3:
            pass
        elif number_image_dimensions == 2:
            numpy_image = numpy_image[:,:,np.newaxis]
        else:
            raise ValueError(f"Image must have 2 or 3 dimensions, but has {number_image_dimensions}")

        # calculate metadata
        self.mean = _pixel_mean(numpy_image).tolist()
        self.std = _pixel_std(numpy_image).tolist()
        self.sumOfValues = _sum_of_values(numpy_image).tolist()
        self.sumOfSquares = _sum_of_squares(numpy_image).tolist()
        self.shape = _shape(numpy_image)
        self.snr = _signal_to_noise_ratio(image)
        self.sharpness = _sharpness(image)
        self.sizeInBytes = _size_in_bytes(image)
