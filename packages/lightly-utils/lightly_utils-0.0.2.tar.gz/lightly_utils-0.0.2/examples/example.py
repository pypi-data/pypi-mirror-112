from PIL import Image
from lightly_utils import image_processing

with Image.open('example.jpg') as image:

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

print(30 * '-')
print('Metadata:')
for key, item in metadata_dict.items():
    print(f'{key:{30}}: {item}')
print(30 * '-')

print('Exifdata:')
for key, item in exifdata_dict.items():
    print(f'{key:{30}}: {item}')
print(30 * '-')