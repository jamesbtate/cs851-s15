#!/usr/bin/env python3
from multiprocessing import Pool, Manager
import subprocess
import signal
import time
import sys
import os

def startProcess(tweetID, count, lock):
    lock.acquire()
    count += 1
    print(count, tweetID)
    lock.release()
    cmd = "./download_headers.bash " + tweetID.strip()
    subprocess.call(cmd, shell=True)
    cmd2 = "./download_content.bash " + tweetID.strip()
    subprocess.call(cmd2, shell=True)

def init_worker():
    signal.signal(signal.SIGINT, signal.SIG_IGN)

if __name__=='__main__':
    #signal.signal(signal.SIGINT, handler)
    manager = Manager()
    lock = manager.Lock()
    count = manager.Value(int, 0)
    tweetIDs = os.listdir('tweets')
    pool = Pool(64, init_worker)
    try:
        #pool.map_async(startProcess, tweetIDs, 1)
        for id in tweetIDs:
            pool.apply_async(func=startProcess, args=(id,count,lock))
        pool.close()
        pool.join()
    except KeyboardInterrupt:
        print('KeyboardInterrupt')
        pool.terminate()
        pool.join()
