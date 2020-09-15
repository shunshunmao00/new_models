# -*- coding:utf-8 -*-
import json
import requests
import os
from core.util import image_tools


test_mode = 1  # 1: 本地， 2： 本机docker， 3. 开发环境k8s部署， 4. CubeAI生产环境  （3和4需要将xxxx替换为部署实例uuid）

if test_mode == 1:
    url_model = 'http://127.0.0.1:3330/api/model'
    url_stream = 'http://127.0.0.1:3330/api/stream/'
elif test_mode == 2:
    url_model = 'http://172.17.0.2:3330/api/model'
    url_stream = 'http://172.17.0.2:3330/api/stream/'
elif test_mode == 3:
    url_model = 'http://127.0.0.1:8080/ability/model/xxxx'
    url_stream = 'http://127.0.0.1:8080/ability/stream/xxxx/'
else:
    url_model = 'https://cubeai.dimpt.com/ability/model/xxxx'
    url_stream = 'https://cubeai.dimpt.com/ability/stream/xxxx/'


def test_gen_test_img_base64():
    body = {
        'method': 'gen_test_img_base64',
        'kwargs': {},
    }

    response = requests.post(url=url_model, data=json.dumps(body))
    result = json.loads(response.text, encoding='utf-8')
    if result['status'] == 'ok':
        img_base64 = result['value']
        if not os.path.exists('temp'):
            os.system('mkdir temp')
        with open('temp/result_base64.txt', 'w') as f:
            f.write(img_base64)
            print('随机base64编码字符串已存入临时文件：' + 'temp/result_base64.txt')
    else:
        print(result['value'])

def test_photo2painter_base64():
    with open('temp/result_base64.txt', 'r') as f:
        img_base64 = f.read()

    body = {
        'method': 'photo2painter_base64',
        'kwargs': {
            'img_base64': img_base64,
        },
    }
    response = requests.post(url=url_model, data=json.dumps(body))
    result = json.loads(response.text, encoding='utf-8')

    if result['status'] == 'ok':
        imgs = result['value']
        for img_url in imgs:
            img = image_tools.url_to_img(img_url)
            img.show()
    else:
        print(result['value'])


test_gen_test_img_base64()
test_photo2painter_base64()

