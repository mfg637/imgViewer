#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import tkinter
import abc


class SomeFile:
    """
        Base class of any filesystem object, who tan ge displayed on grid
        self._parent must be instance of class GUI
        self._wrapper its a tkinter.Frame object
    """
    __metaclass__ = abc.ABCMeta

    def grid(self, **kwargs):
        self._wrapper.grid(**kwargs)

    def update(self):
        self._wrapper.update()

    def show_thumbnail(self):
        pass

    def _create_widget(self, root, img_icon, name, bind, right_click_bind = None, *pargs, **kwargs):
        self._wrapper = tkinter.Frame(root, *pargs, **kwargs)
        self._icon = tkinter.Label(self._wrapper, image=img_icon)
        self._icon.pack(side="top")
        self._file_name_label = tkinter.Label(
            self._wrapper,
            text=name,
            width=25,
            wraplength=192
        )
        self._file_name_label.pack(side="top")
        self._wrapper.bind("<Double-Button-1>", bind)
        self._icon.bind("<Double-Button-1>", bind)
        self._file_name_label.bind("<Double-Button-1>", bind)
        if right_click_bind is not None:
            self._wrapper.bind("<Button-3>", right_click_bind)
            self._icon.bind("<Button-3>", right_click_bind)
            self._file_name_label.bind("<Button-3>", right_click_bind)

    @abc.abstractmethod
    def create_widget(self, root, *pargs, **kwargs):
        pass
