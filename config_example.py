import os
import pyimglib_decoders

app_location = os.path.dirname(os.path.realpath(__file__))

pyimglib_decoders.YUV4MPEG2.limited_range_correction = \
    pyimglib_decoders.YUV4MPEG2.LIMITED_RANGE_CORRENTION_MODES.CLIPPING

# needs to decode JPEG XL images
pyimglib_decoders.jpeg_xl.PATH_TO_REFERENCE_DECODER = None
