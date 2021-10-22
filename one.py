from PIL import Image
from PIL.ExifTags import TAGS

def get_exif():
    ret = {}
    i = Image.open("life/702_i.JPG")
    info = i._getexif()
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        ret[decoded] = value
    print(ret)
    return ret

get_exif()

for tag in TAGS:
    print(tag)

