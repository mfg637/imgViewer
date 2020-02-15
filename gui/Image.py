#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter
import PIL.Image
from PIL import ImageTk
import os
import sys
from pathlib import Path
from gui import somefile
import decoders

img_icon = None

thumbnail_size = (192, 144)

def init():
    global img_icon
    img_icon = ImageTk.PhotoImage(PIL.Image.open(os.path.join(
        os.path.dirname(sys.argv[0]),
        "images",
        "img_icon.png"
    )))


class Image(somefile.SomeFile):
    def __init__(self, path, parent, id):
        self._path = path
        self._id = id
        self._parent = parent
        self._wrapper = None
        self._icon = None
        self._file_name_label = None
        self._thumbnail = None

    def create_widget(self, root, *pargs, **kwargs):
        self._create_widget(root, img_icon=img_icon, name=self._path.stem, bind=self.show_image, *pargs, **kwargs)

    def show_image(self, event):
        self._parent.show_image(self._id)

    def show_thumbnail(self):
        exist = True
        #if not os.path.isdir('.thumbnails'):
        #    exist = False
        #    os.mkdir('.thumbnails')
        #if exist and os.path.exists(os.path.join(".thumbnails", self._path.stem+'.webp')):
        #    img = decoders.open_image(os.path.join(".thumbnails", self._path.stem+'.webp'))
        #    self._thumbnail = ImageTk.PhotoImage(img)
        #    self._icon['image'] = self._thumbnail
        #    img.close()
        #else:
        source_img = decoders.open_image(str(self._path), thumbnail_size)
        img = source_img.convert(mode="RGBA")
        source_img.close()
        img.thumbnail(thumbnail_size, PIL.Image.LANCZOS)
        self._thumbnail = ImageTk.PhotoImage(img)
        self._icon['image'] = self._thumbnail
        #    img.save(os.path.join(".thumbnails", self._path.stem+'.webp'), quality=90)
        img.close()
