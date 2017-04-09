# -*- coding: UTF-8 -*-

import re

import chardet
import requests
from bs4 import BeautifulSoup

from previewer.preview import Preview

__all__ = ["Page"]

UA = "Previewer/0.1 (+bfontaine.net)"

def http_get(url):
    return requests.get(url, headers={"User-Agent": UA})

def get_html(url):
    resp = http_get(url)
    if not resp.ok:
        return ""

    if resp.headers.get("content-type", "") not in {"text/xhtml", "text/html"}:
        return ""

    # fix for wrong encoding guesses
    if resp.encoding != "utf-8" and \
            chardet.detect(resp.content)["encoding"] == "utf-8":
        resp.encoding = "utf-8"

    return resp.text

def clean_text(text):
    text = re.sub(r"\s+", " ", text, re.UNICODE)
    text = text.strip()
    return text

class Page:
    def __init__(self, url):
        self.url = url
        self.fetch()

    def fetch(self):
        html = get_html(self.url)
        self.soup = BeautifulSoup(html, "html.parser")
        self.has_content = bool(html)

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

        for p in self.soup.select("p", limit=2):
            if len(p.text) > 70:
                return clean_text(p.text)

        # TODO
        return ""

    @property
    def image_url(self):
        for rel in ("icon", "apple-touch-icon", "apple-touch-icon-precomposed",
                    "msapplication-TileImage"):
            href = self._get_link(rel)
            if href:
                return href

        for meta in ("og:image", "twitter:image", "msapplication-TileImage"):
            m = self._get_meta(meta)
            if m:
                return clean_text(m)


    def get_preview(self):
        return Preview(self)

    def _get_link(self, rel):
        el = self.soup.select_one("link[rel=%s]" % rel)
        if el and "href" in el.attrs:
            return el.attrs["href"]

    def _get_meta(self, name):
        el = self.soup.select_one("meta[property=%s]" % name)
        if el and "content" in el.attrs:
            return el.attrs["content"]
