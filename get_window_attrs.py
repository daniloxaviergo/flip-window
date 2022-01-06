#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import os
import sys
import json

from wmctrl_window import WmctrlWindow

wid = sys.argv[1]

outt = os.popen("wmctrl -dliGux | grep {wid}".format(wid=wid)).read()
lines = outt.split("\n")
lines.pop()

window = WmctrlWindow(lines[0])
print("{monitor} {workspace} {title}".format(monitor=window.monitor, workspace=window.workspace, title=window.name))
sys.exit()
