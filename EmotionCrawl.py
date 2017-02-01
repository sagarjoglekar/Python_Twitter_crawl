import sys
import twitterSearch
from optparse import OptionParser

keywords = []
geo = ''
FileRoot = ''
words = []

if __name__ == "__main__":

    if len(sys.argv) < 3:
        print 'Use search correctly:python  EmotionCrawl <user.config> --geo(optional) <place> --radius(optional) <radius in meters> <keyphraseList.list> File>'
        print ' If geotag absent, a default world level would be used '
        sys.exit()
    else:
        if str(sys.argv[1]).split(".")[-1] == "config":
            filepath = str(sys.argv[1])
        else:
            print "second argument needs to be a .config file with your twitter api credentials"

        if str((sys.argv[2]))=='--geo':
            geo = str((sys.argv[3]))
            rad = float(sys.argv[4])
            keywords = str(sys.argv[5])
        else:
            keywords = str(sys.argv[2])

        if keywords.split(".")[-1].strip() == "list":
            f  = open(keywords,"rb")
            words = f.readlines()
        else:
            print keywords
            print "Please input a .list file with keyphrases seperated by newlines"


    search = twitterSearch.EmoCrawl(filepath, words, geo)

    #search.makePost();

    search.search()
