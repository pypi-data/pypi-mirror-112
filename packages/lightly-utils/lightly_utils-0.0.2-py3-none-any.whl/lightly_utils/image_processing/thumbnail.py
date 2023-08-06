"""Create Thumbnail of Image"""

# Copyright (c) 2021. Lightly AG and its affiliates.
# All Rights Reserved

import io
from PIL import Image


class Thumbnail:
    """Thumbnail class for PIL image.

    Attributes:
        thumbnail:
            PIL image representing the thumbnail of the input image.

    Examples:
        >>> with Image.open('my-image.jpg', 'r') as image:
        >>>     thumbnail = Thumbnail(image)
        >>>     thumbnail_bytes = thumbnail.to_bytes() # use this to send

    """

    RESAMPLE = Image.LANCZOS
    SIZE_FOR_LIGHTLY: int = 128

    def __init__(self, image: Image):

        self.thumbnail = image.copy()
        self.thumbnail.thumbnail(
            (
                Thumbnail.SIZE_FOR_LIGHTLY,
                Thumbnail.SIZE_FOR_LIGHTLY
            ),
            Thumbnail.RESAMPLE
        )

    def to_bytes(self, ext: str = 'webp', quality: int = 90):
        """Returns the thumbnail as a bytes array.

        Args:
            ext:
                Extension with which to save the thumbnail.
            quality:
                Quality at which to save the thumbnail.

        """
        bytes_io = io.BytesIO()
        if quality is not None:
            self.thumbnail.save(bytes_io, format=ext, quality=quality)
        else:
            subsampling = -1 if ext.lower() in ['jpg', 'jpeg'] else 0
            self.thumbnail.save(
                bytes_io, format=ext, quality=100, subsampling=subsampling
            )
        bytes_io.seek(0)
        return bytes_io
