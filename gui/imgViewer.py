#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter
import PIL.Image
from PIL import ImageTk
import threading
import decoders
import sys
import os

width = 1280
height = 720

left_arrow_img = None
right_arrow_img = None
left_arrow_active_img = None
right_arrow_active_img = None
close_btn_default = None
close_btn_active = None


def init():
    global left_arrow_img
    global right_arrow_img
    global left_arrow_active_img
    global right_arrow_active_img
    global close_btn_default
    global close_btn_active
    img = PIL.Image.open(os.path.join(
        os.path.dirname(sys.argv[0]),
        "images",
        "arrow.png"
    ))
    right_arrow_img = ImageTk.PhotoImage(img)
    left_arrow_img = ImageTk.PhotoImage(img.transpose(PIL.Image.FLIP_LEFT_RIGHT))
    img.close()
    img = PIL.Image.open(os.path.join(
        os.path.dirname(sys.argv[0]),
        "images",
        "arrow_active.png"
    ))
    right_arrow_active_img = ImageTk.PhotoImage(img)
    left_arrow_active_img = ImageTk.PhotoImage(img.transpose(PIL.Image.FLIP_LEFT_RIGHT))
    img.close()
    img = PIL.Image.open(os.path.join(
        os.path.dirname(sys.argv[0]),
        "images",
        "close_btn_default.png"
    ))
    close_btn_default = ImageTk.PhotoImage(img)
    img.close()
    img = PIL.Image.open(os.path.join(
        os.path.dirname(sys.argv[0]),
        "images",
        "close_btn_active.png"
    ))
    close_btn_active = ImageTk.PhotoImage(img)
    img.close()


