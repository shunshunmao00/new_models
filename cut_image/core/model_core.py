# -*-coding:utf-8-*-
# -*- coding: utf-8 -*-
import random
import asyncio
from PIL import Image
from core import image_tools
from core.global_data import g


class ModelCore(object):
    # 声明对外公开可通过API接口访问的方法。如public_methods未声明或值为None则默认本class中定义的所有方法都对外公开。
    public_methods = ('cut_image_base64', 'gen_test_img_base64')

    def __init__(self):
        pass

    def gen_test_img_base64(self):
        return image_tools.get_base64_from_file('core/image_data/{}.jpg'.format(random.randint(1, 3)))

    def cut_image_base64(self, img_base64, ws_topic):
        square_img = self.fill_image(image_tools.url_to_img(img_base64))
        img_list = self.cut_image(square_img)
        return img_list

    # 将图片填充为正方形
    def fill_image(self, image):
        width, height = image.size
        # 选取长和宽中较大值作为新图片的
        new_image_length = width if width > height else height
        # 生成新图片[白底]
        new_image = Image.new(image.mode, (new_image_length, new_image_length), color='white')
        # 将之前的图粘贴在新图上，居中
        if width > height:  # 原图宽大于高，则填充图片的竖直维度
            new_image.paste(image, (0, int((new_image_length - height) / 2)))  # (x,y)二元组表示粘贴上图相对下图的起始位置
        else:
            new_image.paste(image, (int((new_image_length - width) / 2), 0))
        return new_image

    def cut_image(self, image):
        width, height = image.size
        item_width = int(width / 3)
        box_list = []
        # (left, upper, right, lower)
        for i in range(0, 3):
            for j in range(0, 3):
                # print((i*item_width,j*item_width,(i+1)*item_width,(j+1)*item_width))
                box = (j * item_width, i * item_width, (j + 1) * item_width, (i + 1) * item_width)
                box_list.append(box)

        image_list = [image.crop(box) for box in box_list]
        re_list = []
        image_tools.image_to_url
        for item in image_list:
            re_list.append(image_tools.image_to_url(item))

        return re_list

    def process_websocket_message(self, websocket, msg):
        if g.event_loop is None:
            g.event_loop = asyncio.get_event_loop()

        if msg.get('type') == 'subscribe_gif2png':
            topic = msg.get('content')
            if isinstance(topic, str):
                if g.ws_connections.get(topic) is not None:
                    g.ws_connections.pop(topic)
                g.ws_connections[topic] = websocket
