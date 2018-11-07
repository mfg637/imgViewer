#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gui
import decoders
import sys

gui_instance = gui.GUI()
gui_instance.show_image(decoders.open_image(sys.argv[1]))
gui_instance.root.mainloop()
