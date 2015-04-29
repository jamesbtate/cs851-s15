#!/usr/bin/env python3
from library import *
import threading
import requests
import operator
import json
import time
import sys
import os
import re

if __name__=='__main__':
    if len(sys.argv) != 2:
        stderr("Usage:", sys.argv[0], "<mementos list>")
        sys.exit(1)
    mementos = []
    try:
        with open(sys.argv[1], 'r') as mementosFile:
            for line in mementosFile:
                mementos.append(line.strip())
    except Exception as e:
        stderr("error reading mementos file:", e)
        sys.exit(2)

    count = 0
    total = len(mementos)
    for memento in mementos:
        timemapPath = memento.split(':')[0]
        tweetID = timemapPath.split('/')[1]
        timemapProvider = timemapPath.split('/')[3][:-8]
        tweetDir = 'tweets2/' + tweetID + '/'
        mementosDir = tweetDir + 'mementos/'
        mementoURI = memento[memento.index('<')+1:memento.rindex('>')]
        #fix for broken archive.it timemaps:
        if mementoURI[:2] == '//':
            mementoURI = 'http:' + mementoURI
        dateString = re.search('datetime="(.*?)"', memento).group(1)
        isoString = time.strftime('%Y-%m-%dT%H:%M:%S', time.strptime(dateString, '%a, %d %b %Y %H:%M:%S GMT'))
        mementoPath = mementosDir + isoString + '.' + timemapProvider

        if not os.path.exists(mementosDir) and os.path.exists(tweetDir):
            os.makedirs(mementosDir)
        
        try:
            count += 1
            progress = str(count) + '/' + str(total)
            response = requests.get(mementoURI)
            with open(mementoPath, 'w') as mementoFile:
                mementoFile.write(response.text + '\n')
            stderr(progress, "downloaded memento for URI", tweetID, "with time", isoString)
        except Exception as e:
            stderr("exception when downloading and saving memento:", e)
