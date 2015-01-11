import urlparse
import oauth2 as oauth
import ParseTwitterConfig
import sys

config = ParseTwitterConfig.Parser(str(sys.argv[1]))
config.parseConfig()

consumer_key = config.getConsumerKey()
consumer_secret = config.getConsumerSecret()
access_token = config.getAccessToken()
access_secret = config.getAccessTokenSecret()

api = twitter.Api(consumer_key=consumer_key,
                  consumer_secret=consumer_secret,
                  access_token_key=access_token,
                  access_token_secret=access_secret)
