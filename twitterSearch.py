import urlparse
import oauth2 as oauth
import ParseTwitterConfig
import sys
import tweepy
from time import gmtime, strftime


class tweepyCrawl:

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


    def __init__(self, filepath ):

        '''Initialize Parser and parse the config'''

        config = ParseTwitterConfig.Parser(filepath)
        config.parseConfig()

        '''Populate OAuth fields '''

        self.consumer_key = config.getConsumerKey()
        self.consumer_secret = config.getConsumerSecret()
        self.access_token = config.getAccessToken()
        self.access_secret = config.getAccessTokenSecret()
        self.owner = config.getOwner()
        self.max_tweets = int(config.getMaxTweets())

        ''' Twitter post '''
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_secret)
        self.api =  tweepy.API(auth)


    def search(self , keywords , geo_tag):

        searched_tweets = []

        for k in keywords:

            k = k.strip()
            print "searching Twitter for : " + k
            last_id = -1
            search_results = self.api.search(q=k, count=self.max_tweets , show_user = True)
            for t in search_results:
                print t

        print searched_tweets

    def getUsers(self , userIdList):
            userMeta = self.api.lookup_users(user_ids=userIdList)
            for user in userMeta:
                print user















