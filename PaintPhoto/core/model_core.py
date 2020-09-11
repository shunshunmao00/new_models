# -*- coding: utf-8 -*-
import random
import numpy as np
import cv2

from core.painter import Painter
from core.util import image_tools

class ModelCore(object):
    def __init__(self):
        self.painter = Painter()

    def photo2painter_bin(self, img_bin):
        # painter.do_paint('../test_image/1.png')
        pass

    def photo2painter_base64(self, img_base64):
        img = image_tools.get_bytes_from_base64(img_base64)
        img_array = np.frombuffer(img, np.uint8)
        img_cv = cv2.imdecode(img_array, cv2.COLOR_RGBA2BGR)
        self.painter.do_paint(img_cv)


    def gen_test_img_bin(self):
        return image_tools.get_bytes_from_file('core/image_data/{}.png'.format(random.randint(1, 7)))

    def gen_test_img_base64(self):
        # return image_tools.get_base64_from_file('core/image_data/{}.png'.format(random.randint(1, 7)))
        return image_tools.get_base64_from_file('image_data/{}.png'.format(random.randint(1, 7)))

# TODO: use run model server to replace it.
if __name__ == "__main__":
    model_core = ModelCore()
    img_base64 = model_core.gen_test_img_base64()

    model_core.photo2painter_base64(img_base64)
    img = image_tools.get_bytes_from_base64(img_base64)

    # img_bin = model_core.gen_test_img_bin()
    # print(type(img), type(img_bin))

    # import cv2
    # img_array = np.frombuffer(img, np.uint8)
    # img_cv = cv2.imdecode(img_array, cv2.COLOR_RGBA2BGR)
    # cv2.namedWindow('input_image', cv2.WINDOW_AUTOSIZE)
    # cv2.imshow('input_image', img_cv)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()






