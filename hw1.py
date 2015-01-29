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
track = ['python', 'fsf', 'foss', 'coding', 'programming', 'fedora',
         'rhel', 'dovetail', 'woodworking', 'blizzard', 'snowstorm',
         'colorado', 'virginia', 'internet', 'library', 'libraries',
         'json', 'vodka lemonade', 'woodchuck', 'iasip', 'league',
         'awesomenaut', 'tf2']


class MyListener(tweepy.StreamListener):
    def __init__(self, logFile):
        tweepy.StreamListener.__init__(self)
        self.logFile = logFile
        self.count = 0
    def on_status(self, status):
        self.count += 1
        print(self.count, status.text)
        logFile.write(json.dumps(status._json))
        logFile.write('\n')


if __name__ == '__main__':
    logFile = open('output.log', 'a')
    listener = MyListener(logFile)
    auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
    auth.set_access_token(accessToken, accessTokenSecret)
    api = tweepy.API(auth)
    stream = tweepy.Stream(auth=api.auth, listener=listener)
    stream.filter(track=track, async=True, languages=['en'])
