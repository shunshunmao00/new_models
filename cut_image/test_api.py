import os
import json
import requests


test_mode = 1  # 1: 本地， 2： 本机docker， 3. 开发环境k8s部署， 4. CubeAI生产环境  （3和4需要将xxxx替换为部署实例uuid）

if test_mode == 1:
    url_model = 'http://127.0.0.1:3330/api/model'
    url_stream = 'http://127.0.0.1:3330/api/stream/'
elif test_mode == 2:
    url_model = 'http://172.17.0.2:3330/api/model'
    url_stream = 'http://172.17.0.2:3330/api/stream/'
elif test_mode == 3:
    url_model = 'http://127.0.0.1:8080/ability/model/d3391d2594b14374a3be7649746df392'
    url_stream = 'http://127.0.0.1:8080/ability/stream/d3391d2594b14374a3be7649746df392/'
else:
    url_model = 'https://cubeai.dimpt.com/ability/model/0e08af7d9c8e4115937edc9ddbab4a64'
    url_stream = 'https://cubeai.dimpt.com/ability/stream/0e08af7d9c8e4115937edc9ddbab4a64/'


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


def test_cut_image_base64():
    with open('temp/result_base64.txt', 'r') as f:
        img_base64 = f.read()

    body = {
        'method': 'cut_image_base64',
        'kwargs': {
            'img_base64': img_base64,
        },
    }
    response = requests.post(url=url_model, data=json.dumps(body))
    result = json.loads(response.text, encoding='utf-8')

    if result['status'] == 'ok':
        print('图片列表： {}'.format(result['value']))
    else:
        print(result['value'])



test_gen_test_img_base64()
test_cut_image_base64()
