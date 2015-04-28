#!/usr/bin/env python3
from library import *
from get_timemaps import *
import threading
import requests
import operator
import json
import time
import sys
import os
import re

if __name__=='__main__':
    with open('tweets.summary.json', 'r') as summaryFile:
        summary = json.load(summaryFile)
    badURLs = []
    with open('bad_urls_only', 'r') as badURLsFile:
        for line in badURLsFile:
            badURLs.append(line.strip())
    for tweet in summary['tweets']:
        id = tweet['id']
        for url in tweet['urls']:
            final = url['finalURI'].strip()
            if final[0] == '/' or '://' not in final:
                if final in badURLs:
                    print(id, final)
                    with open('tweets/'+id+'/headers.0', 'r') as headersFile:
                        host = ''
                        for line in headersFile:
                            line = line.strip()
                            if re.search('^[lL]ocation:', line):
                                #print(line)
                                if '://' in line:
                                    match = re.search('https?://..*?/', line)
                                    if not match: match = re.search('https?://..*?$', line)
                                    host = match.group()
                                    if host[-1] != '/': host = host + '/'
                        #here               
                        if final[0] == '/':
                            newFinal = host + final[1:]
                        else:
                            newFinal = host + final
                        print(id, newFinal)
                        getTimemaps(id, newFinal)
    






