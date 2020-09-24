#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import os
import sys
import json

from wmctrl_window import WmctrlWindow

# wmctrlWindow = WmctrlWindow("0x02a00136  1 0    473  3840 2137 xavier Tilix: teste")
# sys.exit()

# def ls_window
outt = os.popen('wmctrl -dliGu').read()
lines = outt.split("\n")
lines.pop()

windows = []
for line in lines:
  windows.append(WmctrlWindow(line))

windows.sort(key=lambda x: x.monitor, reverse=False)
# end

# def current_window
outt = os.popen('/home/danilo/scripts/get_current_window.sh').read()
current_window_id = outt.replace(',', '').split('x')[1]
current_window_id = re.sub(r'(\r\n\t|\n|\r\t|\n)', '', current_window_id)

current_window = None
for line in lines:
  if line.find(current_window_id) >= 0:
    current_window = WmctrlWindow(line)

# end

next_monitor = current_window.monitor
next_windows = []

str_json = open("/home/danilo/scripts/flip360_wids.json", "r").read()
jjson = json.loads(str_json)

next_windows = filter(lambda window: window.monitor == current_window.monitor and window.workspace == current_window.workspace and window.valid, windows)

# buscar o idx da minha janela
idx = 0
for window in next_windows:
  if window.id == current_window.id:
    break
  idx = idx + 1

type_cycle = sys.argv[1]
if(type_cycle == 'up'):
  idx = idx - 1
  if(idx == -1):
    idx = len(next_windows) - 1
else:
  idx = idx + 1
  if(idx >= len(next_windows)):
    idx = 0

next_window = next_windows[idx]
key_json = 'm{m}{w}'.format(m=next_window.monitor, w=current_window.workspace)
jjson[key_json] = next_window.str_win

flip360 = open("/home/danilo/scripts/flip360_wids.json", "w")
flip360.write(json.dumps(jjson))
flip360.close()

next_window.set_focus()
script = '/home/danilo/scripts/dmenu/dzen_monitor.sh'
os.popen("{script} {monitor} '{title}'".format(script=script, monitor=current_window.monitor, title=next_window.name)).read()
sys.exit()
