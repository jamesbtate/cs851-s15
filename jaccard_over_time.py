#!/usr/bin/env python3
from library import *
from jaccard import *
import json
import sys
import os

if not len(sys.argv) == 2:
    stderr("Usage:", sys.argv[0], "<list of tweet ids>")
    sys.exit(1)

tweetIDs = []
with open(sys.argv[1], 'r') as idsFile:
    for line in idsFile:
        tweetIDs.append(line.split()[0])

for id in tweetIDs:
    mementosDir = 'tweets2/' + id + '/mementos/'
    filesList = os.listdir(mementosDir)
    filesList.sort()
    firstMementoName = filesList[0]
    filesList.remove(firstMementoName)
    firstWords = wordsFromFile(mementosDir + firstMementoName)
    firstWords.sort()
    #print(firstWords[0:50])

    scores = []
    for item in filesList:
        if 'boilerpipe' not in item:
            continue
        date = item.split('T')[0]
        words = wordsFromFile(mementosDir + item)
        words.sort()
        #print('====',len(firstWords),len(words),item,'====')
        #print(words[0:50])
        distance = jaccardDistance(words, firstWords)
        scores.append((date,distance))
    with open('hw4_report/stats/q3/' + id + '.stats', 'w') as outputFile:
        for score in scores:
            outputFile.write(score[0] + ' ' + str(score[1]) + '\n')
    #for s in scores: print(s)
    stderr("Finished calculating tweet", id)
