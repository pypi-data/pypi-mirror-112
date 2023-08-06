import json
import unittest
import tempfile
from typing import List

from PIL import Image
import numpy as np

from lightly_utils.image_processing import Metadata


def is_jsonable(x):
    try:
        json.dumps(x)
        return True
    except Exception as e:
        return False


class TestMetadata(unittest.TestCase):

    def test_metadata_corrupted(self):
        image = None
        metadata = Metadata(image)
        metadata = metadata.to_dict()

        self.assertTrue(metadata['is_corrupted'])
        self.assertNotEqual(metadata['corruption'], 'e')
        for key, item in metadata.items():
            self.assertTrue(is_jsonable(item))


    def test_metadata(self):
        image_modes = ['1', 'L', 'P', 'RGB']
        for image_mode in image_modes:
            with self.subTest(f'image mode: {image_mode}'):
                image = Image.new(image_mode, (100, 100))
                metadata = Metadata(image)
                metadata = metadata.to_dict()

                self.assertFalse(metadata['is_corrupted'])
                for key, item in metadata.items():
                    self.assertTrue(is_jsonable(item))
                for key in ['mean', 'std', 'sumOfValues', 'sumOfSquares']:
                    value = metadata[key]
                    self.assertIsInstance(value, List)

    def test_metadata_nonzero(self):
        arr = np.random.randint(0, 255, (100, 100, 3))
        image = Image.fromarray(arr, 'RGB')
        metadata = Metadata(image)
        metadata = metadata.to_dict()

        self.assertFalse(metadata['is_corrupted'])
        for key, item in metadata.items():
            self.assertTrue(is_jsonable(item))