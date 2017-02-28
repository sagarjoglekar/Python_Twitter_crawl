import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib
from datetime import datetime , timedelta
import json
from twitterSearch import tweepyCrawl
#from selenium.common.exceptions import NoSuchElementException
import ParseTwitterConfig


class RestCrawler:

    since = "2013-01-01"
    till = "2014-12-31"#datetime.datetime.today().strftime('%Y-%m-%d')
    #since = (datetime.today() - timedelta(days=10)).strftime('%Y-%m-%d')
    #till = datetime.today().strftime('%Y-%m-%d')
    queryBase = "https://twitter.com/search?l=en&q="

    def __init__(self, configFile , since = None , till = None ):

        if since != None:
            self.since = since
        if till != None:
            self.till = till


    def encodeQuery(self, query  , Exact = True):
        queryString = ''
        if Exact:
            queryString = '"{}"'.format(query) + ' since:' + self.since + ' until:' + self.till
        else:
            queryString = query + ' since:' + self.since + ' until:' + self.till
        return queryString

    def deserializeTweets(self, tweetText):
        components = tweetText.split('\n')
        for i in range(len(conponents)):
            if components[i] == "More":
                metaText = componets[:i]
        return self

    def killBrowser(self):
        self.browser.quit()
        time.sleep(1)

    def doCrawl(self , queryString , pages):
        url = self.queryBase+queryString
        print url
        tweetData = dict()

        # browser = webdriver.Chrome(self.driver,
        # chrome_options=self.options,
        # service_args=self.service_args,
        # service_log_path=self.service_log_path)

        self.browser.get(url)
        time.sleep(1)

        body = self.browser.find_element_by_tag_name('body')

        for _ in range(pages):
            body.send_keys(Keys.PAGE_DOWN)
            print "Scrolling: %d" %_
            time.sleep(2)

        try:
            stream = body.find_element_by_class_name('stream')
            tweets = stream.find_elements_by_class_name('stream-item')
            print "Found %d Tweets " %len(tweets)
        except NoSuchElementException:
            print "Search showed up empty, moving on"
            return tweetData

        for tweet in tweets:
            reply_count = 0
            retweet_count = 0
            like_count = 0
            attrs = {}
            tweet_text = ""

            try :
                meta = tweet.find_element_by_class_name('tweet')
                print tweet.text

                attrs = self.browser.execute_script('var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;', meta)

                content = meta.find_element_by_class_name('content')

                tweet_text = content.find_element_by_class_name('tweet-text').text




                actions = content.find_element_by_class_name('ProfileTweet-actionList')

                reply = actions.find_element_by_class_name('ProfileTweet-action--reply')
                reply_count = reply.find_element_by_class_name('ProfileTweet-actionCountForPresentation').text

                retweet = actions.find_element_by_class_name('ProfileTweet-action--retweet')
                retweet_count = retweet.find_element_by_class_name('ProfileTweet-actionCountForPresentation').text

                like = actions.find_element_by_class_name('ProfileTweet-action--favorite' )
                like_count = like.find_element_by_class_name('ProfileTweet-actionCountForPresentation').text

            except NoSuchElementException:

                print "Failed to find Action Fields!! "
                break







            tweetData[attrs['data-tweet-id']] = dict()
            tweetData[attrs['data-tweet-id']]['meta'] = attrs
            tweetData[attrs['data-tweet-id']]['text'] = tweet_text
            tweetData[attrs['data-tweet-id']]['Reply_count'] = reply_count
            tweetData[attrs['data-tweet-id']]['Retweet_count'] = retweet_count
            tweetData[attrs['data-tweet-id']]['Like_count'] = like_count
            print tweetData[attrs['data-tweet-id']]
            print "\n"


        return tweetData

    def getUserInfo(self , DataDict):
        baseUrl = "https://www.twitter.com/"

        for tweet in DataDict:
            userScreenName = DataDict[tweet]['meta']['data-screen-name']
            url = baseUrl + userScreenName
            tweets_number = str(0)
            following_number = str(0)
            follower_number = str(0)
            fav_number = str(0)


            self.browser.get(url)
            time.sleep(1)
            body = self.browser.find_element_by_tag_name('body')
            zone = body.find_element_by_class_name('ProfileNav-list')
            try :

                tweets = zone.find_element_by_class_name('ProfileNav-item--tweets')
                tweets_number = tweets.find_element_by_class_name('ProfileNav-value').text

                following = zone.find_element_by_class_name('ProfileNav-item--following')
                following_number = following.find_element_by_class_name('ProfileNav-value').text

                follower = zone.find_element_by_class_name('ProfileNav-item--followers')
                follower_number = follower.find_element_by_class_name('ProfileNav-value').text
                try:
                    fav = zone.find_element_by_class_name('ProfileNav-item--favorites')
                    fav_number = fav.find_element_by_class_name('ProfileNav-value').text
                except NoSuchElementException:
                    print "Couldn't Find Favourites"

                print "User Stats for user : " + userScreenName + " following: " + following_number + " tweets: " +  tweets_number + " Followers: " +  follower_number + " Favourites: " +fav_number
                usermeta = {'Name' : userScreenName , 'Following' : following_number , 'tweets' : tweets_number  , 'Followers' : follower_number , 'Likes' : fav_number}
                DataDict[tweet]['userMeta'] = dict()

                DataDict[tweet]['userMeta'] = usermeta

            except NoSuchElementException :
                print "Failed to find fields!! for : " + userScreenName

        return DataDict








if __name__ == "__main__":
    query = urllib.pathname2url('Alabama Football: Biggest Questions Defending Champs Must Answer')
    searchObj = SeleniumCrawler("sagarConfig.config")
    # apiObj = tweepyCrawl("sagarConfig.con")

    crawledData = searchObj.doCrawl(searchObj.encodeQuery(query , True) , 3)

    searchObj.getUserInfo(crawledData)
    with open('result2.json', 'w') as fp:
        json.dump(crawledData, fp)
    searchObj.killBrowser()
