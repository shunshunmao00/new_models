import os
from core.model_core import ModelCore

model_core = ModelCore()

img_base64 = model_core.gen_test_img_base64()
print( img_base64)
reList = model_core.cut_image_base64(img_base64, 'xxx')
print(reList)
