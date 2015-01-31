#!/usr/bin/python3
from library import *
import argparse
import json
import sys
import os

SAVE_DIR = 'tweets'

def parseArgs():
    desc = "Download headers and website content of URLs in tweets."
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('tweets_file', metavar='tweets-file', help='File containing tweet JSON strings, one per line.')
    args = parser.parse_args()
    return args

def printTweetKeysValues(tweet, maxLength=-1):
    for key in tweet:
        print(key, str(tweet[key]).strip().replace('\n','')[0:maxLength])

def getTweetID(tweet):
    """returns string of tweet id.
    'tweet' is type dict"""
    return str(tweet['id'])

def getTweetText(tweet):
    """returns string of tweet text.
     'tweet' is type dict"""
    for key in tweet:
        if key == 'text':
            text = str(tweet[key])
            text = text.strip()
            text = text.replace('\n',' ')
            text = text.replace('\r','')
            return text
    return None

def getTweetURLs(tweet):
    """returns list of string URLs.
     'tweet' is type dict"""
    urls = []
    for key in tweet:
        if key == 'entities':
            if 'urls' in tweet[key]:
                for url in tweet['entities']['urls']:
                    urls.append(str(url['url']))
                return urls
    return None

def printTweet(tweet, maxLength=999999, spacing=0):
    text = getTweetText(tweet)[0:maxLength]
    print(' '*spacing, text)

def printTweetTextAndURLs(tweet, maxLength=999999, spacing=0):
    printTweet(tweet, maxLength=maxLength, spacing=spacing)
    urls = getTweetURLs(tweet)
    if urls:
        for url in urls:
            print(' '*spacing + ' ' + url)

def saveTweetToFiles(tweet, directory):
    id = getTweetID(tweet)
    text = getTweetText(tweet)
    urls = getTweetURLs(tweet)
    if not urls:
        stderr("tweet", id, "does not have any URLs")
        return
    dir = os.path.join(directory, id)
    try:
        if not os.path.exists(dir):
            os.mkdir(dir)
    except:
        stderr("Failed to create directory", dir)
        return
    try:
        textPath = os.path.join(dir, 'text')
        with open(textPath, 'w') as textFile:
            textFile.write(text)
            textFile.write('\n')
    except:
        stderr("Failed to write tweet text file in directory", dir)
        return
    try:
        index = 0
        for url in urls:
            urlPath = os.path.join(dir, "url." + str(index))
            with open(urlPath, 'w') as urlFile:
                urlFile.write(url)
                urlFile.write('\n')
            index += 1
    except:
        stderr("Failed to write tweet url file", index, "in directory", dir)

def processTweetsFile(tweetsFile):
    for line in tweetsFile:
        tweet = json.loads(line.strip())
        printTweetTextAndURLs(tweet, maxLength=150)
        #printTweetKeysValues(tweet, maxLength=50)
        saveTweetToFiles(tweet, SAVE_DIR)
        print ("#"*5)

if __name__ == '__main__':
    args = parseArgs()
    try:
        with open(args.tweets_file, 'r') as tweetsFile:
            processTweetsFile(tweetsFile)
    except BrokenPipeError:
        pass
