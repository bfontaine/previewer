# -*- coding: UTF-8 -*-

from io import BytesIO
from urllib.parse import urlencode, urlparse

from flask import Flask, request, abort, redirect, make_response
from PIL import Image
from PIL import ImageDraw

app = Flask(__name__)

@app.route("/favicon.ico")
def favicon():
    abort(404)

@app.route("/<path:path>/p.png")
def main(path):
    url = path
    if request.args:
        url = "%s?%s" % (url, urlencode(request.args))

    p = urlparse(url)
    if p.scheme not in {"http", "https", ""}:
        abort(400)

    # User don't want an image: redirect them to the resource
    # Mattermost has the following Accept header:
    #   image/webp,image/*,*/*;q=0.8
    accept = request.headers.get("Accept", "")
    if False and not accept.startswith("image/"):  # debug
        return redirect(url)

    # just a test for now
    img = Image.new("RGBA", (400, 50))
    draw = ImageDraw.Draw(img)
    draw.text((5, 20), url, (0, 0, 0))
    fp = BytesIO()
    img.save(fp, format="PNG")

    fp.seek(0)
    resp = make_response(fp.read())
    resp.headers["Content-Type"] = "image/png"
    return resp

    # TODO
    return url
