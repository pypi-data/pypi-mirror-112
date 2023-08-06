# lightly_utils

## Install

The `lightly_utils` package can be installed from source, jump to this directory and run
```bash
make install
```

To install it via PIP simply use
```
pip install lightly_utils
```

## Distribute

To release a new version, first make sure that the version number in `lightly_utils.__init__.py` is incremented. Then, use
```
make dist
```
to get the wheel files. This will create a directory `dist/` which should look like this:
```
dist/
L lightly_utils-X.X.X-py3-none-any.whl
L lightly_utils-0.0.1.tar.gz
```

Make sure you have [twine](https://pypi.org/project/twine/) installed for the next step. Run the following command to release the package:
```
python -m twine upload dist/*
```

Ask one of your colleagues at Lightly for credentials if you don't have any.

## Use

### image_processing

`lightly_utils` offers utilities to work with images. In particular, you can easily extract metadata and exifdata, and you can generate thumbnails.

```python
from PIL import Image
from lightly_utils import image_processing

with Image.open('my-image.jpg') as image:

    # get metadata, exifdata, and thumbnail objects
    metadata = image_processing.Metadata(image)
    exifdata = image_processing.Exifdata(image)
    thumbnail = image_processing.Thumbnail(image)

    # access the metadata as a dictionary
    metadata_dict = metadata.to_dict()

    # access the exifdata as a dictionary
    exifdata_dict = exifdata.to_dict()

    # access the thumbnail as bytes array
    thumbnail_bytes = thumbnail.to_bytes()
```

Head to `examples/` and run the `example.py` script to see what kind of information can be extracted.