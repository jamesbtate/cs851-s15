#!/usr/bin/env python3
from library import *
import subprocess
import operator
import json
import time
import sys
import os

if __name__=='__main__':
    tweetIDsFile = open('boilerpipe_success_dirs', 'r')
    tweetIDs = []
    for line in tweetIDsFile.readlines():
        tweetIDs.append(line.strip().replace('./tweets/', '').replace('/',''))
    download2Stats = open('download2.stats', 'r')
    stats = json.load(download2Stats)
    for tweetID in [operator.getitem(a, 0) for a in stats['contentErrors']]:
        if tweetID in tweetIDs:
            tweetIDs.remove(tweetID)
            stderr("removed", tweetID)
        else:
            stderr(tweetID, "not in list")
    for tweetID in [operator.getitem(a, 0) for a in stats['headerErrors']]:
        if tweetID in tweetIDs:
            tweetIDs.remove(tweetID)
            stderr("removed", tweetID)
        else:
            stderr(tweetID, "not in list")
    for t in tweetIDs:
        print(t)
