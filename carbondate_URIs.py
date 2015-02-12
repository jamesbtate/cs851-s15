#!/usr/bin/env python
from library import *
from summary import readSummary
from CarbonDate.local import cd
from time import strptime,mktime
from multiprocessing.dummy import Pool,Lock
import json
import time
import sys
import os

def printOldOutput(*strings):
    if len(strings) > 1:
        for s in strings:
            oldout.write(str(s) + ' ')
        oldout.write('b\n')
    elif len(strings) == 1:
        oldout.write(str(strings[0]) + '\n')

def carbondate(tweet):
    #tweet is a dict
    for url in tweet['urls']:
        try:
            ret = json.loads(cd(url['finalURI'].replace("'", '%27')))
            earliest = ret['Estimated Creation Date']
            topsy = ret['Topsy.com']
            lock.acquire()
            if not earliest:
                stderr("Earliest time is empty.")
                continue
            seconds = tweet['creation'] - mktime(strptime(earliest, "%Y-%m-%dT%H:%M:%S"))
            if seconds < 0.0: seconds = 0.0
            #stderr(seconds) 
            url['timeDelta'] = seconds
        except Exception as e:
            stderr("Error getting time difference:", e)
        finally:
            if 'timeDelta' not in url or url['timeDelta'] != seconds:
                url['timeDelta'] = 0.0
            global count
            count += 1
            stderr("Got (or errored) CarbonDate for", count, "URLs")
            lock.release()

if __name__=='__main__':
    null = open(os.devnull, 'w')
    oldout = sys.stdout
    count = 0
    sys.stdout = null
    lock = Lock()
    max = 128
    started = 0
    succeeded = 0
    headerErrors = []
    contentErrors = []
    startTime = time.time()
    pool = Pool(max)
    summary = readSummary(sys.argv[1])
    tweets = summary['tweets']
    pool.map(carbondate, tweets, 1)
    printOldOutput(json.dumps(summary))
