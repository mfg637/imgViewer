#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABCMeta


class SomeFile:
    """
        Base class of any filesystem object, who tan ge displayed on grid
        self._parent must be instance of class GUI
        self._wrapper its a tkinter.Frame object
    """
    __metaclass__ = ABCMeta

    def grid(self, **kwargs):
        self._wrapper.grid(**kwargs)

    def update(self):
        self._wrapper.update()

    def show_thumbnail(self):
        pass
