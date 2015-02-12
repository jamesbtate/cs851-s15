#!/usr/bin/python3
from time import mktime,strptime
from library import *
import statistics
import argparse
import shutil
import json
import math
import sys
import os
import re

tweetsDir = 'not_set'

def parseArgs():
    desc = "Generate or display summary JSON from tweets directory."
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument('-l', '--load-tweets', metavar='tweets-dir', help='Load  and summarize tweets from directory containing only tweet directories - one for each tweet. Directory name is the tweet ID.')
    parser.add_argument('-r', '--read-summary', metavar='summary-file', help='Read tweets summary from JSON file.')
    parser.add_argument('-p', '--print-json', action='store_true')
    parser.add_argument('-s', '--print-stats', action='store_true')
    parser.add_argument('-S', '--print-stats-10000', action='store_true')
    parser.add_argument('-d', '--download-stats', help="Load the download stats from the given file and use it to exclude tweets that had errors during download.")
    parser.add_argument('-x', '--remove-errors', action="store_true", help="Remove the tweet directory of all tweets that we consider failed.")
    parser.add_argument('-f', '--final-uris', action="store_true", help="Save final URI into file in tweet directory.")
    parser.add_argument('-t', '--tweets-file', help="Load other tweet information from this tweets file.")
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

def dictValuesToCount(input):
    # takes input dict with some repeated values, and generates output dict
    # with keys the being the values from input and values being the number
    # of occurences of each
    output = {}
    for key in input:
        addOrIncrementDict(output, input[key])
    return output

def printStats(tweets, delete=False, stopAt=999999999):
    print("Number of tweets with URIs:", len(tweets))
    codes = {}
    finalURIs = {}
    initialURIs = {}
    numURIs = {}
    timeDeltas = {}
    numRedirects = {}
    totalURIs = 0
    for tweet in tweets:
        if totalURIs >= stopAt: break
        addOrIncrementDict(numURIs, len(tweet['urls']))
        for url in tweet['urls']:
            if totalURIs >= stopAt: break
            redirects = 0
            for code in url['codes']:
                code = int(code)
                addOrIncrementDict(codes, code)
                if code >= 300 and code < 400:
                    redirects += 1
            addOrIncrementDict(numRedirects, redirects)
            if 'timeDelta' in url:
                addOrIncrementDict(timeDeltas, url['timeDelta'])
            try:
                addOrIncrementDict(finalURIs, url['finalURI'])
                totalURIs += 1
            except:
                stderr("Tweet", tweet['id'], "has no final URI.")
                if delete: removeTweetDirByID(tweet['id'])
            addOrIncrementDict(initialURIs, url['t.co'])
    print("Number of URIs:", totalURIs)
    print("HTTP Status Codes:")
    printDict(codes)
    print("Number of Redirects:")
    printDict(numRedirects)
    print("Number of unique t.co URIs:", len(initialURIs))
    print("Number of unique final URIs:", len(finalURIs))
    initialURIFrequencies = dictValuesToCount(initialURIs)
    print("Frequency of Initial URL Multiplicity:")
    printDict(initialURIFrequencies)
    finalURIFrequencies = dictValuesToCount(finalURIs)
    print("Frequency of Final URL Multiplicity:")
    printDict(finalURIFrequencies)
    print("Number of URLs per Tweet:")
    printDict(numURIs)
    allTimeDeltas = []
    for time in timeDeltas:
        for i in range(timeDeltas[time]):
            allTimeDeltas.append(time)
    print("Median URI Age:", round(statistics.mean(allTimeDeltas)))
    print("Mean URI Age:", round(statistics.median(allTimeDeltas)))
    print("Standard Deviation of URI Ages:", round(statistics.stdev(allTimeDeltas)))
    print("Standard Error of URI Ages:", round(statistics.stdev(allTimeDeltas)/math.sqrt(len(allTimeDeltas))))
    print("Time Deltas (Twitter - creation estimate) in Seconds:")
    printDict(timeDeltas)

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

def saveFinalURIs(summary):
    tweetsDir = summary['tweetsDir']
    count = 0
    for tweet in summary['tweets']:
        tweetPath = os.path.join(tweetsDir, tweet['id'])
        for url in tweet['urls']:
            try:
                finalURIPath = os.path.join(tweetPath, 'final_url.' + str(url['index']))
                finalURIFile = open(finalURIPath, 'w')
                finalURIFile.write(url['finalURI']+'\n')
                finalURIFile.close()
                count += 1
                sys.stderr.write("\rWrote %d final URIs to file" %count)
            except Exception as e:
                stderr("\nError writing final URI for tweet", tweet['id'], "to file:", str(e))
    stderr("")

def removeTweetDirByID(id):
    deletePath = os.path.join(tweetsDir, id)
    shutil.rmtree(deletePath)
    stderr("Removed tweet directory for tweet", id)

def excludeDownloadErrors(tweets, downloadStatsPath, delete=False):
    downloadStatsFile = open(downloadStatsPath, 'r')
    downloadStats = json.loads(downloadStatsFile.read())
    downloadStatsFile.close()
    for tweet in tweets:
        if tweet['id'] in tuple(l[0] for l in downloadStats['headerErrors']):
            tweets.remove(tweet)
            stderr("Tweet", tweet['id'], "removed for curl error", [x[1] for x in downloadStats['headerErrors'] if x[0] == tweet['id']][0])
            if delete: removeTweetDirByID(tweet['id'])
        if tweet['id'] in tuple(l[0] for l in downloadStats['contentErrors']):
            tweets.remove(tweet)
            stderr("Tweet", tweet['id'], "removed for wget error", [x[1] for x in downloadStats['contentErrors'] if x[0] == tweet['id']][0])
            if delete: removeTweetDirByID(tweet['id'])

def readSummary(summaryPath):
    summaryFile = open(summaryPath, 'r')
    summary = json.loads(summaryFile.read())
    summaryFile.close()
    return summary

def loadMetadata(summary, tweetsFilePath):
    tweetsFile = open(tweetsFilePath, 'r')
    count = 0
    for line in tweetsFile:
        tweet = json.loads(line)
        lineID = int(tweet['id'])
        try:
            summaryTweet = next(t for t in summary['tweets'] if int(t['id']) == lineID)
        except StopIteration:
            continue
        if summaryTweet:
            summaryTweet['creation'] = mktime(strptime(tweet['created_at'], "%a %b %d %H:%M:%S +0000 %Y"))
            count += 1
            sys.stderr.write("\rLoaded metadata for " + str(count) + " tweets.")
    tweetsFile.close()
    stderr("")

if __name__ == '__main__':
    args = parseArgs()
    summary = {}
    if args.load_tweets:
        summary['tweetsDir'] = args.load_tweets
        tweets = summarizeTweets(args.load_tweets)
        summary['tweets'] = tweets
    else:
        summary = readSummary(args.read_summary)
    tweetsDir = summary['tweetsDir']
    if args.download_stats:
        excludeDownloadErrors(summary['tweets'], args.download_stats, args.remove_errors)
    if args.final_uris:
        saveFinalURIs(summary)
    if args.tweets_file:
        loadMetadata(summary, args.tweets_file)
    if args.print_json:
        print(json.dumps(summary))
    if args.print_stats:
        print("=== Stats for all tweets ===")
        printStats(summary['tweets'], delete=args.remove_errors)
    if args.print_stats_10000:
        print("=== Stats for first 10000 tweets ===")
        printStats(summary['tweets'], delete=args.remove_errors, stopAt=10000)

