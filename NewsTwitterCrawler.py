from seleniumCrawler import SeleniumCrawler
import json
import urllib
import hashlib

def loadJson(file):
    with open(file , 'rb') as fp:
        newsArts = json.load(fp)

    return newsArts


if __name__ == "__main__":
    newsFile = "NewsArts02.json"
    Dir = "NewsCrawlDir/"
    arts = loadJson(newsFile)
    searchObj = SeleniumCrawler("sagarConfig.config")

    for i in  arts.keys()[:3]:

        query = urllib.pathname2url(arts[i]['title'])

        crawledData = searchObj.doCrawl(searchObj. encodeQuery(query , True) , 1)

        searchObj.getUserInfo(crawledData)
        filename = Dir + str(hashlib.sha224(i).hexdigest())+ ".json"
        with open(filename, 'w') as fp:
            json.dump(crawledData, fp)



