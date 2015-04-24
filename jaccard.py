#!/usr/bin/env python3
from library import *
import subprocess
import operator
import json
import time
import sys
import os

if __name__=='__main__':
    tweetIDsFile = open('boilerpipe_common_ids', 'r')
    tweetIDs = []
    for line in tweetIDsFile.readlines():
        tweetIDs.append(line.strip())
    tweetIDsFile.close()
    print("Tweet_ID", "Unigram_Distance", "Bigram_Distance", "Trigram_Distance")
    for id in tweetIDs:
        text1 = ''
        text2 = ''
        with open('tweets/' + id + '/content.0/boilerpipe.output', 'r') as textFile1:
            for line in textFile1:
                text1 = text1 + extractWords(line).strip() + ' '
        with open('tweets2/' + id + '/content.0/boilerpipe.output', 'r') as textFile2:
            for line in textFile2:
                text2 = text2 + extractWords(line).strip() + ' '
        unigrams1 = text1.split(' ')
        unigrams2 = text2.split(' ')
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
        union1 = set(unigrams1).union(unigrams2)
        intersection1 = set(unigrams1).intersection(unigrams2)
        union2 = set(bigrams1).union(bigrams2)
        intersection2 = set(bigrams1).intersection(bigrams2)
        union3 = set(trigrams1).union(trigrams2)
        intersection3 = set(trigrams1).intersection(trigrams2)
        dist1 = (len(union1) - len(intersection1)) * 1.0 / len(union1)
        dist2 = (len(union2) - len(intersection2)) * 1.0 / len(union2)
        dist3 = (len(union3) - len(intersection3)) * 1.0 / len(union3)
        print(id, dist1, dist2, dist3)
