import cairosvg

import pyimglib_decoders
import PIL.Image
import PIL.ImageChops
import gui.Image
import io
from images import folder_icon_painter
import config
import os
import json
from pathlib import Path


class ThumbnailsCacheManager:
    def __init__(self):
        self._cache = dict()
        self._dir_cache = dict()

    def load_thumbnail(self, abs_path):
        if abs_path in self._cache:
            buffer = io.BytesIO(self._cache[abs_path])
            img = PIL.Image.open(buffer)
            return img
        else:
            source_img = pyimglib_decoders.open_image(str(abs_path), gui.Image.thumbnail_size)
            img = source_img.convert(mode="RGBA")
            source_img.close()
            img.thumbnail(gui.Image.thumbnail_size, PIL.Image.LANCZOS)
            buffer = io.BytesIO()
            img.save(buffer, format="WEBP", lossless=False, quality=90, method=4)
            self._cache[abs_path] = buffer.getvalue()
            buffer.close()
            return img

    def load_folder_thumbnail(self, abs_path, color=None, cover_image=None):
        config_file = os.path.join(abs_path, ".imgview-dir-config.json")
        if abs_path not in self._dir_cache and os.path.exists(config_file):
            with open(config_file, 'r') as f:
                serialized = json.load(f)
                self._dir_cache[abs_path] = {
                    'color': serialized['color'],
                    'thumbnail': None
                }
                if serialized['cover'] is None:
                    self._dir_cache[abs_path]['cover'] = None
                else:
                    self._dir_cache[abs_path]['cover'] = Path(serialized['cover'])
        if color is None and cover_image is None:
            pass
        else:
            if color is not None and cover_image is not None:
                self._dir_cache[abs_path] = {
                    'color': color,
                    'cover': cover_image,
                }
            elif color is not None and cover_image is None:
                if abs_path in self._dir_cache:
                    self._dir_cache[abs_path]['color'] = color
                else:
                    self._dir_cache[abs_path] = {
                        'color': color,
                        'cover': None,
                    }
            elif cover_image is not None and color is None:
                if abs_path in self._dir_cache:
                    self._dir_cache[abs_path]['cover'] = cover_image
                else:
                    self._dir_cache[abs_path] = {
                        'color': None,
                        'cover': cover_image,
                    }
            self._dir_cache[abs_path]['thumbnail'] = None
            with open(config_file, 'w') as f:
                serializable = {
                    "color": self._dir_cache[abs_path]['color'],
                }
                if self._dir_cache[abs_path]['cover'] is None:
                    serializable['cover'] = None
                else:
                    serializable['cover'] = str(self._dir_cache[abs_path]['cover'])
                json.dump(serializable, f)

        if abs_path in self._dir_cache:
            if self._dir_cache[abs_path]['thumbnail'] is None:
                if self._dir_cache[abs_path]['color'] is not None and self._dir_cache[abs_path]['cover'] is None:
                    svg_file = folder_icon_painter.paint_icon(
                        os.path.join(config.app_location, "images/folder icon.svg"),
                        self._dir_cache[abs_path]['color']
                    )
                    self._dir_cache[abs_path]['thumbnail'] = cairosvg.svg2png(bytestring=svg_file)
                    buffer = io.BytesIO(self._dir_cache[abs_path]['thumbnail'])
                    img = PIL.Image.open(buffer)
                    return img
                elif self._dir_cache[abs_path]['cover'] is not None:
                    img = None
                    if self._dir_cache[abs_path]['color'] is not None:
                        svg_file = folder_icon_painter.paint_icon(
                            os.path.join(config.app_location, "images/folder icon blank.svg"),
                            self._dir_cache[abs_path]['color']
                        )
                        img = PIL.Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg_file)))
                    if img is None:
                        img = PIL.Image.open(os.path.join(config.app_location, "images/folder icon blank.png"))
                    cover_thumb = pyimglib_decoders.open_image(
                        Path(abs_path).joinpath(self._dir_cache[abs_path]['cover']),
                        (174, 108)
                    )
                    cover_thumb.thumbnail((174, 108), PIL.Image.LANCZOS)
                    xoffset = (174 - cover_thumb.size[0])//2 + 10
                    yoffset = (108 - cover_thumb.size[1])//2 + 30
                    if cover_thumb.mode == "RGBA":
                        img.paste(cover_thumb, (xoffset, yoffset), cover_thumb)
                    else:
                        img.paste(cover_thumb, (xoffset, yoffset))
                    buffer = io.BytesIO()
                    img.save(buffer, format="PNG")
                    self._dir_cache[abs_path]['thumbnail'] = buffer.getvalue()
                    buffer.close()
                    return img
            else:
                buffer = io.BytesIO(self._dir_cache[abs_path]['thumbnail'])
                img = PIL.Image.open(buffer)
                return img
        else:
            return None



manager = ThumbnailsCacheManager()