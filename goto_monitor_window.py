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

# primeiro next_monitor

# descobrir qual é o próximo monitor
# se o próximo não tiver janela ir para o próximo

next_monitor = current_window.monitor
next_windows = []

# buscar no json se há alguma window para esse monitor
# se tiver validar se ela ainda existe senão 
# executar o restante
str_json = open("/home/danilo/scripts/flip360_wids.json", "r").read()
jjson = json.loads(str_json)

key_json = ''
type_cycle = sys.argv[1]
if type_cycle == 'next':
  if (next_monitor + 1 == 5):
    key_json = 'm1{w}'.format(w=current_window.workspace)
  else:
    key_json = 'm{m}{w}'.format(m=(next_monitor + 1), w=current_window.workspace)
else:
  if (next_monitor - 1 == 0):
    key_json = 'm5{w}'.format(w=current_window.workspace)
  else:
    key_json = 'm{m}{w}'.format(m=(next_monitor - 1), w=current_window.workspace)

next_window = jjson.get(key_json)

outt = os.popen('/home/danilo/scripts/get_visible_windows.sh').read()
visible_windows = outt.split("\n")
visible_windows = [int(w, 16) for w in visible_windows if (len(w) > 0)]

if next_window:
  next_window = WmctrlWindow(next_window)

  if int(next_window.id, 16) in visible_windows:
    for line in lines:
      if line.find(str(next_window.id)) >= 0:
        next_window.set_focus()
        title = next_window.name.encode('ascii', 'ignore')
        script = '/home/danilo/scripts/dmenu/dzen_monitor.sh'
        os.popen("{script} {monitor} '{title}'".format(script=script, monitor=next_window.monitor, title=title)).read()
        sys.exit()

limit = 6
while(limit > 0 and len(next_windows) == 0):
  if type_cycle == 'next':
    next_monitor = next_monitor + 1
    if(next_monitor == 5):
      next_monitor = 1
  else:
    next_monitor = next_monitor - 1
  if(next_monitor == 0):
    next_monitor = 5

  next_windows = filter(lambda window: window.monitor == next_monitor and
                               window.workspace == current_window.workspace and
                               int(window.id, 16) in visible_windows and
                               window.valid, windows)
  limit = limit - 1
  
# filtra as telas por monitor
next_windows = filter(lambda window: window.monitor == next_monitor and
                                     window.workspace == current_window.workspace and
                                     int(window.id, 16) in visible_windows and
                                     window.valid, windows)

# focar na window e salvar no json
next_window = next_windows[0]
next_window.set_focus()

# key_json = 'm{m}{w}'.format(m=next_monitor, w=current_window.workspace)
# jjson[key_json] = next_window.str_win

# flip360 = open("/home/danilo/scripts/flip360_wids.json", "w")
# flip360.write(json.dumps(jjson))
# flip360.close()

title  = next_window.name.encode('ascii', 'ignore')
script = '/home/danilo/scripts/dmenu/dzen_monitor.sh'
os.popen("{script} {monitor} '{title}'".format(script=script, monitor=next_window.monitor, title=title)).read()

sys.exit()


# wmctrlWindow = WmctrlWindow("0x05600010  1 8504 1388 1641 987  xavier zim - Zim")
