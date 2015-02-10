#!/usr/bin/python3
from library import *
import argparse
import json
import sys
import os
import re

SAVE_DIR = 'tweets'

def parseArgs():
    desc = "Generate or display summary JSON from tweets directory."
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument('-l', '--load-tweets', metavar='tweets-dir', help='Load  and summarize tweets from directory containing only tweet directories - one for each tweet. Directory name is the tweet ID.')
    parser.add_argument('-r', '--read-summary', metavar='summary-file', help='Read tweets summary from JSON file.')
    parser.add_argument('-p', '--print-json', action='store_true')
    parser.add_argument('-s', '--print-stats', action='store_true')
    parser.add_argument('-S', '--print-stats-10000', action='store_true')
    parser.add_argument('-d', '--download-stats', help="Load the download stats from the given file and use it to exclude tweets that had errors during download.")
    args = parser.parse_args()
    if not args.load_tweets and not args.read_summary:
        parser.error("You must specify either -l or -r")
    if args.load_tweets and args.read_summary:
        parser.error("You cannot specify both -l and -r")
    return args

def addOrIncrementDict(d, item):
    try:
        d[item] += 1
    except KeyError:
        d[item] = 1

def printDict(d):
    sortedKeys = sorted(d)
    for key in sortedKeys:
        print(key, d[key])

def printStats(tweets):
    print("Number of tweets with URIs:", len(tweets))
    codes = {}
    finalURIs = {}
    initialURIs = {}
    numURIs = {}
    for tweet in tweets:
        addOrIncrementDict(numURIs, len(tweet['urls']))
        for url in tweet['urls']:
            for code in url['codes']:
                addOrIncrementDict(codes, code)
            try:
                addOrIncrementDict(finalURIs, url['finalURI'])
            except:
                stderr("Tweet", tweet['id'], "has no final URI.")
            addOrIncrementDict(initialURIs, url['t.co'])
    print("HTTP Status Codes:")
    printDict(codes)
    print("Number of unique t.co URIs:", len(initialURIs))
    print("Number of unique final URIs:", len(finalURIs))

def summarizeTweets(tweetsDir):
    tweetDirs = os.listdir(tweetsDir)
    stderr("Found", len(tweetDirs), "tweet directories.")
    tweets = []
    for tweetDir in tweetDirs:
        tweet = {}
        tweet['id'] = tweetDir
        tweetPath = os.path.join(tweetsDir, tweetDir)
        textFile = open(os.path.join(tweetPath, 'text'), 'r')
        tweet['text'] = textFile.read()
        textFile.close()
        tweetFiles = os.listdir(tweetPath)
        tweet['urls'] = []
        for item in tweetFiles:
            if item[:3] == 'url':
                url = {}
                url['index'] = int(item.split('.')[1])
                urlFile = open(os.path.join(tweetPath, item), 'r')
                url['t.co'] = urlFile.read()
                urlFile.close()
                # get info from headers file:
                url['codes'] = []
                try:
                    headersFile = open(os.path.join(tweetPath, 'headers.'+str(url['index'])), 'r')
                except:
                    stderr("\nProblem opening headers file", os.path.join(tweetPath, 'headers.'+str(url['index'])))
                    continue
                for line in headersFile.readlines():
                    line = line.strip()
                    location = ''
                    redirected = False
                    m = re.search('^HTTP/1.[01] ([0-9][0-9][0-9])', line)
                    if m:
                        url['codes'].append(m.group(1))
                    m = re.search('^[Ll]ocation: (.*)$', line)
                    if m:
                        url['finalURI'] = m.group(1)
                tweet['urls'].append(url)
        if len(tweet['urls']) > 0:
            tweets.append(tweet)
        else:
            stderr("Tweet", tweet['id'], "had no URIs.")
        sys.stderr.write("\rSummarized " + str(len(tweets)) + " tweets.")
    stderr("")
    return tweets

def excludeDownloadErrors(tweets, downloadStatsPath):
    downloadStatsFile = open(downloadStatsPath, 'r')
    downloadStats = json.loads(downloadStatsFile.read())
    downloadStatsFile.close()
    for tweet in tweets:
        if tweet['id'] in tuple(l[0] for l in downloadStats['headerErrors']):
            tweets.remove(tweet)
            stderr("Tweet", tweet['id'], "removed for curl error", [x[1] for x in downloadStats['headerErrors'] if x[0] == tweet['id']][0])
        if tweet['id'] in tuple(l[0] for l in downloadStats['contentErrors']):
            tweets.remove(tweet)
            stderr("Tweet", tweet['id'], "removed for wget error", [x[1] for x in downloadStats['contentErrors'] if x[0] == tweet['id']][0])

def readSummary(summaryPath):
    summaryFile = open(summaryPath, 'r')
    tweets = json.loads(summaryFile.read())
    summaryFile.close()
    return tweets

if __name__ == '__main__':
    args = parseArgs()
    if args.load_tweets:
        tweets = summarizeTweets(args.load_tweets)
    else:
        tweets = readSummary(args.read_summary)
    if args.download_stats:
        excludeDownloadErrors(tweets, args.download_stats)
    if args.print_json:
        print(json.dumps(tweets))
    if args.print_stats:
        print("=== Stats for all tweets ===")
        printStats(tweets)
    if args.print_stats_10000:
        print("=== Stats for first 10000 tweets ===")
        printStats(tweets[:10000])

