#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import PIL.Image
from PIL import ImageTk
import tkinter
from tkinter import filedialog


class GUI:
    def __init__(self):
        self.root = tkinter.Tk()
        self._show_image_window = None

    def show_image(self, img):
        self._show_image_window = ShowImage(self.root, img)


class ShowImage:
    def __init__(self, root, img, width=1280, height=720):
        self._root = tkinter.Toplevel(root)
        scaled_img = img.copy()
        scaled_img.thumbnail((width, height), PIL.Image.LANCZOS)
        self._image = ImageTk.PhotoImage(scaled_img)
        self.image_label = tkinter.Label(self._root, image=self._image)
        self.image_label.pack()