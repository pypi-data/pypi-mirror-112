import unittest
import tempfile
from PIL import Image

from lightly_utils.image_processing import Thumbnail


class TestThumbnail(unittest.TestCase):

    def test_thumbnail(self):

        for w in [100, 200]:
            for h in [100, 200]:
                image = Image.new('RGB', (w, h))

                thumbnail = Thumbnail(image)

                if w > Thumbnail.SIZE_FOR_LIGHTLY and h > Thumbnail.SIZE_FOR_LIGHTLY:
                    # width and height are larger than thumbnail size
                    self.assertEqual(thumbnail.thumbnail.size[0], Thumbnail.SIZE_FOR_LIGHTLY)
                    self.assertEqual(thumbnail.thumbnail.size[1], Thumbnail.SIZE_FOR_LIGHTLY)
                elif h > Thumbnail.SIZE_FOR_LIGHTLY:
                    # only height is larger than thumbnail size
                    self.assertEqual(thumbnail.thumbnail.size[1], Thumbnail.SIZE_FOR_LIGHTLY)
                elif w > Thumbnail.SIZE_FOR_LIGHTLY:
                    # only width is larger than thumbnail size
                    self.assertEqual(thumbnail.thumbnail.size[0], Thumbnail.SIZE_FOR_LIGHTLY)
                else:
                    self.assertEqual(thumbnail.thumbnail.size[0], w)
                    self.assertEqual(thumbnail.thumbnail.size[1], h)

                thumbnail = thumbnail.to_bytes()
