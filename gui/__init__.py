#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
    def __init__(self, root, img):
        self._root = tkinter.Toplevel(root)
        self._image = ImageTk.PhotoImage(img)
        self.image_label = tkinter.Label(self._root, image=self._image)
        self.image_label.pack()