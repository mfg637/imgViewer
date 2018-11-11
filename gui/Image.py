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
    def __init__(self, path, parent):
        self._path = path
        self._parent = parent
        self._wrapper = None
        self._icon = None
        self._file_name_label = None

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
        self._parent.show_image(decoders.open_image(str(self._path)))
