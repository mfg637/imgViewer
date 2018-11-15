#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import PIL.Image
from . import jpeg, ffmpeg_webm_video


def open_image(file_path):
    if jpeg.is_JPEG(file_path):
        decoder = jpeg.JPEGDecoder(file_path)
        decoded_jpg = decoder.decode()
        img = PIL.Image.open(decoded_jpg.stdout)
        return img
    return PIL.Image.open(file_path)
