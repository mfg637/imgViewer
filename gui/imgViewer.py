#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess
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
spinner = []
spinner_duration = 0
spinner_x_cords = None
spinner_y_cords = None


def init():
    global left_arrow_img
    global right_arrow_img
    global left_arrow_active_img
    global right_arrow_active_img
    global close_btn_default
    global close_btn_active
    global spinner
    global spinner_duration
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
    img = PIL.Image.open(os.path.join(
        os.path.dirname(sys.argv[0]),
        "images",
        "Spinner-1s-200px.webp"
    ))
    try:
        while(True):
            spinner.append(ImageTk.PhotoImage(img))
            img.seek(img.tell()+1)
    except EOFError:
        spinner_duration = img.info['duration']
    img.close()


class ButtonImage:
    def __init__(self, root, canvas, default_image, active_image,
                 x_offset, y_offset, predicate, on_click, visibility=True):
        self._root = root
        self._canvas = canvas
        self._default_image = default_image
        self._active_image = active_image,
        self._x_offset = x_offset
        self._y_offset = y_offset
        self._predicate = predicate
        self._is_active = False
        self.is_visible = visibility
        self._button = None
        self._on_click = on_click

    def __draw_default(self):
        self._button = self._canvas.create_image(
            self._x_offset(),
            self._y_offset(),
            anchor=tkinter.NW,
            image=self._default_image
        )

    def __draw_active(self):
        self._button = self._canvas.create_image(
            self._x_offset(),
            self._y_offset(),
            anchor=tkinter.NW,
            image=self._active_image
        )

    def update(self, x_cords, y_cords):
        if self.is_visible:
            if self._predicate(x_cords, y_cords):
                if not self._is_active:
                    self._canvas.delete(self._button)
                    self._is_active = True
                    self.__draw_active()
                    self._root['cursor'] = 'hand2'
            elif self._is_active:
                self._is_active = False
                self._canvas.delete(self._button)
                self.__draw_default()
        return self._is_active

    def redraw(self):
        if self._button is not None:
            self._canvas.delete(self._button)
        if self.is_visible:
            if self._is_active:
                self.__draw_active()
            else:
                self.__draw_default()
        else:
            self._button = None

    def click_event(self):
        if self._is_active:
            self._on_click()
        return self._is_active


