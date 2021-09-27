#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gui
import pyimglib
import sys
import os

from multiprocessing import cpu_count
pyimglib.config.avifdec_workers_count = cpu_count()

gui_instance = gui.GUI()
if len(sys.argv) > 1 and os.path.isfile(sys.argv[1]):
    gui_instance.open_dir(os.path.dirname(sys.argv[1]))
    gui_instance.show_image(pyimglib.decoders.open_image(sys.argv[1]))
elif len(sys.argv) > 1 and os.path.isdir(sys.argv[1]):
    gui_instance.open_dir(sys.argv[1])
else:
    gui_instance.open_dir(os.path.dirname(sys.argv[0]))
gui_instance.root.mainloop()
