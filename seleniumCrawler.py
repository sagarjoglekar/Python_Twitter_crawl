import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import datetime
import urllib



class SeleniumCrawler:

    since = "2013-01-01"
    till = "2013-12-31"#datetime.datetime.today().strftime('%Y-%m-%d')
    queryBase = "https://twitter.com/search?l=en&q="

    def __init__(self, since = None , till = None ):

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


    def doCrawl(self , queryString , pages = 3):
        url = self.queryBase+queryString

        browser = webdriver.Chrome()
        browser.get(url)
        time.sleep(1)
        body = browser.find_element_by_tag_name('body')
        for _ in range(pages):
            tweets = body.find_elements_by_class_name('tweet-text')

            for tweet in tweets:
                print(tweet.text)

            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(1)
        browser.quit()



if __name__ == "__main__":
    query = "Happy holidays"
    searchObj = SeleniumCrawler()
    searchObj. encodeQuery(query , True)
    searchObj.doCrawl(searchObj. encodeQuery(query , True))
