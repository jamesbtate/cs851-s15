#!/usr/bin/python3
import argparse
import json
import sys

def parseArgs():
    desc = "Download headers and website content of URLs in tweets."
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('tweets_file', metavar='tweets-file', help='File containing tweet JSON strings, one per line.')
    args = parser.parse_args()
    return args

def printTweet(tweet, maxLength=999999, spacing=0):
    for key in tweet:
        print(' '*spacing + key, str(tweet[key])[0:maxLength])

def printTweetTextAndURLs(tweet, maxLength=999999, spacing=0):
    for key in tweet:
        if key == 'text':
            print(' '*spacing + str(tweet[key]))
    for key in tweet:
        if key == 'entities':
            if 'urls' in tweet[key]:
                for url in tweet['entities']['urls']:
                    print(' '*spacing + ' ' + str(url['url']))

if __name__ == '__main__':
    args = parseArgs()
    with open(args.tweets_file, 'r') as tweetsFile:
        for line in tweetsFile:
            tweet = json.loads(line.strip())
            printTweetTextAndURLs(tweet, maxLength=100)
            if 'retweeted_status' in tweet:
                printTweetTextAndURLs(tweet['retweeted_status'], maxLength=100, spacing=1)
            print ("#"*100)
