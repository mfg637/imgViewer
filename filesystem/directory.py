#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter, tkinter.simpledialog, tkinter.messagebox
import PIL.Image
from PIL import ImageTk
import os
import config
from pathlib import Path

from .filesystem import browse_folder
from gui import somefile
import abc
import cache

folder_icon = None
up_directory_icon = None
select_all_icon = None


def init():
    global folder_icon
    global up_directory_icon
    global select_all_icon
    folder_icon = ImageTk.PhotoImage(PIL.Image.open(os.path.join(
        config.app_location,
        "images",
        "folder_icon.png"
     )))
    up_directory_icon = ImageTk.PhotoImage(PIL.Image.open(os.path.join(
        config.app_location,
        "images",
        "up_directory_icon.png"
     )))
    select_all_icon = ImageTk.PhotoImage(PIL.Image.open(os.path.join(
        config.app_location,
        "images",
        "select_all_icon.png"
    )))


class AbstractDirectory(somefile.SomeFile, abc.ABC):
    def __init__(self, parent):
        #self.directory = directory
        self._parent = parent
        self._wrapper = None
        self._icon = None
        self._dir_name_label = None

    @abc.abstractmethod
    def open_dir(self, event=None):
        pass


class MatchFilesPattern(AbstractDirectory):
    def __init__(self, parent):
        super(MatchFilesPattern, self).__init__(parent)

    def create_widget(self, root, *pargs, **kwargs):
        self._create_widget(root, img_icon=select_all_icon, name="*", bind=self.open_dir, *pargs, **kwargs)

    def open_dir(self, event=None):
        self._parent.browse_all_files()


class Directory(AbstractDirectory):
    def __init__(self, parent, directory:Path):
        super(Directory, self).__init__(parent)
        self.directory = directory
        self._custom_icon = None
        self._image = folder_icon
        self.dir_popup_menu = tkinter.Menu(self._parent.root, tearoff=0)
        self.dir_popup_menu.add_command(label="hide menu")
        self.dir_popup_menu.add_command(label="Change color", command=self.__change_color)
        self.dir_popup_menu.add_command(label="Rename", command=self.__rename)
        try:
            items = browse_folder(directory)
            if len(items[0])==0 and len(items[1])==0:
                self.dir_popup_menu.add_command(label="Delete", command=self.__delete)
        except PermissionError:
            pass

    def show_thumbnail(self):
        self.load_icon()

    def load_icon(self, color=None, cover=None):
        self._custom_icon = cache.manager.load_folder_thumbnail(self.directory.resolve(), color, cover)
        if self._custom_icon is None:
            self._image = folder_icon
        else:
            self._custom_icon = ImageTk.PhotoImage(self._custom_icon)
            self._image = self._custom_icon
        self._icon['image'] = self._image

    def create_widget(self, root, *pargs, **kwargs):
        self._create_widget(
            root,
            img_icon=self._image,
            name=self.directory.stem,
            bind=self.open_dir,
            right_click_bind=self.show_popup_menu,
            *pargs, **kwargs
        )

    def open_dir(self, event=None):
        self._parent.open_dir(str(self.directory))

    def show_popup_menu(self, event):
        self.dir_popup_menu.post(event.x_root, event.y_root)

    def __change_color(self):
        hex_color = tkinter.simpledialog.askstring("New color", "hex color:")
        if hex_color is None:
            return
        self.load_icon(color=hex_color)

    def __delete(self):
        answer = tkinter.messagebox.askokcancel(
            "Directory deleting",
            "Are you sure what you want delete this folder \"{}\"".format(str(self.directory))
        )
        if answer:
            for f in self.directory.iterdir():
                f.unlink()
            self.directory.rmdir()
            self._parent.open_dir('.')

    def __rename(self, event=None):
        RENAME_ERROR_TITLE = "Rename Error"

        new_name = tkinter.simpledialog.askstring(
            "Rename dialogue",
            "Rename \"{}\" to:".format(self.directory.name),
        )
        if new_name is not None:
            if len(new_name) > 0:
                try:
                    self.directory = cache.manager.rename_dir(self.directory.resolve(), new_name)
                except FileExistsError as e:
                    tkinter.messagebox.showerror(RENAME_ERROR_TITLE, "Directory not found: {}".format(e.args[0].name))
            else:
                tkinter.messagebox.showerror(RENAME_ERROR_TITLE, "Empty name!")
        self._parent.open_dir('.')


class ParentDirectory(AbstractDirectory):
    def __init__(self, parent):
        super(ParentDirectory, self).__init__(parent)
        self._image = up_directory_icon

    def create_widget(self, root, *pargs, **kwargs):
        self._create_widget(
            root,
            img_icon=self._image,
            name="..",
            bind=self.open_dir,
            *pargs, **kwargs
        )

    def open_dir(self, event=None):
        self._parent.open_dir("..")




