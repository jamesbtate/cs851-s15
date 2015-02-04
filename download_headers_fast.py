#!/usr/bin/env python3
from multiprocessing import Pool, Manager
import subprocess
import signal
import time
import sys
import os

if __name__=='__main__':
    max = 64
    tweetIDs = os.listdir('tweets')
    started = 0
    succeeded = 0
    headerErrors = []
    contentErrors = []
    try:
        headerProcesses = []
        contentProcesses = []
        gotHeaders = []
        while True:
            for process,id in headerProcesses:
                ret = process.poll()
                if ret is None:
                    continue
                elif ret != 0:
                    headerErrors.append((id, ret))
                else:
                    cmd2 = "./download_content.bash " + id.strip()
                    contentProcesses.append((subprocess.Popen(cmd2, shell=True), id))
                headerProcesses.remove((process,id))
            for process,id in contentProcesses:
                ret = process.poll()
                if ret is None:
                    continue
                elif ret != 0:
                    contentErrors.append((id, ret))
                else:
                    succeeded += 1
                contentProcesses.remove((process,id))
            if len(headerProcesses) + len(contentProcesses) < max and len(tweetIDs) > 1:
                id = tweetIDs.pop()
                cmd = "./download_headers.bash " + id.strip()
                headerProcesses.append((subprocess.Popen(cmd, shell=True), id))
                started += 1
            sys.stdout.write('\r' + 'started: %d  succeeded: %d  header errors: %d  content errors: %d'
                %(started, succeeded, len(headerErrors), len(contentErrors)))
            time.sleep(0.02)
    except KeyboardInterrupt:
        print('\nKeyboardInterrupt')