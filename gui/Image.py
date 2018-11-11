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
        self._wrapper = tkinter.Frame(root, *pargs, **kwargs)
        self._icon = tkinter.Label(self._wrapper, image=img_icon)
        self._icon.pack(side="top")
        self._file_name_label = tkinter.Label(
            self._wrapper,
            text=self._path.stem,
            width=25,
            wraplength=192
        )
        self._file_name_label.pack(side="top")
        self._wrapper.bind("<Double-Button-1>", self.show_image)
        self._icon.bind("<Double-Button-1>", self.show_image)
        self._file_name_label.bind("<Double-Button-1>", self.show_image)

    def show_image(self, event):
        self._parent.show_image(decoders.open_image(str(self._path)), self._id)

    def show_thumbnail(self):
        exist = True
        if not os.path.isdir('.thumbnails'):
            exist = False
            os.mkdir('.thumbnails')
        if exist and os.path.exists(os.path.join(".thumbnails", self._path.stem+'.webp')):
            img = decoders.open_image(os.path.join(".thumbnails", self._path.stem+'.webp'))
            self._thumbnail = ImageTk.PhotoImage(img)
            self._icon['image'] = self._thumbnail
            img.close()
        else:
            img = decoders.open_image(str(self._path))
            img.thumbnail((192, 144), PIL.Image.LANCZOS)
            self._thumbnail = ImageTk.PhotoImage(img)
            self._icon['image'] = self._thumbnail
            img.save(os.path.join(".thumbnails", self._path.stem+'.webp'), quality=90)
            img.close()
