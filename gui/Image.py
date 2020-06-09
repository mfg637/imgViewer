#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter
import PIL.Image
from PIL import ImageTk
import os
import config
from pathlib import Path
from gui import somefile
import decoders
import tkinter.messagebox
import tkinter.filedialog
import cache
from . import move_file_dialog

img_icon = None

thumbnail_size = (192, 144)


def init():
    global img_icon
    img_icon = ImageTk.PhotoImage(PIL.Image.open(os.path.join(
        config.app_location,
        "images",
        "img_icon.png"
    )))


class Image(somefile.SomeFile):
    def __init__(self, path, parent, id):
        self._path = path
        self._abs_path = self._path.resolve()
        self.id = id
        self._parent = parent
        self._wrapper = None
        self._icon = None
        self._file_name_label = None
        self._thumbnail = None
        self.file_popup_menu = tkinter.Menu(self._parent.root, tearoff=0)
        self.file_popup_menu.add_command(label="hide menu")
        self.file_popup_menu.add_command(label="Delete file", command=self.__remove_file)
        self.file_popup_menu.add_command(label="Move/Rename file", command=self.__move_file_dialogue)
        self.file_popup_menu.add_command(label="Set as cover image", command=self.__set_cover)
        self._parent_root = None

    def __remove_file(self):
        answer = tkinter.messagebox.askokcancel(
            "File deleting",
            "Are you sure what you want delete file \"{}\"".format(str(self._path))
        )
        if answer:
            self._parent.remove_file(self.id)
            self._parent.page_rendering()

    def __move_file_dialogue(self):
        dialog = move_file_dialog.MoveFileDialog(self.__move_file_callback, self._parent_root, self._abs_path)

    def __move_file_callback(self, filepath):
        self._parent.move_file(self.id, str(filepath))
        self._parent.page_rendering()

    def create_widget(self, root, *pargs, **kwargs):
        self._parent_root = root
        self._create_widget(
            root,
            img_icon=img_icon,
            name=self._path.stem,
            bind=self.show_image,
            right_click_bind=self.show_popup_menu,
            *pargs, **kwargs)

    def show_image(self, event):
        self._parent.show_image(self.id)

    def show_popup_menu(self, event):
        self.file_popup_menu.post(event.x_root, event.y_root)

    def show_thumbnail(self):
        img = cache.manager.load_thumbnail(self._abs_path)
        self._thumbnail = ImageTk.PhotoImage(img)
        self._icon['image'] = self._thumbnail
        img.close()

    def __set_cover(self):
        cache.manager.load_folder_thumbnail(os.path.dirname(self._abs_path), cover_image=self._path)
