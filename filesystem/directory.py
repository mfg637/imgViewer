#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter
import PIL.Image
from PIL import ImageTk
import os
import sys
from pathlib import Path

folder_icon = None
up_directory_icon = None


def init():
    global folder_icon
    global up_directory_icon
    folder_icon = ImageTk.PhotoImage(PIL.Image.open(os.path.join(
        os.path.dirname(sys.argv[0]),
        "images",
        "folder_icon.png"
     )))
    up_directory_icon = ImageTk.PhotoImage(PIL.Image.open(os.path.join(
        os.path.dirname(sys.argv[0]),
        "images",
        "up_directory_icon.png"
     )))


class Directory():
    def __init__(self, parent, directory):
        self.directory = directory
        self.parent = parent
        self._wrapper = None
        self._icon = None
        self._dir_name_label = None

    def create_widget(self, root, *pargs, **kwargs):
        self._wrapper = tkinter.Frame(root, *pargs, **kwargs)
        self._icon = tkinter.Label(self._wrapper, image=folder_icon)
        self._icon.pack(side="top")
        self._dir_name_label = tkinter.Label(
            self._wrapper,
            text=self.directory.stem,
            width=25,
            wraplength=192
        )
        self._dir_name_label.pack(side="top")
        self._wrapper.bind("<Double-Button-1>", self.open_dir)
        self._icon.bind("<Double-Button-1>", self.open_dir)
        self._dir_name_label.bind("<Double-Button-1>", self.open_dir)

    def grid(self, **kwargs):
        self._wrapper.grid(**kwargs)

    def open_dir(self, event):
        self.parent.open_dir(str(self.directory))

    def update(self):
        self._wrapper.update()


class ParentDirectory(Directory):
    def __init__(self, parent):
        super(ParentDirectory, self).__init__(parent, Path('..'))

    def create_widget(self, root, *pargs, **kwargs):
        self._wrapper = tkinter.Frame(root, *pargs, **kwargs)
        self._icon = tkinter.Label(self._wrapper, image=up_directory_icon)
        self._icon.pack(side="top")
        self._dir_name_label = tkinter.Label(
            self._wrapper,
            text=self.directory.stem,
            width=25,
            wraplength=192
        )
        self._dir_name_label.pack(side="top")
        self._wrapper.bind("<Double-Button-1>", self.open_dir)
        self._icon.bind("<Double-Button-1>", self.open_dir)
        self._dir_name_label.bind("<Double-Button-1>", self.open_dir)
