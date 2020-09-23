# -*-coding:utf-8-*-
from core.model_core import ModelCore

model_core = ModelCore()
url = 'https://gitee.com/mirrors/CubeAI.git'
# url = 'https://github.com/cube-ai/cubeai.git'
model_core.find_secret(url,'xxx')
