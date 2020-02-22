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
THUMBNAIL_WIDTH = 192
items_per_table_row = 4
THUMBS_WRAPPER_HORIZONTAL_MARGIN = 20
THUMBS_WRAPPER_VERTICAL_MARGIN = 30
THUMBS_GRID_PADDING = 72


class GUI:
    def __init__(self):
        self.root = tkinter.Tk()
        self._show_image_window = None
        self.root.geometry("840x530")
        self._width = 840
        self._height = 530
        filesystem.directory.init()
        Image.init()
        imgViewer.init()
        self.thumbs_wrapper = ScrolledFrame.VerticalScrolledFrame(
            self.root,
            width=self._width - THUMBS_WRAPPER_HORIZONTAL_MARGIN,
            height=self._height - THUMBS_WRAPPER_VERTICAL_MARGIN
        )
        self.thumbs_wrapper.pack(side="top")
        self._items_list = []
        self._page = 0
        bottom_panel = tkinter.Frame(self.root)
        tkinter.ttk.Button(
            bottom_panel,
            text="parent dir",
            command=lambda: self.open_dir('..')
        ).pack(side="left")
        tkinter.Label(bottom_panel, text="Page: ").pack(side="left")
        self.page_count_field = tkinter.Entry(bottom_panel, width=5)
        self.page_count_field.pack(side="left")
        self.page_count_field.bind("<Return>", self.__goto)
        self.page_count_field.bind("<KP_Enter>", self.__goto)
        tkinter.Label(bottom_panel, text="of ").pack(side="left")
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
        self.root.bind("<Configure>", self._resize)
        self._resize_timer = None

    def _resize(self, event):
        global items_per_table_row
        if self.root.winfo_width() != self._width or self.root.winfo_height() != self._height:
            try:
                self.root.after_cancel(self._resize_timer)
            except ValueError:
                pass
            self._width = self.root.winfo_width()
            self._height = self.root.winfo_height()
            self.thumbs_wrapper.resize(
                width=self._width - THUMBS_WRAPPER_HORIZONTAL_MARGIN,
                height=self._height - THUMBS_WRAPPER_VERTICAL_MARGIN
            )
            items_per_table_row = (self._width - THUMBS_GRID_PADDING) // THUMBNAIL_WIDTH
            self._resize_timer = self.root.after(500, self.__page_rendering)

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
        for i in range(_items_per_page):
            current_item = self._items_list[start+i]
            current_item.create_widget(self.thumbs_wrapper.interior)
            current_item.grid(row=i // items_per_table_row, column=i % items_per_table_row, sticky=tkinter.N)
            current_item.update()
        if items_per_page == 1:
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

    @staticmethod
    def _extract_mtime_key(file:Path):
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
            i += 1
        self._page_count()
        self.__page_rendering()

    def next(self):
        if (self._page+1)*items_per_page < len(self._items_list):
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

    def open_page_by_id(self, image_id):
        self._page = (image_id + self._dir_count) // items_per_page
        self.__page_rendering()

    def remove_file(self, image_id):
        self._items_list.pop(image_id + self._dir_count)
        i = 0
        for j in range(self._dir_count, len(self._items_list)):
            self._items_list[j].id = i
            i += 1
        self._page_count()
