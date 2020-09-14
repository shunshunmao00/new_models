# -*- coding: utf-8 -*-
import random
import numpy as np
import cv2

from core.model_core import ModelCore
from core.util import image_tools
from PIL import Image, ExifTags
import io
import base64
import matplotlib.pyplot as plt

class TestDev(object):
    def __init__(self):
        self.painter = ModelCore()

    def photo2painter_bin(self, img_bin):
        # painter.do_paint('../test_image/1.png')
        pass

    def photo2painter_base64(self, img_base64, ws_topic=None):
        # TODO: add more arguments
        img = image_tools.get_bytes_from_base64(img_base64)
        img_array = np.frombuffer(img, np.uint8)
        print(type(img_array), img_array.shape, img_array)
        img_cv = cv2.imdecode(img_array, cv2.COLOR_RGBA2RGB)
        print(type(img_cv), img_cv.shape, img_cv)
        self.painter.do_paint(img_cv)


    def gen_test_img_bin(self):
        return image_tools.get_bytes_from_file('core/image_data/{}.png'.format(random.randint(1, 7)))

    def gen_test_img_base64(self):
        # return image_tools.get_base64_from_file('core/image_data/{}.png'.format(random.randint(1, 7)))
        return image_tools.get_base64_from_file('core/image_data/1.png')

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

def show_img_base64(img_base64):
    return get_img_from_bytes(base64.b64decode(img_base64.encode()))


