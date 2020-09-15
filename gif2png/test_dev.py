import os
from core.model_core import ModelCore

model_core = ModelCore()

gif_base64 = model_core.gen_test_img_base64()
print( gif_base64)
model_core = model_core.split_gif_base64(gif_base64)
