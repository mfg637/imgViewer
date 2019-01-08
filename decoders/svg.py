#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

svg_tag = re.compile(r'<svg[^>]*>')
attributes = re.compile(r'[a-zA-Z\:]+\s?=\s?[\'\"][^\'\"]+[\'\"]')


def is_svg(file_path):
    file = open(file_path, 'r')
    try:
        data = file.read()
    except UnicodeDecodeError:
        file.close()
        return False
    file.close()
    return svg_tag.search(data) is not None


def get_resolution(file_path):
    file = open(file_path, 'r')
    data = file.read()
    file.close()
    svg_tag_data = svg_tag.search(data).group(0)
    svg_raw_attributes = attributes.findall(svg_tag_data)
    svg_attributes = dict()
    for raw_attribute in svg_raw_attributes:
        attribute_name, attribute_value = raw_attribute.split('=')
        if attribute_name[-1] == ' ':
            attribute_name = attribute_name[:-1]
        if attribute_value[0] == ' ':
            attribute_value = attribute_value[1:]
        if (attribute_value[0] == '\'' and attribute_value[-1] == '\'') or \
                (attribute_value[0] == '\"' and attribute_value[-1] == '\"'):
            attribute_value = attribute_value[1:-1]
        svg_attributes[attribute_name] = attribute_value
    if 'width' in svg_attributes and 'height' in svg_attributes:
        return (float(svg_attributes['width']), float(svg_attributes['height']))
    elif 'viewBox' in svg_attributes:
        values = svg_attributes['viewBox'].split(' ')
        return (float(values[2]), float(values[3]))
    else:
        return None


def decode(file_path, required_size=None):
    pass