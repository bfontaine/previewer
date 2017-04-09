# -*- coding: UTF-8 -*-

from urllib.parse import urlencode, urlparse

from flask import Flask, request, abort, redirect, make_response

from previewer import Page

app = Flask(__name__)

@app.route("/favicon.ico")
def favicon():
    abort(404)

@app.route("/")
def root():
    return redirect("https://github.com/bfontaine/previewer#previewer")

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
    if not accept.startswith("image/"):
        return redirect(url)

    p = Page(url)
    if not p.has_content:
        # We can't show anything: redirect to the original
        return redirect(url)

    preview = p.get_preview()

    resp = make_response(preview.bytes())
    resp.headers["Content-Type"] = preview.content_type
    return resp
