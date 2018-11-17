from PIL import Image, ImageFile
import ffmpeg
import subprocess
import io


def _accept(prefix):
    return prefix[:5] == b"\x1a\x45\xdf\xa3\x01"


class WebM_Video(ImageFile.ImageFile):

    format = "WEBM"
    format_description = "WebM video file"

    def _open(self):
        self._current_frame = 0

        data = ffmpeg.probe(self.filename)
        print(data)

        if data['format']['format_name'] != "matroska,webm":
            raise SyntaxError("not a WEBM file")

        video = None
        for stream in data['streams']:
            if stream['codec_type'] == "video":
                video = stream
        fps = eval(video['r_frame_rate'])
        self.info['duration'] = int(round(1 / fps * 1000))
        print(video["width"], video["height"])
        self._size = (video["width"], video["height"])

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
        self.process = subprocess.Popen(commandline, stdout=subprocess.PIPE)
        self._frame_size = self.size[0]*self.size[1]*3
        self.info['duration_of_video'] = float(data['format']['duration'])
        if 30 >= self.info['duration_of_video']:
            self._exclusive_fp = None
            self.info['loop'] = 0
            tmpbuf = self.process.stdout.read()
            self.raw_data_len = len(tmpbuf)
            self.raw_data_buf = io.BytesIO(tmpbuf)
            self.raw_data_buf.seek(0)
            self.fp = io.BytesIO(self.raw_data_buf.read(self._frame_size))
        else:
            self.info['loop'] = 1
            self.raw_data_len = self._frame_size
            self.fp = io.BytesIO(self.process.stdout.read(self.raw_data_len))
        self._n_frames = self.raw_data_len // self._frame_size

    @property
    def n_frames(self):
        return self._n_frames

    @property
    def is_animated(self):
        return self._n_frames > 1

    def seek(self, frame):
        if frame >= self._n_frames or frame < 0:
            raise EOFError

        self.raw_data_buf.seek(self._frame_size * frame)
        self.fp = io.BytesIO(self.raw_data_buf.read(self._frame_size))
        self.tile = [
            ("raw", (0, 0) + self.size, 0, (self.mode, 0, 1))
        ]
        self.load()

        self._current_frame = frame

    def tell(self):
        return self._current_frame


Image.register_open(WebM_Video.format, WebM_Video, _accept)

Image.register_extension(WebM_Video.format, ".webm")
