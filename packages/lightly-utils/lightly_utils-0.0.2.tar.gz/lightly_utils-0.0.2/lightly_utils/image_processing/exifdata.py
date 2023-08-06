"""Extract exifdata from image"""

# Copyright (c) 2021. Lightly AG and its affiliates.
# All Rights Reserved

import warnings
from PIL import Image, ExifTags, TiffImagePlugin

from lightly_utils.image_processing._data import _DataObject


def _parse_GPSInfo(data):
    """TODO: implement.

    """
    return None


def _parse_exif_data(key, data):
    """Takes exif data and returns it in a serializable format.

    Args:
        key:
            Exif tag defined by PIL.
        data:
            Exif data.

    Returns:
        Exif data in a serializable format.

    """
    if key == 'GPSInfo':
        # gps information needs to be parsed separately
        return _parse_GPSInfo(data)

    elif isinstance(data, dict):
        # recursively parse dictionaries
        new_data = {}
        for key, item in data.items():
            new_data[key] = _parse_exif_data(key, item)
        return new_data
    elif isinstance(data, tuple):
        # recursively parse tuples
        new_data = ()
        for d in data:
            new_data += (_parse_exif_data(key, d),)
        return new_data
    elif isinstance(data, bytes):
        # convert bytes to text
        try:
            return data.decode('utf-8')
        except Exception:
            return ''
    elif isinstance(data, int) or isinstance(data, str):
        # return for ints and strings
        return data
    elif isinstance(data, float):
        # return for floats as well
        return data
    elif isinstance(data, TiffImagePlugin.IFDRational):
        # convert rational to float
        numerator, denominator = data.limit_rational(1e6)
        return numerator / float(denominator) if denominator > 0 else 'nan'
    else:
        # haven't had this before, raise a warning an return None
        warnings.warn(
            f'Unexpected type: Exif {key} is of unexpected type: {type(data)}'
        )


class Exifdata(_DataObject):
    """Exif class for a PIL image. Extracts all available exifdata.

    The `to_dict` function allows to get the data as a serializable dictionary.

    TODO: Does not work for GPS data yet.

    Attributes:
        All exifdata tags in the image.

    Examples:
        >>> with Image.open('my-image.jpg', 'r') as image:
        >>>     exifdata = Exifdata(image)
        >>>     exifdata_dict = exifdata.to_dict() # use this to send it as json

    """

    def __init__(self, image: Image):

        exifdata = image.getexif()
        for tag_id in exifdata:
            # get human readable tag name
            tag = ExifTags.TAGS.get(tag_id, tag_id)
            data = exifdata.get(tag_id)
            # set attribute of object to exif data
            setattr(self, tag, _parse_exif_data(tag, data))
