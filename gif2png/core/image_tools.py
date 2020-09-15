# -*- coding: utf-8 -*-
import io
import base64
import re
from PIL import Image, ExifTags


def get_img_from_bytes(img_bytes):
    image = Image.open(io.BytesIO(img_bytes))

    # 自动按拍摄时相机的重心旋转图像
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = dict(image._getexif().items())
        if exif[orientation] == 3:
            image = image.rotate(180, expand=True)
        elif exif[orientation] == 6:
            image = image.rotate(270, expand=True)
        elif exif[orientation] == 8:
            image = image.rotate(90, expand=True)
    except:
        pass

    return image


def get_img_from_base64(img_base64):
    return get_img_from_bytes(base64.b64decode(img_base64.encode()))


def get_base64_from_file(path):
    with open(path, 'rb') as file:
        return str(base64.b64encode(file.read()), encoding='utf-8')
    
    
def get_bytes_from_file(path):
    with open(path, 'rb') as file:
        return file.read()
    
    
def get_bytes_from_base64(img_base64):
    return base64.b64decode(img_base64.encode())

def image_to_url(img):
    output_buffer = io.BytesIO()
    img.save(output_buffer, format='PNG')
    return 'data:image/png;base64,' + str(base64.b64encode(output_buffer.getvalue()), encoding='utf-8')

def url_to_img(img_url):
    img_base64 = re.sub('^data:image/.+;base64,', '', img_url)
    return Image.open(io.BytesIO(base64.b64decode(img_base64.encode())))
