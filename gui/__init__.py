#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import PIL.Image
from PIL import ImageTk
import tkinter
from tkinter import filedialog
from . import ScrolledFrame
import sys
import os
import filesystem


class ShowImage:
    def __init__(self, root, img, width=1280, height=720):
        self._root = tkinter.Toplevel(root)
        scaled_img = img.copy()
        scaled_img.thumbnail((width, height), PIL.Image.LANCZOS)
        self._image = ImageTk.PhotoImage(scaled_img)
        self.image_label = tkinter.Label(self._root, image=self._image)
        self.image_label.pack()
        self._root.attributes("-topmost", True)

class GUI:
    def __init__(self):
        self.root = tkinter.Tk()
        self._show_image_window = None
        self.root.geometry("840x720")
        self.thumbs_wrapper = ScrolledFrame.VerticalScrolledFrame(self.root, width=820, height=720)
        self.thumbs_wrapper.pack()
        self._img_icon = ImageTk.PhotoImage(PIL.Image.open(os.path.join(
            os.path.dirname(sys.argv[0]),
            "images",
            "img_icon.png"
        )))

    def show_image(self, img):
        self._show_image_window = ShowImage(self.root, img)

    def open_dir(self, directory_path):
        n = 4
        i = 0
        image_list = filesystem.get_image_files(directory_path)
        for image_path in image_list:
            item_wrapper = tkinter.Frame(self.thumbs_wrapper.interior)
            tkinter.Label(item_wrapper, image=self._img_icon).pack(side="top")
            tkinter.Label(
                item_wrapper,
                text=image_path.stem,
                width=25,
                wraplength=192
            ).pack(side="top")
            item_wrapper.grid(row=i//n, column=i%n, sticky=tkinter.N)
            i += 1