# -*- coding: UTF-8 -*-

import re

import requests
from bs4 import BeautifulSoup

from previewer.preview import Preview

__all__ = ["Page"]

UA = "Previewer/0.1 (+bfontaine.net)"

def get_html(url):
    resp = requests.get(url, headers={"User-Agent": UA})
    return resp.text if resp.ok else ""

def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    text = text.strip()
    return text


class Page:
    def __init__(self, url):
        self.url = url
        self.fetch()

    def fetch(self):
        html = get_html(self.url)
        self.soup = BeautifulSoup(html, "html.parser")

    @property
    def title(self):
        for meta in ("og:title", "twitter:title"):
            m = self._get_meta(meta)
            if m:
                return clean_text(m)

        title = self.soup.select_one("title")
        if title:
            return clean_text(title.text)

        # h1, h2
        for h in range(1, 2+1):
            el = self.soup.select_one("h%d" % h)
            if el:
                return clean_text(el.text)

        return clean_text(self.url)

    @property
    def excerpt(self):
        for meta in ("og:description", "twitter:description",
                     "description", "sailthru.description"):
            m = self._get_meta(meta)
            if m:
                return clean_text(m)

        p = self.soup.select_one("p")
        if p:
            t = clean_text(p.text)
            print(t)
            return t

        # TODO
        return ""

    @property
    def image_url(self):
        # Other candidates:
        # <link rel="apple-touch-icon" href=
        # <link rel="apple-touch-icon-precomposed" href=
        # <meta name="msapplication-TileImage"
        #
        for meta in ("og:image",):
            m = self._get_meta(meta)
            if m:
                return clean_text(m)


    def get_preview(self):
        return Preview(self)

    def _get_meta(self, name):
        el = self.soup.select_one("meta[property=%s]" % name)
        if el and "content" in el.attrs:
            return el.attrs["content"]
