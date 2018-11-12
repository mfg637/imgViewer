#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter
import PIL.Image
from PIL import ImageTk
import threading
import decoders

width = 1280
height = 720


class ShowImage:
    def __init__(self, root, img, parent=None, _id=None):
        global width
        global height
        self._root = tkinter.Toplevel(root, background="black")
        self._root.attributes("-fullscreen", True)
        width = self._root.winfo_screenwidth()
        height = self._root.winfo_screenheight()
        self._img = img
        self._image = None
        self._canvas_img = None
        self._canvas = tkinter.Canvas(self._root, background="black")
        self._canvas.pack()
        self._canvas.bind("<Double-Button-1>", self.on_closing)
        self.__show()
        self._root.attributes("-topmost", True)
        self._root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self._root.bind("<Configure>", self.resize)
        self._root.bind("<Escape>", self.on_closing)
        if parent is not None:
            self._id = _id
            self.image_list = parent.get_image_files()
            self._root.bind("<Left>", self.__prev)
            self._root.bind("<Right>", self.__next)
        else:
            self._id = None
            self.image_list = None
        self._root.focus()

    def on_closing(self, event=None):
        self._img.close()
        self._root.destroy()

    def resize(self, event):
        global width
        global height
        if event.width != self._root.winfo_width() \
                or event.height != self._root.winfo_height():
            print(event.width, event.height)
            width = event.width
            height = event.height
            self.__show()

    def __show(self):
        scaled_img = self._img.copy()
        scaled_img.thumbnail((width, height), PIL.Image.LANCZOS)
        self._root.geometry("{}x{}".format(width, height))
        self._image = ImageTk.PhotoImage(scaled_img)
        self._canvas['width'] = width
        self._canvas['height'] = height
        self._canvas_img = self._canvas.create_image(
            int((width - scaled_img.width) / 2),
            int((height - scaled_img.height) / 2),
            anchor=tkinter.NW,
            image=self._image
        )

    def __prev(self, event):
        if self._id > 0:
            self._id -= 1
            self._img = decoders.open_image(str(self.image_list[self._id]))
            self.__show()

    def __next(self, event):
        if self._id < len(self.image_list)-1:
            self._id += 1
            self._img = decoders.open_image(str(self.image_list[self._id]))
            self.__show()