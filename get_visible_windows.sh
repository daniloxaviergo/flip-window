#!/bin/sh

xwinfo_ids=$(xdotool search --onlyvisible --name '.*')
printf '0x%x\n' $xwinfo_ids