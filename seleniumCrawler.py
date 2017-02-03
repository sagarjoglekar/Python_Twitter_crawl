import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


browser = webdriver.Chrome()
baseUrl =  u'https://twitter.com/search?l=en&q='
query = u'%40Hillary'

url = baseUrl + query

browser.get(url)

time.sleep(1)


body = browser.find_element_by_tag_name('body')

for _ in range(5):
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(1)

tweets = body.find_elements_by_class_name('tweet-text')

for tweet in tweets:
    print(tweet.text)