class ShowImage:
    def __init__(self, root, img, parent=None, _id=None):
        global width
        global height
        self._root = tkinter.Toplevel(root, background="black")
        self._root.attributes("-fullscreen", True)
        width = self._root.winfo_screenwidth()
        height = self._root.winfo_screenheight()
        self._img = img
        self._image = None
        self._canvas_img = None
        self._prev_img_btn = None
        self._next_img_btn = None
        self._close_btn = None
        self._canvas = tkinter.Canvas(self._root, background="black", highlightthickness=0)
        self._canvas.pack()
        self._canvas.bind("<Double-Button-1>", self.on_closing)
        self._left_arrow_active = False
        self._right_arrow_active = False
        self._close_btn_active = False
        self._controls_visible = True
        self.__show()
        self._root.attributes("-topmost", True)
        self._root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self._root.bind("<Configure>", self.resize)
        self._root.bind("<Escape>", self.on_closing)
        if parent is not None:
            self._id = _id
            self.image_list = parent.get_image_files()
            self._root.bind("<Left>", self.__prev)
            self._root.bind("<Right>", self.__next)
        else:
            self._id = None
            self.image_list = None
        self._root.focus()
        self._hide_cursor_timer = None
        self._cursor_visible = True

    def on_closing(self, event=None):
        self._img.close()
        self._root.destroy()

    def resize(self, event):
        global width
        global height
        if event.width != self._root.winfo_width() \
                or event.height != self._root.winfo_height():
            print(event.width, event.height)
            width = event.width
            height = event.height
            self.__show()

    def __show(self):

        if self._prev_img_btn is not None:
            self._canvas.delete(self._prev_img_btn)
            self._canvas.delete(self._next_img_btn)
            self._canvas.delete(self._close_btn)
        scaled_img = self._img.copy()
        scaled_img.thumbnail((width, height), PIL.Image.LANCZOS)
        self._root.geometry("{}x{}".format(width, height))
        self._image = ImageTk.PhotoImage(scaled_img)
        self._canvas['width'] = width
        self._canvas['height'] = height
        self._canvas_img = self._canvas.create_image(
            int((width - scaled_img.width) / 2),
            int((height - scaled_img.height) / 2),
            anchor=tkinter.NW,
            image=self._image
        )
        if self._controls_visible:
            if self._left_arrow_active:
                self.__draw_prev_btn_active()
            else:
                self.__draw_prev_btn_default()
            if self._right_arrow_active:
                self.__draw_next_btn_active()
            else:
                self.__draw_next_btn_default()
            self.__draw_close_btn_default()
        self._canvas.bind("<Motion>", self.mouse_move)
        self._canvas.bind("<Button-1>", self.on_click)

    def __prev(self, event=None):
        if self._id > 0:
            self._id -= 1
            self._img = decoders.open_image(str(self.image_list[self._id]))
            self.__show()

    def __next(self, event=None):
        if self._id < len(self.image_list) - 1:
            self._id += 1
            self._img = decoders.open_image(str(self.image_list[self._id]))
            self.__show()

    def mouse_move(self, event):
        if self._controls_visible:
            if 8 <= event.x <= 72 and \
                    (height / 2 - 16) <= event.y <= (height / 2 + 16):
                if not self._left_arrow_active:
                    self._canvas.delete(self._prev_img_btn)
                    self._left_arrow_active = True
                    self.__draw_prev_btn_active()
                    self._root['cursor'] = 'hand2'
                return None
            if self._left_arrow_active:
                self._left_arrow_active = False
                self._canvas.delete(self._prev_img_btn)
                self.__draw_prev_btn_default()
            if (self._root.winfo_screenwidth() - 72) <= event.x <= \
                    (self._root.winfo_screenwidth() - 8) and \
                    (height / 2 - 16) <= event.y <= (height / 2 + 16):
                if not self._right_arrow_active:
                    self._right_arrow_active = True
                    self._canvas.delete(self._next_img_btn)
                    self.__draw_next_btn_active()
                    self._root['cursor'] = 'hand2'
                return None
            if self._right_arrow_active:
                self._right_arrow_active = False
                self._canvas.delete(self._next_img_btn)
                self.__draw_next_btn_default()
            if (self._root.winfo_screenwidth() - 32) <= event.x <= self._root.winfo_screenwidth() and \
                    0 <= event.y < 32:
                if not self._close_btn_active:
                    self._close_btn_active = True
                    self._canvas.delete(self._close_btn)
                    self.__draw_close_btn_active()
                    self._root['cursor'] = 'hand2'
                return None
            if self._close_btn_active:
                self._close_btn_active = False
                self._canvas.delete(self._close_btn)
                self.__draw_close_btn_default()
            self._root['cursor'] = 'arrow'
        else:
            if self._hide_cursor_timer is not None:
                self._root.after_cancel(self._hide_cursor_timer)
            if not self._controls_visible:
                self._root['cursor'] = 'arrow'
            self._root.after(1000, self.__hide_cursor)

    def on_click(self, event):
        if self._left_arrow_active:
            self.__prev()
        elif self._right_arrow_active:
            self.__next()
        elif self._close_btn_active:
            self.on_closing()
        else:
            if self._controls_visible:
                self._controls_visible = False
                self._canvas.delete(self._prev_img_btn)
                self._canvas.delete(self._next_img_btn)
                self._canvas.delete(self._close_btn)
                self._root['cursor'] = 'arrow'
                self._hide_cursor_timer = self._root.after(1000, self.__hide_cursor)
            else:
                self._controls_visible = True
                self.__draw_prev_btn_default()
                self.__draw_next_btn_default()
                self.__draw_close_btn_default()
                self._root.after_cancel(self._hide_cursor_timer)
                self._root['cursor'] = 'arrow'

    def __draw_prev_btn_default(self):
        self._prev_img_btn = self._canvas.create_image(
            8,
            int(height / 2 - 16),
            anchor=tkinter.NW,
            image=left_arrow_img
        )

    def __draw_prev_btn_active(self):
        self._prev_img_btn = self._canvas.create_image(
            8,
            int(height / 2 - 16),
            anchor=tkinter.NW,
            image=left_arrow_active_img
        )

    def __draw_next_btn_default(self):
        self._next_img_btn = self._canvas.create_image(
            self._root.winfo_screenwidth() - 72,
            int(height / 2 - 16),
            anchor=tkinter.NW,
            image=right_arrow_img
        )

    def __draw_next_btn_active(self):
        self._next_img_btn = self._canvas.create_image(
            self._root.winfo_screenwidth() - 72,
            int(height / 2 - 16),
            anchor=tkinter.NW,
            image=right_arrow_active_img
        )

    def __draw_close_btn_default(self):
        self._close_btn = self._canvas.create_image(
            self._root.winfo_screenwidth() - 32,
            0,
            anchor=tkinter.NW,
            image=close_btn_default
        )

    def __draw_close_btn_active(self):
        self._close_btn = self._canvas.create_image(
            self._root.winfo_screenwidth() - 32,
            0,
            anchor=tkinter.NW,
            image=close_btn_active
        )

    def __hide_cursor(self):
        self._root['cursor'] = 'none'
