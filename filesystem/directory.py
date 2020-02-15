#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter
import PIL.Image
from PIL import ImageTk
import os
import sys
from pathlib import Path
from gui import somefile
import abc

folder_icon = None
up_directory_icon = None
select_all_icon = None


def init():
    global folder_icon
    global up_directory_icon
    global select_all_icon
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
    select_all_icon = ImageTk.PhotoImage(PIL.Image.open(os.path.join(
        os.path.dirname(sys.argv[0]),
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
        self._image = folder_icon

    def create_widget(self, root, *pargs, **kwargs):
        self._create_widget(root, img_icon=self._image, name=self.directory.stem, bind=self.open_dir, *pargs, **kwargs)

    def open_dir(self, event=None):
        self._parent.open_dir(str(self.directory))


class ParentDirectory(Directory):
    def __init__(self, parent):
        super(ParentDirectory, self).__init__(parent, Path('..'))
        self._image = up_directory_icon


