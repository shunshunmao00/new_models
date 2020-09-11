# -*- coding: utf-8 -*-
import io
import base64
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
