from seleniumCrawler import SeleniumCrawler
import json
import sys
import os
from pyvirtualdisplay import Display

if __name__ == "__main__":
    linkfile = sys.argv[1]
    print "Extracting userdata for " + linkfile
    if os.path.exists(linkfile):
        print "extracting ... "
        with open(linkfile,'rb') as f:
            lines = f.readlines()

        usernames = []
        for l in lines:
            parts = l.split(',')
            name = parts[4]
            if name not in usernames:
                usernames.append(name)

        print "Creating selenium object"
        display = Display(visible=0, size=(800, 600))
        display.start()
        searchObj = SeleniumCrawler("sagarConfig.config")
        data = searchObj.getUserInfo(usernames)
        json.dump(data,open(linkfile+"_userstats.json"),'wb')

        print "Saved User Stats"
        searchObj.killBrowser()
        display.stop()
