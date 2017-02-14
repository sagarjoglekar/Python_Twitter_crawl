import ConfigParser
import io

class Parser:
    _consumerKey = ""
    _consumerSecret = ""
    _accessToken = ""
    _accessTokenSecret = ""
    _owner = ""
    _ownerId = ""
    _configFilePath = ""
    _maxTweets="100"
    configParser = ConfigParser.RawConfigParser()

    def __init__(self, filepath):
        self._configFilePath = filepath
        print 'Using File : ', filepath

        try:
            self.configParser.readfp(open(filepath, 'r'))
        except:
            print 'Invalid cofig file path, Cannot open', filepath

    def parseConfig(self):
        try:
            self._consumerKey =  self.configParser.get('User_Twitter_Config','ConsumerKey')
            self._consumerSecret = self.configParser.get('User_Twitter_Config','ConsumerSecret')
            self._accessToken = self.configParser.get('User_Twitter_Config','AccessToken')
            self._accessTokenSecret = self.configParser.get('User_Twitter_Config','AccessTokenSecret')
            self._owner = self.configParser.get('User_Twitter_Config','Owner')
            self._ownerId = self.configParser.get('User_Twitter_Config','OwnerId')
            self._maxTweets = self.configParser.get('User_Twitter_Config','maxTweets')
            self._chromePath = self.configParser.get('User_Twitter_Config','chromePath')
            self._chromeDriverPath = self.configParser.get('User_Twitter_Config','chromeDriverPath')

        except:
            print 'Invalid configuration'


    def getConsumerKey(self):
        return self._consumerKey

    def getConsumerSecret(self):
        return self._consumerSecret

    def getAccessToken(self):
        return self._accessToken

    def getAccessTokenSecret(self):
        return self._accessTokenSecret

    def getOwner(self):
        return self._owner

    def getOwnerId(self):
        return self._ownerId

    def getMaxTweets(self):
        return self._maxTweets

    def getChromePath(self):
        return self._chromePath

    def getChromeDriverPath(self):
        return self._chromeDriverPath


