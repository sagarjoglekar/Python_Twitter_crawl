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


