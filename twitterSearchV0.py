import urlparse
import oauth2 as oauth
import ParseTwitterConfig
import sys
import twitter
import operator
import collections
import nltk

from collections import Counter
from time import gmtime, strftime
from TwitterSearch import *
from nltk.tokenize import RegexpTokenizer


class EmoCrawl:

    ''' Get a list of keywords '''
    keywords = []
    geo = ''

    consumer_key = ''
    consumer_secret = ''
    access_token = ''
    access_secret = ''
    owner = ''
    tweettext = []
    adjectives = []
    nouns = []


    def __init__(self, filepath, keyword_list, geo_tag):

        '''Initialize Parser and parse the config'''

        config = ParseTwitterConfig.Parser(filepath)
        config.parseConfig()

        ''' store search keywords and geo'''
        self.keywords = keyword_list
        self.geo = geo_tag


        '''Populate OAuth fields '''

        self.consumer_key = config.getConsumerKey()
        self.consumer_secret = config.getConsumerSecret()
        self.access_token = config.getAccessToken()
        self.access_secret = config.getAccessTokenSecret()
        self.owner = config.getOwner()



    def makePost(self):

        ''' Twitter post '''
        api = twitter.Api(consumer_key= self.consumer_key,
                          consumer_secret= self.consumer_secret,
                          access_token_key= self.access_token,
                          access_token_secret= self.access_secret)

        print api.VerifyCredentials()

        status = "Crawling Twitter for fun at : "
        time = strftime("%Y-%m-%d %H:%M:%S", gmtime())

        posted = api.PostUpdate(status + time)
        print posted.text


    def search(self):
        try:
            tso = TwitterSearchOrder() # create a TwitterSearchOrder object
            tso.set_keywords(self.keywords) # let's define all words we would like to have a look for
            tso.set_language('en') # we want to see English tweets only
            tso.set_include_entities(False) # and don't give us all those entity information

            # it's about time to create a TwitterSearch object with our secret tokens
            ts = TwitterSearch(
                consumer_key = self.consumer_key,
                consumer_secret = self.consumer_secret,
                access_token = self.access_token,
                access_token_secret = self.access_secret
             )

             # this is where the fun actually starts :)
            for tweet in ts.search_tweets_iterable(tso):
                #print( '@%s tweeted: %s' % ( tweet['user']['screen_name'], tweet['text'] ) )
                self.tweettext.append(tweet['text']);

        except TwitterSearchException as e: # take care of all those ugly errors if there are some
            print(e)

        for twttxt in self.tweettext:
            tokenizer = RegexpTokenizer(r'\w+')
            #tokens = nltk.word_tokenize(twttxt)
            tokens = tokenizer.tokenize(twttxt)
            tags = nltk.pos_tag(tokens)
            for word, pos in tags:
                if pos in ['JJ']: # feel free to add any other noun tags
                    self.adjectives.append(word)
            for word, pos in tags:
                if pos in ['NN']: # feel free to add any other noun tags
                    self.nouns.append(word)
        adjHist = Counter(self.adjectives)
        print "Histogram of Adjectives : " + str(adjHist)
        nounHist = Counter(self.nouns)
        print "Histogram of Nouns : " + str(nounHist)