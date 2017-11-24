from seleniumCrawler import SeleniumCrawler
import json
import sys
import os
from pyvirtualdisplay import Display
import time

if __name__ == "__main__":
    if len(sys.argv) == 2:
        linkfile = sys.argv[1]
        print "Extracting userdata for " + linkfile
        if os.path.exists(linkfile):
            print "extracting ... "
            with open(linkfile,'rb') as f:
                lines = f.readlines()

            usernames = {}
            for l in lines[1:]:
                parts = l.split('|')
                name = parts[4]
                if name not in usernames:
                    usernames[name] = 1
                else:
                    usernames[name]+=1

            with open("usernames.json" , 'wb') as f:
                json.dump(usernames,f)
    else:
        with open("usernames.json" , 'rb') as f:
            usernames = json.load(f)



    print "found %d usernames to look for" %(len(usernames))

    #crawlnames = ['sagarjoglekar', 'realdonaldtrump' , 'mad_astronaut' , 'billnye' , 'iamsrk']

    crawlnames = usernames.keys();
    crawledFiles = os.listdir("UserCrawlDir/")
    crawledUsers = []
    for l in crawledFiles:
        with open("UserCrawlDir/"+l,'rb') as f:
            usrs = json.load(f)
        crawledUsers = list(set(crawledUsers + usrs.keys()))

    finalNames = [k for k in crawlnames if k not in crawledUsers]

    print "Starting crawl of %d usernames"%(len(finalNames))

    for start, end in zip(range(0, len(finalNames), 200), range(200, len(finalNames), 200)):
        print "Creating selenium object"
        display = Display(visible=0, size=(800, 600))
        display.start()
        searchObj = SeleniumCrawler("sagarConfig.config")

        data = searchObj.getUserInfo(finalNames[start:end])


        print "Killing chrome driver and selenium"
        searchObj.killBrowser()
        display.stop()


        with open("UserCrawlDir/fragment_"+ str(int(time.time())) + "_userstats.json",'wb') as f:
            json.dump(data,f)
        print "Saved User Stats Fragment!!"
