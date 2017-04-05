# -*- coding: UTF-8 -*-

import textwrap

def fit_width(text, font, width, max_lines=None):
    if not text:
        return text

    w, _ = font.getsize(text)

    # easy case
    if w <= width:
        return text

    pt_w, _ = font.getsize(".")
    width_pt = int(width / float(pt_w))

    wrapped = None
    wrap_width = width_pt

    while w > width:
        wrap_width -= 1

        lines = textwrap.wrap(text, width=wrap_width,
                                max_lines=max_lines,
                                placeholder="...",
                                break_long_words=False)

        too_long_word = False
        for l in lines:
            if len(l) > wrap_width:
                too_long_word = True
                break

        # one of the lines doesn't fit: keep the first one and truncate it if
        # necessary
        if too_long_word:
            text = lines[0]
            while w > width:
                text = textwrap.shorten(text, wrap_width, placeholder="...")
                w, _ = font.getsize(text)
                wrap_width -= 1

            return text

        wrapped = "\n".join(lines)
        w, _ = font.getsize(lines[0])

    return wrapped


def fit_height(text, font, height):
    _, line_height = font.getsize("A")
    spacing = 4

    # Find highest X such as
    # X*line_height + (X-1)*spacing <= height

    # X*line_height + X*spacing - spacing <= height
    # X*line_height + X*spacing <= height + spacing
    # X*(line_height+spacing) <= height + spacing
    # X <= (height + spacing) / (line_height + spacing)

    lines_count = int((height + spacing) / float(line_height + spacing))

    lines = text.split("\n")
    if len(lines) > lines_count:
        text = "%s..." % ("\n".join(lines[:lines_count]))[:-3]

    return text

def fit_text(text, font, width, height, max_lines=None):
    text = fit_width(text, font, width, max_lines)
    text = fit_height(text, font, height)
    return text