# TODO: use run model server to replace it.
if __name__ == "__main__":

    model_core = TestDev()
    img_base64 = model_core.gen_test_img_base64()

    model_core.photo2painter_base64(img_base64)
    img = image_tools.get_bytes_from_base64(img_base64)


    # img_bin = model_core.gen_test_img_bin()
    # print(type(img), type(img_bin))

    # import cv2
    #
    # img_b64 = '/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/2wBDAQkJCQwLDBgNDRgyIRwhMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjL/wAARCACAAIADASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD3REUIOBS7V9KB90UZpAGB6UYHpRmgGgBwA9KguYUdBlQTmpXkWNSzsFUDJJOMVxWvfEGy03cIzHsXrJIcA/QVNx2OpFtGOqCl+zxf3BXCxfF7wsbKOWe7ZZmHzRJGzEf0qzZ/FbwrePsS8lT3eI/0q0nYR3dtGihgqgc0+eJJEwyg81iQ+JdKZIZor2KVJ3EabGyS307fjW2H3c0guQfY4v7gpDZRf3BVnNFAFQ2UX9wULZw5z5Yq1mloAg8lAOFFQXFvG8ZBFWmOKhkOUNICbPApCaTPAopgLVS91Wz06MvdTrGFGTk9KW/vYtO0+e8ncJHEhZmPQYrwybVdQ8b6lLLFuWxVyIwe/wDtH3pqPMUja8b/ABH8+GW10rPl4O6dhjP0FeNSR6rrE3nzmWXPRnOB+Fe52Xw9sbaz3aiTPcSDIA4CD+prJ1PwSYlY2dwCeyyD+oq01H4UTJq55QuiSgZlkRB7c09YreyyysXfHXtW9qfh/WLckyxb1/6ZtmueuoZonCSRshPOGGKiU5dRqxYttWu7cq8MhRlPWvYvDXxQW70GSK6uYoNTgjJXzR8kpA4P+IrxNU2Jg0lYuTY+VH0F4X+Luk6uUttUAsLo8bif3bH69vxr0NZVdA6MGUjIIOQa+Oa7zwR8Sb/w7JHZXrtcaYTjDctF7r7e1OM+4NH0WrZNKWqhp1/BqFnHdW0qywygMjqeCKsl60JHO2RVZn+U09nqrK2M+4oA0Owooz8ooFAHAfFlr250G10qyO0Xc3798/dRef54/KqvhLSba1js7SFf3MS7ie7HuTVjxrMZtZjTPypFx+ZqhoOvWOnSzmeYsQu1UQZ5rVL3dBqSjqzs7k5LOaxLoM5IQZY9Kry+LoZvlis5GHu2M1GutzYymnojHu0hpqLMXNGVrmi3X2B5kmYyg8qgHArzDXNOdEFyJpJGQ/MH5IFeoXuo6nJIVJhQdtuaxbyC5licvDDKCCDhOa6Yxhy2kiFOz0PLhIXHSitafSy+97dMEdU/wrLdGVirAgjqDXm1Y2lorHTCSktBlFFFZFnrHwe8SNDLPos8hKOd8QJ6HvivYvMr5L0/VZdI1O3u7diJYnDDBr2rRvinZahMIrq3a3bHUHIraF7GcmrnozPUE7fus8cVUh1K2uYhLFOjxnoQaq3+qwx2rbGDN7VdibnUE8CmyvsjY/lS5yq1VvX2oi+pzSKPN/iS0ts1tLD1mUoSOox/+uuZ0KyO0tLkbua9P8R6Adbt4mjkVJYSSpboQetZmneH4rRQ07CRh2HSuiL90wndsoWFk9w223j2r3dq47xD42j0vU57GztxPJAxR5JCQNw6gCvVrQAb2AAGcDFZ+oeF9A1CZrq+023eU8s+MFvrjrVISSPIYvHeo3dxHH/ZsEpJxtj3ZP616XbWcTwRyPE8bsoJQtkqfSpYtO02yk/0Cxgt1HAKIAT+PWpyQoyelaJCdjhdZtY7bUZBGoUE5wKw7zTobxSSNsnZhXQa8+/VZD2wMVQhgkuJNka5NZyinoxJ2d0cedGv3vFtoLaWaVj8ojUtmrs3gvxLbpvk0W82/wCzHu/lXo3hS9/sHXHNzDvjZNjsvOzvmvV7S5tb2ISW8ySKf7prllQsbxrJ6dT49kglhu3jnjeN0bDK6kEH6V0GgL5uu2i4ypf5h7d6978UfDvRvEU5vJWNrcY+eRQCG+oNYWneB/DekOwSeae4PHnDov0HSrSJe5zU0dzpE3nWbs0BPKdcVv2z3F7ZGQW8i5HIYVcvNN/sa4gug4uLMtjd3HsRXTWsttPa+ZBsKsO1MZPa+IbKRVja4jL+zCsXXvE8CXTQRzhfLGCcc5ry9Nxfg8561IzSC4be5YE855qoRV9SJVHY9E0PW31Hz0DuQhHLHkiqeuXt5Z3eIZ2CSLkA84rH0KRtPu1uQ4eJhhlXuKj8a+JbeFrdrSLfIMjLiuiNm7Izd9zp9Cv7p7Z2vFAT+FsYJqe5uXnOOidhXnWm+Mr1PLWdY3iJ5AXB/Cu3NyhQFRnIzVOFmCZIWVBknFU55i4IHC0juXOSaic9qaQzntZQm9TA5ZRWpp9kLeELj525Y1XvDGuqWzSkBAOpqLUvENvAz2trIr3BXkj+Ef41FlzETbS0J7meCF33uq5/Ols77aDNaXJUr1MbYNcqZGdtzEknuak0tidYCx/dbIcDoRitU+h51Sk0nK+pvXHjHVrg+W1yXhHRW71Nb+KigG+2yf8AZaqUuix7spNtHowpEsbaLG+XefYUOnHsEcTJLRlrUPE9xcWhTyCtvuBIDZJNRS6k1jaCWCSRSw5ANEyQzRGMYxSXFsJLPZheB1rCdNJ6HVRxEpLUoWq7pfpSPzI31ot5Nkn14ppOWNYo6WXdPuzC/luf3bH8qTW9Lj1EAF9jLyrDmqgq7Bc7gsbnkcA1cHZ3C+liXTPCcVr5U1xN5uACFC4FdEaceIY/90VA8nYV03b3Cw5mx9ai60UtAzD1v/XRf7tedLHqC6jLIIZDLvPRSc16NrX/AB8R/wC7VKG4EKMmfmbpWTV5EVJOMW0jKs7DUrsAzbbdO/8AerZijtdGh/dgtK38R6mnRzVl38xe6YE8DgVpdJHnvmqSs9i2t3JcTEu2fQVNv4rIhm2SAnp3rQD8daEwlCxKW5q/DLmPB5BFZTyAAk1ds3E1tGw5GKmTNKUepmDODUUVz2k/OrRiZWKkEGrNp4bnurYTCRVLdFNcyO+xUEsf98UyS4VQCpyR6U+70i7sT+9j+X+8vIqtHGXYLTuFjq9P1BrqJYpDiRR+Yq5Xnl9rkllrdja2zYZpF8w+xPSvQ85Ga6ISvoO1kFOFMzSCaPdt3DNWIyNZ4uUz/crhL7xHBHqJMW51j+XI6H1rr/GEpgsZ5BwRCQPx4ryLNclabi7I3pUlNPmPRLDWrW9A8uTD/wB1uDTr3/WeYOh6154jsjBlYgjuK2LTxDcwqEmxMn+11ojWvpIxngrO8Dog9SpdvGMA8e9NtfFnh4whLjSJFbHLK2anOt+EZxhorqLPpmp9vbow+qN7mde6jJIvlqwx3xWjo2tw21oIJw2VzgjoRUkMXg66UsuoyRYGcOcfzFZFsdLvNVa2tpJBFztdiDmp9um7l/VrRsew3Gn6Rqqr5UkazY6qefyqW30ea3t1jBD7eMjvXjX2m4jl8yOV1YHgg13ejfEqz0/SB/a8jtNHwCq5LCs4VLuxvOkkrnVtasRtkiyPQiuQ8a6bDp+hXV5aFYpgvzDOBjvj3qWP4vaTqTNFbxzQjpukXk1xHj/xRBfWi2tvMzKeX9zW1zHlMTw4r6z4xtpJORv8w/RRn+levs56KpY+grh/hrpMTW5vywMs3yL/ALIHWvSoLNnIVQAM1vStGN2Z1G72RjmC5nPzEIvpWjpmjB5g7/MoPNblvpcKANIwY+lXNsca4UgAelEq/SIo0ne8jjPH9pajw7MrRqrMAqkDvmvA5I2ikZGGCDivZPiRqiyXNrZI/wAvLN9eMV5tqNisy+ahG8dfeuacW9TppzUXYwxU0EMlxMsUSF3Y4AHeoyhU4NXtGvv7M1OK6Kbwh5FZHSR3dlcWFwYLmMxyAAkGoRV7WtUfV9Tku2XbkAAegFUCCVIHWmSypdXG792p4HWix3CbepIx6Ui2bM3zHirscaxLhRVEWbep/9k='
    # img = image_tools.get_bytes_from_base64(img_b64)
    # img_array = np.frombuffer(img, np.uint8)
    # img_cv = cv2.imdecode(img_array, cv2.COLOR_RGBA2BGR)
    # cv2.namedWindow('input_image', cv2.WINDOW_AUTOSIZE)
    # cv2.imshow('input_image', img_cv)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # img_b = show_img_base64(img_b64)
    # plt.figure("dog")
    # plt.imshow(img_b)
    # plt.show()




