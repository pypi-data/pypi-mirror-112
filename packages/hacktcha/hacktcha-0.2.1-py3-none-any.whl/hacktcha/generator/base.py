"""to make some generalized captcha images
"""
import itertools
import os
from typing import Callable, Tuple
import uuid
import random
import abc

from PIL import Image, ImageFont, ImageFilter, ImageDraw

class BaseCaptchaImage(metaclass=abc.ABCMeta):
    '''
    size: width, height in pixel
    font: font family(string), size (unit pound) and font color (in "#rrggbb" format)
    bgcolor: in "#rrggbb" format

    to generate a image with char-rotated, no padding/maring
    '''
    def __init__(self, nchars:int, font: Tuple[str, int, str], bgcolor:str, vocab:str, max_rotate:float=0, save_to:str="./sample"):
        self._font_family, self._font_size, self._font_color = font
        self._bgcolor = bgcolor

        self._nchars = nchars
        self._vocab = vocab
        self._save_to = save_to

        self._font = ImageFont.truetype(self._font_family, self._font_size)
        #self._font = ImageFont.load_default()
        self._max_rotate = max_rotate * 100

        width, height = self._font.getsize(vocab)
        # 1.2: leave space for rotate
        self._width = int(width * (1 + nchars) * 1.2 / len(vocab))
        self._height = int(1.2 * height)

        #self._top_margin = int(self._height * 0.025)
        self._left_margin = int(self._width / (2 * nchars))

        self._tfms = []

    # by default, draw center align text
    def draw_text(self, img: Image, text:str):
        char_start_pos = self._left_margin
        for char in text:
            char_width, char_height = self._font.getsize(char)

            char_img = Image.new('RGB', (char_width, char_height), self._bgcolor)
            draw_obj = ImageDraw.Draw(char_img)
            draw_obj.text((0,0), char, fill=self._font_color, font= self._font)
            if self._max_rotate != 0:
                angle = random.randint(-self._max_rotate, self._max_rotate) / 100.0
                char_img = char_img.rotate(angle, resample = 2, fillcolor=self._bgcolor)

            img.paste(char_img, (char_start_pos, 0))
            char_start_pos += int(char_width * 1.2)

        return img


    def draw_background(self, img):
        pass
    
    def add_transform(self, transform: Callable):
        self._tfms.append(transform)


    def gen_image(self, text:str):
        img = Image.new('RGB', (self._width, self._height), self._bgcolor)

        self.draw_background(img)
        self.draw_text(img, text)

        for transform in self._tfms:
            transform(img)

        file = os.path.join(self._save_to, f"{text}_{str(uuid.uuid4())[-4:]}.jpg")
        file = os.path.normpath(file)

        img.save(file)
        img.close()

    def run(self, epoch:int=1, total:int=999999999999999):
        print("total is ", total)
        for i in range(epoch):
            for chars in itertools.permutations(self._vocab, self._nchars):
                text = "".join(chars)
                self.gen_image(text)
                total -= 1

                if total <= 0:
                    break
            if total <= 0:
                break

if __name__ == "__main__":
    vocab = "0123456789"
    captcha = BaseCaptchaImage(4, font=("NotoSansJP-Regular.otf", 32, "#000000"), vocab=vocab, max_rotate=30, bgcolor="#fff")
    captcha.run(total = 5)
