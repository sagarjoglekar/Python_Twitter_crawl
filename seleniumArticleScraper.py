import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib
from datetime import datetime , timedelta
import json
from twitterSearch import tweepyCrawl
from selenium.common.exceptions import NoSuchElementException
import ParseTwitterConfig

class seleniumArticleScraper:

    def __init__(self, configFile ):

        config = ParseTwitterConfig.Parser(configFile)
        self.service_log_path = "{}/chromedriver.log".format(".")
        self.service_args = ['--verbose']
        config.parseConfig()
        self.options = webdriver.ChromeOptions()
        #Uncomment this line for Ubuntu
        #self.options.binary_location = config.getChromePath()
        self.driver = config.getChromeDriverPath()
        print self.options
