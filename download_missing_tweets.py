#!/usr/bin/python3
import tweepy
import json

#@classmethod                    
#def parse(cls, api, raw):
#        status = cls.first_parse(api, raw)
#        setattr(status, 'json', json.dumps(raw))
#        return status
#tweepy.models.Status.first_parse = tweepy.models.Status.parse
#tweepy.models.Status.parse = parse

consumerKey = '0XwRBiz4CUHsknKQ413Jnrury'
consumerSecret = '3uYMltqnTlZUVMxP6TnXyHl3l9eugEamQANoQKKhokBxSKcE0a'
accessToken = '2999979436-6Bg2iZUYAT4nnVvQg7wmpG3aE0lPkPF7tItBll2'
accessTokenSecret = '1BhUQd7UtVqhV4SVnI8DKUkAaaORLracbBtJI9Z8Fx4i3'

if __name__ == '__main__':
    #logFile = open('output.log', 'a')
    #listener = MyListener(logFile)
    auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
    auth.set_access_token(accessToken, accessTokenSecret)
    api = tweepy.API(auth)
    #stream = tweepy.Stream(auth=api.auth, listener=listener)
    #stream.filter(track=track, async=True, languages=['en'])
    ids = ['560606694930386945',
        '560614975731802113',
        '560616224716226560',
        '560618439174148096',
        '560618800895512576',
        '561235693834620928']
    results = api.statuses_lookup(ids)
    for r in results:
        print(json.dumps(r._json))
    #print(tweet['created_at'])
