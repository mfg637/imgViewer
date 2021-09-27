import os
import pyimglib

app_location = os.path.dirname(os.path.realpath(__file__))

pyimglib.YUV4MPEG2.limited_range_correction = \
    pyimglib.YUV4MPEG2.LIMITED_RANGE_CORRENTION_MODES.CLIPPING

# needs to decode JPEG XL images
pyimglib.jpeg_xl.PATH_TO_REFERENCE_DECODER = None

ACLMMP_COMPATIBILITY_LEVEL = 3

AUDIO_CHANNELS = 2
