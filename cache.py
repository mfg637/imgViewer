import decoders
import PIL.Image
import gui.Image
import io


class ThumbnailsCacheManager:
    def __init__(self):
        self._cache = dict()

    def load_thumbnail(self, abs_path):
        if abs_path in self._cache:
            buffer = io.BytesIO(self._cache[abs_path])
            img = PIL.Image.open(buffer)
            return img
        else:
            source_img = decoders.open_image(str(abs_path), gui.Image.thumbnail_size)
            img = source_img.convert(mode="RGBA")
            source_img.close()
            img.thumbnail(gui.Image.thumbnail_size, PIL.Image.LANCZOS)
            buffer = io.BytesIO()
            img.save(buffer, format="WEBP", lossless=False, quality=90, method=4)
            self._cache[abs_path] = buffer.getvalue()
            buffer.close()
            return img


manager = ThumbnailsCacheManager()