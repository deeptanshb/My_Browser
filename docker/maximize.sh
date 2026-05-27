#!/bin/bash
export DISPLAY=:99
echo "Waiting for browser window..."
sleep 15
for i in $(seq 1 30); do
    WINS=$(xdotool search --onlyvisible --any --name "" 2>/dev/null)
    if [ -n "$WINS" ]; then
        for WID in $WINS; do
            xdotool windowsize $WID 1280 800 2>/dev/null
            xdotool windowmove $WID 0 0 2>/dev/null
            wmctrl -ir $WID -b add,maximized_vert,maximized_horz 2>/dev/null
        done
        echo "Maximized"
        sleep 30
    else
        echo "Attempt $i - waiting..."
        sleep 3
    fi
done