class ShowImage:
    def __init__(self, root, img=None, parent=None, _id=None):
        global spinner_x_cords
        global spinner_y_cords
        global width
        global height
        self._root = tkinter.Toplevel(root, background="black")
        self._root.attributes("-fullscreen", True)
        spinner_x_cords = self._root.winfo_screenwidth() / 2 - 100
        spinner_y_cords = self._root.winfo_screenheight() / 2 - 100
        width = self._root.winfo_screenwidth()
        height = self._root.winfo_screenheight()
        self._read_done = False
        self._canvas = tkinter.Canvas(self._root, background="black", highlightthickness=0)
        self._canvas.pack()
        self._canvas.bind("<Double-Button-1>", self.mouse_double_click)
        self._spinner_frame = -1
        self._spinner_image = None
        self._img = img
        self._image = None
        self._canvas_img = None
        self._frames = []
        self._current_frame = 0
        self._buttons = [
            ButtonImage(
                self._root,
                self._canvas,
                left_arrow_img,
                left_arrow_active_img,
                lambda: 8,
                lambda: int(height / 2 - 16),
                lambda x, y: 8 <= x <= 72 and \
                             (height / 2 - 16) <= y <= (height / 2 + 16),
                self.__prev
            ),
            ButtonImage(
                self._root,
                self._canvas,
                right_arrow_img,
                right_arrow_active_img,
                lambda: self._root.winfo_screenwidth() - 72,
                lambda: int(height / 2 - 16),
                lambda x, y: (self._root.winfo_screenwidth() - 72) <= x <= \
                             (self._root.winfo_screenwidth() - 8) and \
                             (height / 2 - 16) <= y <= (height / 2 + 16),
                self.__next
            ),
            ButtonImage(
                self._root,
                self._canvas,
                close_btn_default,
                close_btn_active,
                lambda: self._root.winfo_screenwidth() - 32,
                lambda: 0,
                lambda x, y: (self._root.winfo_screenwidth() - 32) <= x <= self._root.winfo_screenwidth() and \
                             0 <= y < 32,
                self.on_closing
            )
        ]
        self._controls_visible = True
        self._animation_tick = None
        self._parent = parent
        if parent is not None:
            self._id = _id
            self.image_list = parent.get_image_files()
            self._root.bind("<Left>", self.__prev)
            self._root.bind("<Right>", self.__next)
        else:
            self._id = None
            self.image_list = None
        #self.__show(img)
        self._root.attributes("-topmost", True)
        self._root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self._root.bind("<Escape>", self.on_closing)
        self._root.focus()
        self._hide_cursor_timer = None
        self._cursor_visible = True
        self._canvas['width'] = width
        self._canvas['height'] = height
        threading.Thread(target=self.draw_spinner).start()
        threading.Thread(target=self.__show, args=(img,)).start()

    def mouse_double_click(self):
        has_active_button = False
        for button in self._buttons:
            active = button.click_event()
            if active:
                has_active_button = True
        if not has_active_button:
            self.on_closing()

    def on_closing(self, event=None):
        if self._parent is not None and self._id is not None:
            self._parent.open_page_by_id(self._id)
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

    def __show(self, img=None):
        self._read_done = False
        if self._animation_tick is not None:
            self._root.after_cancel(self._animation_tick)
        if img is None:
            self._img = decoders.open_image(
                str(self.image_list[self._id]),
                (width, height)
            )
        else:
            self._img = img
        if 'duration_of_video' in self._img.info and self._img.info['duration_of_video'] >30:
            subprocess.Popen(['mpv', self._img.filename])
            self.on_closing()
        self._frames = []
        self._frames_duration = []
        scaled_img = self._img.convert(mode='RGBA')
        scaled_img.thumbnail((width, height), PIL.Image.LANCZOS)
        self._root.geometry("{}x{}".format(width, height))
        self._image = ImageTk.PhotoImage(scaled_img)
        self._frames.append(self._image)
        self._canvas_img = self._canvas.create_image(
            int((width - scaled_img.width) / 2),
            int((height - scaled_img.height) / 2),
            anchor=tkinter.NW,
            image=self._image
        )
        if self._controls_visible:
            for button in self._buttons:
                button.is_visible = True
                button.redraw()
        self._canvas.bind("<Motion>", self.mouse_move)
        self._canvas.bind("<Button-1>", self.on_click)
        if self._img.format == 'WEBP' and self._img.is_animated:
            self._frames_duration = \
                decoders.webp.get_frames_duration(str(self.image_list[self._id]))
        if 'loop' in self._img.info and self._img.info['loop'] != 1:
            if isinstance(self._img.info['duration'], (list, tuple)):
                self._animation_tick = self._root.after(
                    self._img.info['duration'][self._img.tell()],
                    self.__frame_update
                )
            elif self._img.info['duration'] > 0:
                self._animation_tick = self._root.after(
                    self._img.info['duration'],
                    self.__frame_update
                )
            else:
                self._animation_tick = self._root.after(
                    67,
                    self.__frame_update
                )
        else:
            self._read_done = True

    def __prev(self, event=None):
        if self._id > 0:
            self._id -= 1
            self._read_done = False
            threading.Thread(target=self.draw_spinner).start()
            threading.Thread(target=self.__show).start()

    def __next(self, event=None):
        if self._id < len(self.image_list) - 1:
            self._id += 1
            self._read_done = False
            threading.Thread(target=self.draw_spinner).start()
            threading.Thread(target=self.__show).start()

    def mouse_move(self, event):
        if self._controls_visible:
            has_active_button = False
            for button in self._buttons:
                active = button.update(event.x, event.y)
                if active:
                    has_active_button = True
            if not has_active_button:
                self._root['cursor'] = 'arrow'
        else:
            if self._hide_cursor_timer is not None:
                self._root.after_cancel(self._hide_cursor_timer)
            if not self._controls_visible:
                self._root['cursor'] = 'arrow'
            self._root.after(1000, self.__hide_cursor)

    def on_click(self, event):
        has_active_button = False
        for button in self._buttons:
            active = button.click_event()
            if active:
                has_active_button = True

        if not has_active_button:
            if self._controls_visible:
                self._controls_visible = False
                for button in self._buttons:
                    button.is_visible = False
                    button.redraw()
                self._root['cursor'] = 'arrow'
                self._hide_cursor_timer = self._root.after(1000, self.__hide_cursor)
            else:
                self._controls_visible = True
                for button in self._buttons:
                    button.is_visible = True
                    button.redraw()
                self._root.after_cancel(self._hide_cursor_timer)
                self._root['cursor'] = 'arrow'

    def __hide_cursor(self):
        self._root['cursor'] = 'none'

    def __frame_update(self):
        if self._read_done:
            self._image = self._frames[self._current_frame]
            self._current_frame +=1
            if self._current_frame >= len(self._frames):
                self._current_frame = 0
        else:
            try:
                self._img.seek(self._img.tell() + 1)
            except EOFError:
                self._img.seek(0)
                self._read_done = True
                self._current_frame = 0
            scaled_img = self._img.convert(mode='RGBA')
            scaled_img.thumbnail((width, height), PIL.Image.LANCZOS)
            self._image = ImageTk.PhotoImage(scaled_img)
            if self._img.tell() >= len(self._frames):
                self._frames.append(self._image)
            self._img_width = scaled_img.width
            self._img_height = scaled_img.height
        self._canvas.delete(self._canvas_img)
        self._canvas_img = self._canvas.create_image(
            int((width - self._img_width) / 2),
            int((height - self._img_height) / 2),
            anchor=tkinter.NW,
            image=self._image
        )
        if self._img.format == 'WEBP' and self._read_done:
            if self._frames_duration[self._current_frame]>0:
                self._animation_tick = self._root.after(
                    self._frames_duration[self._current_frame],
                    self.__frame_update
                )
            else:
                self._animation_tick = self._root.after(
                    67,
                    self.__frame_update
                )
        elif self._read_done and isinstance(self._img.info['duration'], (list, tuple)):
            self._animation_tick = self._root.after(
                self._img.info['duration'][self._current_frame],
                self.__frame_update
            )
        else:
            if isinstance(self._img.info['duration'], (list, tuple)):
                self._animation_tick = self._root.after(
                    self._img.info['duration'][self._img.tell()],
                    self.__frame_update
                )
            elif 'duration' in self._img.info and self._img.info['duration'] > 0:
                self._animation_tick = self._root.after(
                    self._img.info['duration'],
                    self.__frame_update
                )
            elif 'duration' in self._img.info:
                self._animation_tick = self._root.after(
                    67,
                    self.__frame_update
                )
            else:
                threading.Thread(target=self.__frame_update).start()
        if self._controls_visible:
            for button in self._buttons:
                button.is_visible = True
                button.redraw()
        self.draw_spinner(nextFrame=False)

    def draw_spinner(self, nextFrame=True):
        if self._spinner_frame < 0 and not nextFrame:
            return
        if self._spinner_image is not None:
            self._canvas.delete(self._spinner_image)
        if not self._read_done:
            if nextFrame:
                self._spinner_frame += 1
                if self._spinner_frame >= 30:
                    self._spinner_frame = 0
            self._spinner_image = self._canvas.create_image(
                spinner_x_cords,
                spinner_y_cords,
                anchor=tkinter.NW,
                image=spinner[self._spinner_frame]
            )
            self._canvas.update_idletasks()
            if nextFrame:
                self._root.after(spinner_duration, self.draw_spinner)
        else:
            self._spinner_image = None
            self._spinner_frame = 0
