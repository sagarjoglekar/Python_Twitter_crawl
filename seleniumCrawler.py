import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib
from datetime import datetime , timedelta
import json
from twitterSearch import tweepyCrawl
from selenium.common.exceptions import NoSuchElementException
import ParseTwitterConfig
from pyvirtualdisplay import Display



class SeleniumCrawler:

    since = "2013-01-01"
    till = "2014-12-31"#datetime.datetime.today().strftime('%Y-%m-%d')
    #since = (datetime.today() - timedelta(days=10)).strftime('%Y-%m-%d')
    #till = datetime.today().strftime('%Y-%m-%d')
    queryBase = "https://twitter.com/search?l=en&q="

    def __init__(self, configFile , since = None , till = None ):

        config = ParseTwitterConfig.Parser(configFile)
        self.service_log_path = "{}/chromedriver.log".format(".")
        self.service_args = ['--verbose']
        config.parseConfig()
        self.options = webdriver.ChromeOptions()
        #Uncomment this line for Ubuntu
        self.options.binary_location = config.getChromePath()
        self.driver = config.getChromeDriverPath()
        print self.options

        #self.browser = webdriver.Chrome(self.driver,chrome_options=self.options,service_args=self.service_args,service_log_path=self.service_log_path)
        self.browser = webdriver.Chrome()

        if since != None:
            self.since = since
        if till != None:
            self.till = till



    def getAttributes(self , element):
        #attributes = {}
        attributes = self.browser.execute_script('var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;', element)
        return attributes


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
        try:
            body = self.browser.find_element_by_tag_name('body')
        except NoSuchElementException:
            print "Couldn't find body, moving on"
            time.sleep(2)
            return tweetData

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

                attrs = self.getAttributes(meta)

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

    def getUserInfo(self , usernames):
        baseUrl = "https://www.twitter.com/"
        DataDict = {}

        for uname in usernames:
            print "crawling User : " + uname
            userScreenName = uname
            url = baseUrl + userScreenName
            tweets_number = str(0)
            following_number = str(0)
            follower_number = str(0)
            fav_number = str(0)


            self.browser.get(url)
            time.sleep(1)
            try:
                body = self.browser.find_element_by_tag_name('body')
            except NoSuchElementException:
                print "Couldn't find body, moving on"
                time.sleep(2)
                continue

            try :
                zone = body.find_element_by_class_name('ProfileNav-list')

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
                    continue

                print "User Stats for user : " + userScreenName + " following: " + following_number + " tweets: " +  tweets_number + " Followers: " +  follower_number + " Favourites: " +fav_number
                usermeta = {'Name' : userScreenName , 'Following' : following_number , 'tweets' : tweets_number  , 'Followers' : follower_number , 'Likes' : fav_number}
                DataDict[uname] = dict()

                DataDict[uname] = usermeta

            except NoSuchElementException :
                print "Failed to find fields!! for : " + userScreenName
                continue

        return DataDict



    def crawlTweet(self , tweetDict ):
        root = "https://twitter.com"
        permaLink = tweetDict['meta']['data-permalink-path']
        url = root + permaLink
        print url
        self.browser.get(url)
        time.sleep(1)
        attributes = {}
        try:
            body = self.browser.find_element_by_class_name('PermalinkOverlay-body')
        except NoSuchElementException:
            print "Couldn't find body, moving on"
            time.sleep(2)
            return tweetDict
        try:
            tweet = body.find_element_by_class_name('tweet')
        except NoSuchElementException:
            print "Couldn't Find tweet"
            return tweetDict
        try:
            mediaElement = tweet.find_element_by_class_name('AdaptiveMediaOuterContainer')
            attributes = mediaElement.get_attribute('innerHTML')
            tweetDict['hasMedia'] = True
            tweetDict['mediaHTML'] = attributes
        except NoSuchElementException:
            try:
                cardElement = tweet.find_element_by_class_name('card2')
                try:
                    attributes = cardElement.get_attribute('innerHTML')
                    tweetDict['hasCard'] = True
                    tweetDict['cardHTML'] = attributes
                except:
                    print "Cant get card"
            except NoSuchElementException:
                print "tweet is a plain text tweet"
                return tweetDict
        return tweetDict




if __name__ == "__main__":
    #query = urllib.pathname2url('Alabama Football: Biggest Questions Defending Champs Must Answer')
    display = Display(visible=0, size=(800, 600))
    display.start()
    # tweetFile = "NewsCrawlDir/0ad446db97de1168675b4cc1c9fa56566c5025964fa1cd941e27e27f.json"
    # fp = open(tweetFile,"rb")
    # js = json.load(fp)

    searchObj = SeleniumCrawler("sagarConfig.config")

    #crawledData = searchObj.doCrawl(searchObj.encodeQuery(query , True) , 3)
    # for k in js.keys():
    #     newDict = searchObj.crawlTweet(js[k])
    #     print newDict
    #     attributes = searchObj.getAttributes()
    #     print attributes


    data = searchObj.getUserInfo(['sagarjoglekar','avraman'])
    print data
    # with open('result2.json', 'w') as fp:
    #     json.dump(crawledData, fp)
    searchObj.killBrowser()
    display.stop()
