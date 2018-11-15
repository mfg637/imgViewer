from PIL import Image, ImageFile
import ffmpeg
import subprocess
import time


def _accept(prefix):
    return prefix[:5] == b"\x1a\x45\xdf\xa3\x01"


class WebM_Video(ImageFile.ImageFile):

    format = "WEBM"
    format_description = "WebM video file"

    def _open(self):
        # self.fp.close()

        self._frames = []

        # size in pixels (width, height)
        data = ffmpeg.probe(self.filename)

        if data['format']['format_name'] != "matroska,webm":
            raise SyntaxError("not a WEBM file")

        self.info['loop'] = 0

        video = None
        for stream in data['streams']:
            if stream['codec_type'] == "video":
                video = stream
        fps = eval(video['r_frame_rate'])
        self.info['duration'] = int(round(1 / fps * 1000))
        self.size = (video["width"], video["height"])

        self.mode = "RGB"

        self.tile = [
            ("raw", (0, 0) + self.size, 0, (self.mode, 0, 1))
        ]

        commandline = ['ffmpeg',
                       '-i', self.filename,
                       '-f', 'image2pipe',
                       '-pix_fmt', 'rgb24',
                       '-an',
                       '-vcodec', 'rawvideo', '-']
        print(commandline)
        self.process = subprocess.Popen(commandline, stdout=subprocess.PIPE)
        self.fp.close()
        self._exclusive_fp = None
        self.fp = self.process.stdout


Image.register_open(WebM_Video.format, WebM_Video, _accept)

Image.register_extension(WebM_Video.format, ".webm")
