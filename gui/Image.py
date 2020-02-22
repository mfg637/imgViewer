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
import tkinter.messagebox
import tkinter.filedialog
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
        self.id = id
        self._parent = parent
        self._wrapper = None
        self._icon = None
        self._file_name_label = None
        self._thumbnail = None
        self.file_popup_menu = tkinter.Menu(self._parent.root, tearoff=0)
        self.file_popup_menu.add_command(label="hide menu")
        self.file_popup_menu.add_command(label="Delete file", command=self.__remove_file)
        self.file_popup_menu.add_command(label="Move/Rename file", command=self.__move_file)

    def __remove_file(self):
        answer = tkinter.messagebox.askokcancel(
            "File deleting",
            "Are you sure what you want delete file \"{}\"".format(str(self._path))
        )
        if answer:
            self._parent.remove_file(self.id)
            self._parent.page_rendering()

    def __move_file(self):
        filepath = tkinter.filedialog.asksaveasfilename(
            initialdir=self._path.parent.resolve(),
            initialfile=self._path.stem
        )
        if len(filepath)>0:
            self._parent.move_file(self.id, filepath+self._path.suffix)
            self._parent.page_rendering()


    def create_widget(self, root, *pargs, **kwargs):
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
