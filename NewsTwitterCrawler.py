from seleniumCrawler import SeleniumCrawler
import json
import urllib
import hashlib
from os import walk
import os
import sys


def loadJson(file):
    with open(file , 'rb') as fp:
        newsArts = json.load(fp)
    return newsArts

def getCrawledHashes(dir):
    files = []
    for (dirpath, dirnames, filenames) in walk(dir):
        files.extend(filenames)
        break
    hashes = []
    for f in files:
        hashes.append(f.split('.')[0])
    return hashes


if __name__ == "__main__":
    os.environ["DISPLAY"] = ":10"
    os.system('pgrep chrome | xargs kill -9')
    newsFile = "NewsArts02.json"
    Dir = "NewsCrawlDir/"
    arts = loadJson(newsFile)
    searchObj = SeleniumCrawler("sagarConfig.config")
    iters = 0
    for i in  arts.keys():
        if iters == 10:
            sys.exit(0)

        hashes = getCrawledHashes(Dir)
        if hashlib.sha224(arts[i]['title'].encode("utf-8")).hexdigest() not in hashes:
            print "Searching for : " + arts[i]['title']
            query = urllib.pathname2url(arts[i]['title'].encode("utf-8"))

            crawledData = searchObj.doCrawl(searchObj. encodeQuery(query , True) , 3)

            searchObj.getUserInfo(crawledData)
            filename = Dir + str( hashlib.sha224(arts[i]['title'].encode("utf-8")).hexdigest() ) + ".json"
            with open(filename, 'w') as fp:
                json.dump(crawledData, fp)

            iters+=1
        else:
            print "Title Already crawled"

    print "Cleaning up !"
    searchObj.killBrowser()






