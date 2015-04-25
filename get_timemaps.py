#!/usr/bin/env python3
from library import *
import threading
import requests
import operator
import json
import time
import sys
import os

def threadDo(tweetID):
    finalURI = False
    for tweet in summary['tweets']:
        if tweet['id'] == tweetID:
            for url in tweet['urls']:
                if url['index'] == 0:
                    finalURI = url['finalURI'].strip()
                    break
            break
    if not finalURI:
        stderr("Could not find finalURI for tweetID", tweetID)
        return
    #curl http://timetravel.mementoweb.org/timemap/json/http://google.com
    indexURI = 'http://timetravel.mementoweb.org/timemap/json/' + finalURI
    #stderr(indexURI)
    response = requests.get(indexURI)
    try:
        responseJSON = json.loads(response.text)
    except:
        stderr("Failed to load JSON response from Timemap Index:")
        stderr(response.text)
        return

if __name__=='__main__':

    # get IDs we want to process
    tweetIDs = []
    with open('boilerpipe_common_ids', 'r') as tweetIDsFile:
        for line in tweetIDsFile:
            tweetIDs.append(line.strip())

    with open('tweets.summary.json', 'r') as summaryFile:
        summary = json.load(summaryFile)
    
    # get TimeMapsIndexes
    threads = []
    index = 0
    while True:
        if index >= len(tweetIDs):
            break
        if threading.active_count() > 16:
            time.sleep(0.1)
            continue
        t = threading.Thread(target=threadDo, args=(tweetIDs[index],))
        index += 1
        t.start()
        stderr("Started thread", t.name, "for tweet id", tweetIDs[index-1])
        threads.append(t)
    for t in threads:
        t.join()








