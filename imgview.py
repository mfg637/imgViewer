#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gui
import decoders
import sys
import os

gui_instance = gui.GUI()
gui_instance.open_dir(os.path.dirname(sys.argv[1]))
if os.path.isfile(sys.argv[1]):
    gui_instance.show_image(decoders.open_image(sys.argv[1]))
gui_instance.root.mainloop()
