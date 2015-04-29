#!/usr/bin/env python3
import json
summaryFile = open('tweets.summary.json', 'r')
summary = json.load(summaryFile)
#old = [tweet for tweet in summary['tweets'] if tweet['urls'][0]['timeDelta'] > 0.0]
#len(old) 5767
#old = [tweet for tweet in summary['tweets'] if tweet['urls'][0]['timeDelta'] > 86400.0]
#len(old) 3160
#old = [tweet for tweet in summary['tweets'] if tweet['urls'][0]['timeDelta'] > 365*86400.0]
#len(old) 600
old = [tweet for tweet in summary['tweets'] if tweet['urls'][0]['timeDelta'] > 730*86400.0]
#len(old) 373
old_ids = [tweet['id'] for tweet in old]
a = open('two-year-old_tweets', 'w')
for id in old_ids:
    a.write(id + '\n')
a.close()
