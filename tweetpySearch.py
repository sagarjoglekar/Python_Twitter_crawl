import tweepy
import sys
# assuming twitter_authentication.py contains each of the 4 oauth elements (1 per line)
import ParseTwitterConfig

config = ParseTwitterConfig.Parser(str(sys.argv[1]))
config.parseConfig()

consumer_key = config.getConsumerKey()
consumer_secret = config.getConsumerSecret()
access_token = config.getAccessToken()
access_secret = config.getAccessTokenSecret()
owner = config.getOwner()

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

query = 'python'
max_tweets = 1000
searched_tweets = [status for status in tweepy.Cursor(api.search, q=query).items(max_tweets)]
print searched_tweets

searched_tweets = []
last_id = -1
while len(searched_tweets) < max_tweets:
    count = max_tweets - len(searched_tweets)
    try:
        new_tweets = api.search(q=query, count=count, max_id=str(last_id - 1))
        if not new_tweets:
            break
        searched_tweets.extend(new_tweets)
        last_id = new_tweets[-1].id
    except tweepy.TweepError as e:
        # depending on TweepError.code, one may want to retry or wait
        # to keep things simple, we will give up on an error
        break
