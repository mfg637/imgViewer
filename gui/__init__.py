#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import PIL.Image
from PIL import ImageTk
import tkinter
import tkinter.ttk
from tkinter import messagebox
from . import ScrolledFrame
import os
import filesystem
from . import Image
import re
from math import ceil
import threading
import decoders

unsigned_number_validate = re.compile(r"^\s*\d+\s*$")
items_per_page = 52
n = 4


class ShowImage:
    def __init__(self, root, img, parent=None, _id=None, width=1280, height=720):
        self._root = tkinter.Toplevel(root)
        self._img = img
        self._image = None
        self._width = None
        self._height = None
        self.image_label = tkinter.Label(self._root)
        self.image_label.pack()
        self.__show(width, height)
        self._root.attributes("-topmost", True)
        self._root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self._root.bind("<Configure>", self.resize)
        if parent is not None:
            self._id = _id
            self.image_list = parent.get_image_files()
            self._root.bind("<Left>", self.__prev)
            self._root.bind("<Right>", self.__next)
        else:
            self._id = None
            self.image_list = None

    def on_closing(self):
        self._img.close()
        self._root.destroy()

    def resize(self, event):
        if event.width != self._width or event.height != self._height:
            self.__show(event.width, event.height)

    def __show(self, width, height):
        scaled_img = self._img.copy()
        scaled_img.thumbnail((width, height), PIL.Image.LANCZOS)
        self._image = ImageTk.PhotoImage(scaled_img)
        self._root.geometry("{}x{}".format(*scaled_img.size))
        self._width = scaled_img.size[0]
        self._height = scaled_img.size[1]
        self.image_label['image'] = self._image
        self.image_label.pack()

    def __prev(self, event):
        if self._id > 0:
            self._id -= 1
            self._img = decoders.open_image(str(self.image_list[self._id]))
            self.__show(
                self._root.winfo_screenwidth(),
                self._root.winfo_screenheight()
            )

    def __next(self, event):
        if self._id < len(self.image_list)-1:
            self._id += 1
            self._img = decoders.open_image(str(self.image_list[self._id]))
            self.__show(
                self._root.winfo_screenwidth(),
                self._root.winfo_screenheight()
            )


class GUI:
    def __init__(self):
        self.root = tkinter.Tk()
        self._show_image_window = None
        self.root.geometry("840x730")
        filesystem.directory.init()
        Image.init()
        self.thumbs_wrapper = ScrolledFrame.VerticalScrolledFrame(self.root, width=820, height=700)
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

    def show_image(self, img, id=None):
        if id is not None:
            self._show_image_window = ShowImage(self.root, img, self, id)
        else:
            self._show_image_window = ShowImage(self.root, img)

    def __show_thumbnails(self):
        for i in range(min(len(self._items_list)-self._page*items_per_page, items_per_page)):
            self._items_list[self._page*items_per_page+i].show_thumbnail()

    def __page_rendering(self):
        self.thumbs_wrapper.to_start()
        for widget in self.thumbs_wrapper.interior.winfo_children():
            widget.destroy()
        self.page_count_field.delete(0, tkinter.END)
        self.page_count_field.insert(0, str(self._page+1))
        for i in range(min(len(self._items_list)-self._page*items_per_page, items_per_page)):
            current_item = self._items_list[self._page*items_per_page+i]
            current_item.create_widget(self.thumbs_wrapper.interior)
            current_item.grid(row=i//n, column=i % n, sticky=tkinter.N)
            current_item.update()
        threading.Thread(target=self.__show_thumbnails).start()

    def open_dir(self, directory_path):
        os.chdir(directory_path)
        self.root.title(os.getcwd())
        self._items_list = []
        self._page = 0
        self._items_list.append(filesystem.directory.ParentDirectory(self))
        directory_list, file_paths_list = filesystem.browse_current_folder()
        for directory in directory_list:
            self._items_list.append(filesystem.directory.Directory(self, directory))
        i = 0
        self._image_list = []
        for image_path in file_paths_list:
            self._items_list.append(Image.Image(image_path, self, i))
            self._image_list.append(image_path)
            i += 1
        self._page_count_label['text'] = str(ceil((len(self._items_list)-1)/items_per_page))
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
