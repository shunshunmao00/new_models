import os
import argparse
from DRL.actor import *
from Renderer.stroke_gen import *
from Renderer.model import *

device = torch.device("cpu")
width = 128

class Painter(object):
    def __init__(self):
        # set default argument
        self.max_step = 20
        self.actor = 'model/actor.pkl'
        self.renderer = 'model/renderer.pkl'
        self.imgid = 0 # set begin number for generated image
        self.divide = 4
        self.canvas_cnt = self.divide * self.divide
        self.T = torch.ones([1, 1, width, width], dtype=torch.float32).to(device)


        self.coord = torch.zeros([1, 2, width, width])
        for i in range(width):
            for j in range(width):
                self.coord[0, 0, i, j] = i / (width - 1.)
                self.coord[0, 1, i, j] = j / (width - 1.)
        self.coord = self.coord.to(device) # Coordconv

        self.Decoder = FCN()
        self.Decoder.load_state_dict(torch.load(self.renderer))


    def decode(self, x, canvas):  # b * (10 + 3)
        x = x.view(-1, 10 + 3)
        stroke = 1 - self.Decoder(x[:, :10])
        stroke = stroke.view(-1, width, width, 1)
        color_stroke = stroke * x[:, -3:].view(-1, 1, 1, 3)
        stroke = stroke.permute(0, 3, 1, 2)
        color_stroke = color_stroke.permute(0, 3, 1, 2)
        stroke = stroke.view(-1, 5, 1, width, width)
        color_stroke = color_stroke.view(-1, 5, 3, width, width)
        res = []
        for i in range(5):
            canvas = canvas * (1 - stroke[:, i]) + color_stroke[:, i]
            res.append(canvas)
        return canvas, res

    def small2large(self, x):
        # (d * d, width, width) -> (d * width, d * width)
        x = x.reshape(self.divide, self.divide, width, width, -1)
        x = np.transpose(x, (0, 2, 1, 3, 4))
        x = x.reshape(self.divide * width, self.divide * width, -1)
        return x

    def large2small(self, x):
        # (d * width, d * width) -> (d * d, width, width)
        x = x.reshape(self.divide, width, self.divide, width, 3)
        x = np.transpose(x, (0, 2, 1, 3, 4))
        x = x.reshape(self.canvas_cnt, width, width, 3)
        return x

    def smooth(self, img):
        def smooth_pix(img, tx, ty):
            if tx == self.divide * width - 1 or ty == self.divide * width - 1 or tx == 0 or ty == 0:
                return img
            img[tx, ty] = (img[tx, ty] + img[tx + 1, ty] + img[tx, ty + 1] + img[tx - 1, ty] + img[tx, ty - 1] + img[
                tx + 1, ty - 1] + img[tx - 1, ty + 1] + img[tx - 1, ty - 1] + img[tx + 1, ty + 1]) / 9
            return img

        for p in range(self.divide):
            for q in range(self.divide):
                x = p * width
                y = q * width
                for k in range(width):
                    img = smooth_pix(img, x + k, y + width - 1)
                    if q != self.divide - 1:
                        img = smooth_pix(img, x + k, y + width)
                for k in range(width):
                    img = smooth_pix(img, x + width - 1, y + k)
                    if p != self.divide - 1:
                        img = smooth_pix(img, x + width, y + k)
        return img

    def save_img(self, res, imgid, origin_shape, divide=False):
        output = res.detach().cpu().numpy()  # d * d, 3, width, width
        output = np.transpose(output, (0, 2, 3, 1))
        if divide:
            output = self.small2large(output)
            output = self.smooth(output)
        else:
            output = output[0]
        output = (output * 255).astype('uint8')
        output = cv2.resize(output, origin_shape)

        cv2.imwrite('output/generated' + str(imgid) + '.png', output)


    def do_paint(self, img):
        # img = cv2.imread(img_path, cv2.IMREAD_COLOR)
        origin_shape = (img.shape[1], img.shape[0])

        actor = ResNet(9, 18, 65)  # action_bundle = 5, 65 = 5 * 13
        actor.load_state_dict(torch.load(self.actor))
        actor = actor.to(device).eval()
        self.Decoder = self.Decoder.to(device).eval()

        canvas = torch.zeros([1, 3, width, width]).to(device)

        patch_img = cv2.resize(img, (width * self.divide, width * self.divide))
        patch_img = self.large2small(patch_img)
        patch_img = np.transpose(patch_img, (0, 3, 1, 2))
        patch_img = torch.tensor(patch_img).to(device).float() / 255.

        img = cv2.resize(img, (width, width))
        img = img.reshape(1, width, width, 3)
        img = np.transpose(img, (0, 3, 1, 2))
        img = torch.tensor(img).to(device).float() / 255.

        os.system('mkdir output')

        with torch.no_grad():
            if self.divide != 1:
                self.max_step = self.max_step // 2
            for i in range(self.max_step):
                stepnum = self.T * i / self.max_step
                actions = actor(torch.cat([canvas, img, stepnum, self.coord], 1))
                canvas, res = self.decode(actions, canvas)
                print('canvas step {}, L2Loss = {}'.format(i, ((canvas - img) ** 2).mean()))
                for j in range(5):
                    self.save_img(res[j], self.imgid, origin_shape)
                    self.imgid += 1
            if self.divide != 1:
                canvas = canvas[0].detach().cpu().numpy()
                canvas = np.transpose(canvas, (1, 2, 0))
                canvas = cv2.resize(canvas, (width * self.divide, width * self.divide))
                canvas = self.large2small(canvas)
                canvas = np.transpose(canvas, (0, 3, 1, 2))
                canvas = torch.tensor(canvas).to(device).float()
                coord = self.coord.expand(self.canvas_cnt, 2, width, width)
                self.T = self.T.expand(self.canvas_cnt, 1, width, width)
                for i in range(self.max_step):
                    stepnum = self.T * i / self.max_step
                    actions = actor(torch.cat([canvas, patch_img, stepnum, coord], 1))
                    canvas, res = self.decode(actions, canvas)
                    print('divided canvas step {}, L2Loss = {}'.format(i, ((canvas - patch_img) ** 2).mean()))
                    for j in range(5):
                        self.save_img(res[j], self.imgid, origin_shape, True)
                        self.imgid += 1


