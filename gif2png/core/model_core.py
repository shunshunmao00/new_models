# -*- coding: utf-8 -*-
import random
import asyncio
from core import image_tools
import os
from PIL import Image, ImageSequence
from core.global_data import g

class ModelCore(object):
    # 声明对外公开可通过API接口访问的方法。如public_methods未声明或值为None则默认本class中定义的所有方法都对外公开。
    public_methods = ('gen_test_img_base64', 'split_gif_base64',)

    def __init__(self):
        pass

    def send_img(self, img, index, ws_topic):
        img_url = image_tools.image_to_url(img)
        # print(img_url)
        if ws_topic is not None:
            asyncio.set_event_loop(g.event_loop)
            websocket = g.ws_connections.get(ws_topic)
            if websocket is not None:
                websocket.write_message({
                    'topic': ws_topic,
                    'type': 'data',
                    'content': img_url,
                    'imgid': index
                })

    def split_gif(self, gif, ws_topic):
        # GIF图片流的迭代器
        iter = ImageSequence.Iterator(gif)
        index = 1

        # 遍历图片流的每一帧
        for frame in iter:
            print("image %d: mode %s, size %s" % (index, frame.mode, frame.size))
            # frame.save("imgs/%s/frame%d.png" % (file_name, index))
            self.send_img(frame, index, ws_topic)
            index += 1


    def gen_test_img_base64(self):
        return image_tools.get_base64_from_file('core/gif_data/{}.gif'.format(random.randint(1, 6)))

    def split_gif_base64(self, img_base64, ws_topic=None):
        image = image_tools.url_to_img(img_base64)
        return self.split_gif(image, ws_topic)

    def process_websocket_message(self, websocket, msg):
        if g.event_loop is None:
            g.event_loop = asyncio.get_event_loop()

        if msg.get('type') == 'subscribe_gif2png':
            topic = msg.get('content')
            if isinstance(topic, str):
                if g.ws_connections.get(topic) is not None:
                    g.ws_connections.pop(topic)
                g.ws_connections[topic] = websocket


