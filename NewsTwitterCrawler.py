from seleniumCrawler import SeleniumCrawler
import json


def loadJson(file):
    with open(file , 'rb') as fp:
        newsArts = json.load(fp)

    return newsArts


if __name__ == "__main__":
    newsFile = "NewsArts02.json"
    arts = loadJson(newsFile)

    print arts.keys()
