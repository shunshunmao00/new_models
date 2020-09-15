from core.model_core import ModelCore
from core.util import image_tools


model_core = ModelCore()


def test():
    img_base64 = model_core.gen_test_img_base64()
    results = model_core.photo2painter_base64(img_base64)
    for img_url in results:
        img = image_tools.url_to_img(img_url)
        img.show()


test()
