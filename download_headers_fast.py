#!/usr/bin/python3
from multiprocessing import Pool
import os

def startProcess(tweetID):
    print(tweetID)
    cmd = "./download_headers.bash " + tweetID.strip()
    os.system(cmd)

if __name__=='__main__':
    tweetIDs = os.listdir('tweets')
    with Pool(16) as pool:
        pool.map(startProcess, tweetIDs, 5)
