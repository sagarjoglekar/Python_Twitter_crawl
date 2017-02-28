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
    #os.system('pgrep chrome | xargs kill -9')
    tweetDir = "oldNewsCrawlDir/"
    Dir = "NewsCrawlDir/"
    searchObj = SeleniumCrawler("sagarConfig.config")
    iters = 0
    tweetFiles = os.listdir(tweetDir)
    for i in tweetFiles:
        crawledTweets = os.listdir(Dir)
        if i not in crawledTweets:
            print "Parsing  : " + i
            jsTweets = loadJson(tweetDir + i)
            revisedjs = dict()
            for k in jsTweets:
                crawledData = searchObj.crawlTweet(jsTweets[k])
                revisedjs[k] = dict()
                revisedjs[k] = crawledData
            filename = Dir + i
            with open(filename, 'w') as fp:
                json.dump(revisedjs, fp)
            iters+=1
        else:
            print "File already revised"

    print "Cleaning up !"
    searchObj.killBrowser()
