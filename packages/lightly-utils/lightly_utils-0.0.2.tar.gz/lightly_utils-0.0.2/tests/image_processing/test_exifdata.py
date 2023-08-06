import json
import unittest
import tempfile
from PIL import Image
import numpy as np

from lightly_utils.image_processing import Exifdata
from lightly_utils.image_processing.exifdata import _parse_exif_data


def is_jsonable(x):
    try:
        json.dumps(x)
        return True
    except Exception as e:
        return False


class TestExifdata(unittest.TestCase):

    def test_exifdata(self):
        image = Image.open('examples/example.jpg')
        exifdata = Exifdata(image)
        exifdata = exifdata.to_dict()
        image.close()

        exifdata_target = {'GPSInfo': None, 'ResolutionUnit': 2, 'ExifOffset': 256, 'Make': 'Canon', 'Model': 'Canon EOS 7D\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', 'Software': 'GIMP 2.8.0', 'Orientation': 1, 'DateTime': '2014:07:20 20:06:28', 'YCbCrPositioning': 1, 'YResolution': 350.0, 'Copyright': '\x00', 'XResolution': 350.0, 'Artist': '\x00'}
        for data_name, data_value in exifdata_target.items():
            self.assertEqual(exifdata[data_name], data_value)
            self.assertTrue(is_jsonable(exifdata[data_name]))

    def test_exifdata_tuples(self):

        a_tuple = (
            'hello',
            0.1,
            {
                'this': 'is',
                'a': 'dictionary',
                'b': 5,
            },
            ('more', 'tuples', 5, 2),
        )

        parsed_tuple = _parse_exif_data('tuple', a_tuple)
        self.assertTupleEqual(a_tuple, parsed_tuple)
