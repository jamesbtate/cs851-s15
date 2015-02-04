#!/bin/bash
#pkill -9 python3 >/dev/null 2>&1
ps -ef | grep "./download_[a-z]\+.bash" | awk '{print $2}' | xargs kill -9
