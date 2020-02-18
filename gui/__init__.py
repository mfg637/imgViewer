#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter
import tkinter.ttk
from tkinter import messagebox
import tkinter.simpledialog
from . import ScrolledFrame
import os
import filesystem
from . import Image
import re
from math import ceil
import threading
from . import imgViewer
from pathlib import Path

unsigned_number_validate = re.compile(r"^\s*\d+\s*$")
items_per_page = 52
n = 4


class GUI:
    def __init__(self):
        self.root = tkinter.Tk()
        self._show_image_window = None
        self.root.geometry("840x525")
        filesystem.directory.init()
        Image.init()
        imgViewer.init()
        self.thumbs_wrapper = ScrolledFrame.VerticalScrolledFrame(self.root, width=820, height=500)
        self.thumbs_wrapper.pack(side="top")
        self._items_list = []
        self._page = 0
        bottom_panel = tkinter.Frame(self.root)
        tkinter.ttk.Button(
            bottom_panel,
            text="parent dir",
            command=lambda:self.open_dir('..')
        ).pack(side="left")
        tkinter.Label(bottom_panel, text="Page: ").pack(side="left")
        self.page_count_field = tkinter.Entry(bottom_panel, width=5)
        self.page_count_field.pack(side="left")
        self.page_count_field.bind("<Return>", self.__goto)
        self.page_count_field.bind("<KP_Enter>", self.__goto)
        tkinter.Label(bottom_panel, text = "of ").pack(side="left")
        self._page_count_label = tkinter.Label(bottom_panel)
        self._page_count_label.pack(side="left")
        self.goto_btn = tkinter.ttk.Button(bottom_panel, text="go to", command=self.__goto)
        self.goto_btn.pack(side="left")
        self.prev_btn = tkinter.ttk.Button(bottom_panel, text="prev", command=self.prev)
        self.prev_btn.pack(side="left")
        self.next_btn = tkinter.ttk.Button(bottom_panel, text="next", command=self.next)
        self.next_btn.pack(side='left')
        bottom_panel.pack(side="top")
        self._img_offset = None
        self._image_list = []
        self._dir_count = 0

    def show_image(self, img):
        if type(img) is int:
            self._show_image_window = imgViewer.ShowImage(self.root, parent=self, _id=img)
        else:
            self._show_image_window = imgViewer.ShowImage(self.root, img)

    def __show_thumbnails(self):
        for i in range(min(len(self._items_list)-self._page*items_per_page, items_per_page)):
            self._items_list[self._page*items_per_page+i].show_thumbnail()

    def __page_rendering(self):
        self.thumbs_wrapper.to_start()
        for widget in self.thumbs_wrapper.interior.winfo_children():
            widget.destroy()
        self.page_count_field.delete(0, tkinter.END)
        self.page_count_field.insert(0, str(self._page+1))
        start = self._page * items_per_page
        _items_per_page = min(len(self._items_list) - start, items_per_page)
        _n = min(n, _items_per_page)
        for i in range(_items_per_page):
            current_item = self._items_list[start+i]
            current_item.create_widget(self.thumbs_wrapper.interior)
            current_item.grid(row=i//n, column=i % n, sticky=tkinter.N)
            current_item.update()
        if _n == 1:
            current_item = self._items_list[0]
            current_item.create_widget(self.thumbs_wrapper.interior)
            current_item.grid(row=0, column=1, sticky=tkinter.N)
            current_item.update()
        threading.Thread(target=self.__show_thumbnails).start()

    def open_dir(self, directory_path):
        os.chdir(directory_path)
        self.root.title(os.getcwd())
        self._items_list = [
            filesystem.directory.ParentDirectory(self),
            filesystem.directory.MatchFilesPattern(self)
        ]
        self._page = 0
        directory_list, file_paths_list = filesystem.browse_current_folder()
        self._dir_count = len(directory_list) + 2
        for directory in directory_list:
            self._items_list.append(filesystem.directory.Directory(self, directory))
        i = 0
        self._image_list = []
        for image_path in file_paths_list:
            self._items_list.append(Image.Image(image_path, self, i))
            self._image_list.append(image_path)
            i += 1
        self._page_count()
        self.__page_rendering()

    def _page_count(self):
        self._page_count_label['text'] = str(ceil((len(self._items_list)) / items_per_page))

    def _extract_mtime_key(self, file:Path):
        return file.stat().st_mtime

    def browse_all_files(self):
        pattern = tkinter.simpledialog.askstring("search pattern", "file match pattern:")
        if len(pattern) == 0:
            return
        self.root.title(os.getcwd()+'*')
        self._items_list = [filesystem.directory.Directory(self, Path('.'))]
        self._page = 0
        self._dir_count = 1
        self._image_list = []
        for file in Path('.').glob(pattern):
            if file.is_file() and file.suffix in filesystem.image_file_extensions:
                self._image_list.append(file)
        self._image_list.sort(key=self._extract_mtime_key, reverse=True)
        i = 0
        for image in self._image_list:
            self._items_list.append(Image.Image(image, self, i))
            #self._image_list.append(image)
            i += 1
        self._page_count()
        self.__page_rendering()

    def next(self):
        if (self._page+1)*items_per_page<len(self._items_list):
            self._page += 1
            self.__page_rendering()

    def prev(self):
        if self._page > 0:
            self._page -= 1
            self.__page_rendering()

    def __goto(self, event=None):
        if unsigned_number_validate.search(self.page_count_field.get()) is not None:
            page = int(re.search(r"\d+", self.page_count_field.get()).group(0))
            if page != self._page-1:
                self._page = page-1
                self.__page_rendering()
        else:
            tkinter.messagebox.showerror('Browser', "invalid page number")

    def get_image_files(self):
        return self._image_list

    def open_page_by_id(self, id):
        self._page = (id+self._dir_count)//items_per_page
        self.__page_rendering()

    def remove_file(self, id):
        self._items_list.pop(id+self._dir_count)
        i=0
        for j in range(self._dir_count, len(self._items_list)):
            self._items_list[j].id = i
            i += 1
        self._page_count()
