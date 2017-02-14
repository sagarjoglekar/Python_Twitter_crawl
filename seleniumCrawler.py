import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib
from datetime import datetime , timedelta
import json
from twitterSearch import tweepyCrawl
from selenium.common.exceptions import NoSuchElementException
import ParseTwitterConfig


class SeleniumCrawler:

    #since = "2013-01-01"
    #till = "2013-12-31"#datetime.datetime.today().strftime('%Y-%m-%d')
    since = (datetime.today() - timedelta(days=10)).strftime('%Y-%m-%d')
    till = datetime.today().strftime('%Y-%m-%d')
    queryBase = "https://twitter.com/search?l=en&q="

    def __init__(self, configFile , since = None , till = None ):

        config = ParseTwitterConfig.Parser(configFile)
        self.service_log_path = "{}/chromedriver.log".format(".")
        self.service_args = ['--verbose']
        config.parseConfig()
        self.options = webdriver.ChromeOptions()
        #Uncomment this line for Ubuntu
        #self.options.binary_location = config.getChromePath()
        self.driver = config.getChromeDriverPath()
        print self.options

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

    def doCrawl(self , queryString , pages = 3):
        url = self.queryBase+queryString
        print url
        tweetData = dict()

        browser = webdriver.Chrome(self.driver,
        chrome_options=self.options,
        service_args=self.service_args,
        service_log_path=self.service_log_path)

        browser.get(url)
        time.sleep(1)

        body = browser.find_element_by_tag_name('body')
        for _ in range(pages):
            tweets = body.find_elements_by_class_name('js-stream-item')


            for tweet in tweets:
                user = tweet.find_element_by_class_name('tweet')

                attrs = browser.execute_script('var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;', user)

                tweetData[attrs['data-tweet-id']] = dict()
                tweetData[attrs['data-tweet-id']]['meta'] = attrs
                tweetData[attrs['data-tweet-id']]['text'] = user.text
                print tweetData[attrs['data-tweet-id']]
                print "\n"

            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(1)
        browser.quit()
        return tweetData

    def getUserInfo(self , DataDict):
        baseUrl = "https://www.twitter.com/"
        'ProfileNav-list'

        browser = webdriver.Chrome(self.driver,
        chrome_options=self.options,
        service_args=self.service_args,
        service_log_path=self.service_log_path)

        for tweet in DataDict:
            userScreenName = DataDict[tweet]['meta']['data-screen-name']
            url = baseUrl + userScreenName

            browser.get(url)
            body = browser.find_element_by_tag_name('body')
            zone = body.find_element_by_class_name('ProfileNav')
            try :

                following = zone.find_element_by_class_name('ProfileNav-item--following')
                following_number = following.find_element_by_class_name('ProfileNav-value').text

                tweets = zone.find_element_by_class_name('ProfileNav-item--tweets')
                tweets_number = tweets.find_element_by_class_name('ProfileNav-value').text

                follower = zone.find_element_by_class_name('ProfileNav-item--followers')
                follower_number = follower.find_element_by_class_name('ProfileNav-value').text

                fav = zone.find_element_by_class_name('ProfileNav-item--favorites')
                fav_number = fav.find_element_by_class_name('ProfileNav-value').text

                print "User Stats for user : " + userScreenName + " following: " + following_number + " tweets: " +  tweets_number + " Followers: " +  follower_number + " Favourites: " +fav_number
                usermeta = {'Name' : userScreenName , 'Following' : following_number , 'tweets' : tweets_number  , 'Followers' : follower_number , 'Likes' : fav_number}
                DataDict[tweet]['userMeta'] = dict()

                DataDict[tweet]['userMeta'] = usermeta

            except NoSuchElementException :
                print "Failed to find fields!! for : " + userScreenName

        browser.quit()
        return DataDict








if __name__ == "__main__":
    query = urllib.pathname2url('#largerhands')
    searchObj = SeleniumCrawler("sagarConfig.config")
    # apiObj = tweepyCrawl("sagarConfig.con")

    crawledData = searchObj.doCrawl(searchObj. encodeQuery(query , True) , 1)

    searchObj.getUserInfo(crawledData)
    with open('result2.json', 'w') as fp:
        json.dump(crawledData, fp)