from PIL import ImageDraw
from hacktcha.generator.base import BaseCaptchaImage


class EastmoneyCaptchaImage(BaseCaptchaImage):
    def __init__(self, save_to: str):
        super().__init__(4, ("NotoSansJP-Regular.otf", 32, "#000"), "#fff", "0123456789", 30, save_to)

        self.add_transform(self.interfereing_line)

    def interfereing_line(self, img):
        do = ImageDraw.Draw(img)
        do.arc((self._width/4, self._height/4, self._width * 0.75, self._height*0.75), 0, 180, 0)
