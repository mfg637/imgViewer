#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import lxml.etree
import PIL.ImageColor as Color


def rgbnorm_to_hsl(r: float, g: float, b: float):
    # r, g, b - [0; 1]
    # h - [0; 360] degrees
    # s, l - [0; 1]
    rgbmin = min(r, g, b)
    rgbmax = max(r, g, b)
    sum = rgbmin + rgbmax
    l = sum/2
    diff = rgbmax - rgbmin
    h = 0
    if rgbmax == rgbmin:
        pass
    elif rgbmax == r and g >= b:
        h = ((g - b)/diff) * 60
    elif rgbmax == r and g < b:
        h = ((g - b) / diff) * 60 + 360
    elif rgbmax == g:
        h = ((b - r) / diff) * 60 + 120
    elif rgbmax == b:
        h = ((r - g) / diff) * 60 + 240
    s = 0
    if l == 0 or rgbmax == rgbmin:
        pass
    elif 0 < l <= 0.5:
        s = diff/sum
    elif l <= 1:
        s = diff/(2-sum)
    return h, s, l


def hsl_to_rgbnorm(h, s, l):
    # h - [0; 360] degrees
    # s, l - [0; 1]
    # r, g, b - [0; 1]

    # fix incorrect values
    while h < 0:
        h = 360 + h
    while h >= 360:
        h -= 360
    if s < 0:
        s=0
    elif s>1:
        s=1
    if l<0:
        s=0
    elif l>1:
        l=1

    # algorithm
    c = (1-abs(2*l-1)) * s
    x = c * (1 - abs((h/60) % 2 - 1))
    m = l - c/2
    if 0 <= h < 60:
        return c + m, x + m, m
    elif 60 <= h < 120:
        return x + m, c + m, m
    elif 120 <= h < 180:
        return m, c + m, x + m
    elif 180 <= h < 240:
        return m, x + m, c + m
    elif 240 <= h < 300:
        return x + m, m, c + m
    else:
        return c + m, m, x + m


def hex_color(*rgb):
    return "#{}{}{}".format(*[hex(rgb[i])[2:].rjust(2, '0') for i in range(len(rgb))])


def byte_limit(x):
    if x < 0:
        return 0
    elif x > 255:
        return 255
    else:
        return x


keys = (
    'back_side_linear_gradient',
    'back_side_radial_gradient',
    'front_side_linear_gradient',
    'front_side_radial_gradient'
)


def paint_icon(icon_file, new_color_hex):

    data = None

    with open(icon_file, 'r') as f:
        data = lxml.etree.parse(f, lxml.etree.XMLParser())
    root = data.getroot()

    base_color_rgb = Color.getrgb("#F6D443")
    base_color_hsl = rgbnorm_to_hsl(*[i / 255 for i in base_color_rgb])
    new_color_rgb = Color.getrgb(new_color_hex)
    new_color_hsl = rgbnorm_to_hsl(*[i / 255 for i in new_color_rgb])

    for child in root:
        if child.get("id") in keys:
            for stop in child:
                orig_css = stop.get("style")
                srcrgb = Color.getrgb(orig_css[11:18])
                srchsl = rgbnorm_to_hsl(*[i/255 for i in srcrgb])
                hsldiff = [base_color_hsl[i] - srchsl[i] for i in range(3)]
                new_hsl = [new_color_hsl[i] - hsldiff[i] for i in range(3)]
                new_rgb = [int(i*255) for i in hsl_to_rgbnorm(*new_hsl)]
                _hex = hex_color(*new_rgb)
                result_css = orig_css[:11] + _hex + orig_css[18:]
                stop.set("style", result_css)

    return "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n".encode("utf-8") + \
           lxml.etree.tostring(root, pretty_print=True, encoding="utf-8")

