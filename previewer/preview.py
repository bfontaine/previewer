# -*- coding: UTF-8 -*-

import os.path
from io import BytesIO

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from previewer.text import fit_text


here = os.path.dirname(__file__)

def load_font(name, *args, **kwargs):
    path = os.path.join(here, "assets", "fonts", "%s.otf" % name)
    return ImageFont.truetype(path, *args, **kwargs)

title_font = load_font("Alegreya-Bold", size=14)
excerpt_font = load_font("Alegreya-Regular", size=10)

class Preview:
    def __init__(self, page,
            size=(400, 70), padding_x=7, padding_y=5, bg="white", fg="black"):

        self.page = page
        self.width, self.height = size
        self._padding_x = padding_x
        self._padding_y = padding_y
        self._fg = fg
        self._bg = bg

        self._max_width = self.width - 2 * self._padding_x
        self._max_height = self.height - 2 * self._padding_y

        self.content_type = "image/png"

        self._y = self._padding_y

        self._img = Image.new("RGB", size, bg)
        self._draw = ImageDraw.Draw(self._img)

        self._draw_title()
        # some margin please
        self._y += 10

        self._draw_excerpt()

    def bytes(self):
        fp = BytesIO()
        self._img.save(fp, format="PNG")
        fp.seek(0)
        return fp.read()

    def _draw_text(self, text, font, max_lines=None):
        max_height = self.height - self._y - self._padding_y
        text = fit_text(text, font, self._max_width,
                max_height, max_lines=max_lines)

        # for some reason we have to encode this to get it to work. Using
        # font.getsize doesn't raise an exception but returns wrong dimensions.
        latin1_text = text.encode("utf-8").decode("latin1")
        _, h = self._draw.textsize(latin1_text)

        self._draw.text((self._padding_x, self._y),
                        text, fill=self._fg, font=font)

        self._y += h

    def _draw_title(self):
        self._draw_text(self.page.title, title_font, max_lines=1)

    def _draw_excerpt(self):
        self._draw_text(self.page.excerpt, excerpt_font, max_lines=4)
