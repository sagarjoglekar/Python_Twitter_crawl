import urlparse
import oauth2 as oauth
import ParseTwitterConfig
import sys
import twitter


from time import gmtime, strftime



config = ParseTwitterConfig.Parser(str(sys.argv[1]))
config.parseConfig()

consumer_key = config.getConsumerKey()
consumer_secret = config.getConsumerSecret()
access_token = config.getAccessToken()
access_secret = config.getAccessTokenSecret()
owner = config.getOwner()

api = twitter.Api(consumer_key=consumer_key,
                  consumer_secret=consumer_secret,
                  access_token_key=access_token,
                  access_token_secret=access_secret)

print api.VerifyCredentials()

statuses = api.GetUserTimeline(screen_name=owner)
print [s.text for s in statuses]

users = api.GetFriends()
print [u.name for u in users]

status = api.PostUpdate(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
print status.text
