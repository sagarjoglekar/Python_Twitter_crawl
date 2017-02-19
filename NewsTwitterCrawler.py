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
    #os.environ["DISPLAY"] = ":10"
    os.system('pgrep chrome | xargs kill -9')
    newsFile = "NewsArts02.json"
    Dir = "NewsCrawlDir/"
    arts = loadJson(newsFile)
    searchObj = SeleniumCrawler("sagarConfig.config")
    iters = 0
    for i in range(len(arts.keys())):
        #if iters == 10:
        #    sys.exit(0)
        k = arts.keys()[i]
        print "Crawling titlenumber %d of %d" %(i,len(arts.keys()))
        hashes = getCrawledHashes(Dir)
        if hashlib.sha224(arts[k]['title'].encode("utf-8")).hexdigest() not in hashes:
            print "Searching for : " + arts[k]['title'].encode("utf-8")
            query = urllib.pathname2url(arts[k]['title'].encode("utf-8"))

            crawledData = searchObj.doCrawl(searchObj. encodeQuery(query , False) , 3)

            searchObj.getUserInfo(crawledData)
            filename = Dir + str( hashlib.sha224(arts[k]['title'].encode("utf-8")).hexdigest() ) + ".json"
            with open(filename, 'w') as fp:
                json.dump(crawledData, fp)

            iters+=1
        else:
            print "Title Already crawled"

    print "Cleaning up !"
    searchObj.killBrowser()






