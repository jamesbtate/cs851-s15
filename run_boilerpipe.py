#!/usr/bin/python3
from library import *
import subprocess
import sys
import re

dir_index = open('tweets_file_list', 'r', encoding='latin-1')
files = []
for line in dir_index:
    line = line.strip()
    if re.search('/content.[0-9]/wget.output$', line): continue
    if re.search('/content.[0-9]$', line): continue
    if not re.search('/content.[0-9]/', line): continue
    files.append(line)

queue = []
stderr("Generating work queue...")
uri_file = open('uniq_final_uris', 'r')
for line in uri_file:
    sys.stderr.write('\r' + str(len(queue)))
    line = line.strip()
    space1 = line.find(' ', 1)
    space2 = line.find(' ', space1+1)
    multiplicity = int(line[:space1])
    tweetURIIDParts = line[space1+1:space2].split('.')
    tweetID = tweetURIIDParts[0]
    uriID = tweetURIIDParts[1]
    uri = line[space2+1:]
    #print(tweetID, uriID, uri)
    matchString = tweetID + '/content.' + uriID
    found = False
    for f in files:
        if matchString in f:
            queue.append(f)
            files.remove(f)
            found = True
            break
    if not found:
        doNothing = True
        #stderr('\n' + "Did not find content directory for", tweetID, uriID)
stderr()

stderr("Running boilerpipe")
count = 1
for item in queue:
    sys.stderr.write('\r' + str(count))
    count += 1
    dir = item[:38]
    outName = dir + 'boilerpipe.output'
    cmd = 'python -m justext -s English -o ' + outName + " '" + item + "'"
    #print(cmd)
    subprocess.call(cmd, shell=True)
