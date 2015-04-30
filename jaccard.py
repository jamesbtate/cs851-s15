#!/usr/bin/env python3
from library import *
import subprocess
import operator
import json
import time
import sys
import os

def jaccardDistance(list1, list2):
    union = set(list1).union(list2)
    intersect = set(list1).intersection(list2)
    dist = (len(union) - len(intersect)) * 1.0 / len(union)
    return dist

def wordsFromFile(filePath):
    text = ''
    with open(filePath, 'r') as textFile:
        for line in textFile:
            text = text + extractWords(line).strip() + ' '
    words = text.strip().split(' ')
    if '' in words:
        words.remove('')
    return words

if __name__=='__main__':
    tweetIDsFile = open('boilerpipe_common_ids', 'r')
    tweetIDs = []
    for line in tweetIDsFile.readlines():
        tweetIDs.append(line.strip())
    tweetIDsFile.close()
    print("Tweet_ID", "Unigram_Distance", "Bigram_Distance", "Trigram_Distance")
    for id in tweetIDs:
        unigrams1 = wordsFromFile('tweets/' + id + '/content.0/boilerpipe.output')
        unigrams2 = wordsFromFile('tweets2/' + id + '/content.0/boilerpipe.output')
        bigrams1 = []
        bigrams2 = []
        trigrams1 = []
        trigrams2 = []
        for i in range(0,len(unigrams1)):
            if i >= 1:
                bigrams1.append(unigrams1[i-1] + ' ' + unigrams1[i])
            if i >= 2:
                trigrams1.append(unigrams1[i-2] + ' ' + unigrams1[i-1] + ' ' + unigrams1[i])
        for i in range(0,len(unigrams2)):
            if i >= 1:
                bigrams2.append(unigrams2[i-1] + ' ' + unigrams2[i])
            if i >= 2:
                trigrams2.append(unigrams2[i-2] + ' ' + unigrams2[i-1] + ' ' + unigrams2[i])
        dist1 = jaccardDistance(unigrams1, unigrams2)
        dist2 = jaccardDistance(bigrams1, bigrams2)
        dist3 = jaccardDistance(trigrams1, trigrams2)
        print(id, "%0.3f %0.3f %0.3f" %(dist1, dist2, dist3))
