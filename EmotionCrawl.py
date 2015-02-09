import sys
import twitterSearch
from optparse import OptionParser

keywords = []
geo = ''
filepath = ''

if len(sys.argv) < 3:
    print 'Use search correctly: twitterSearch user.config --geo(optional) place --radius(optional) radius in meters keyword1 keyword2 .... '
    print ' If geotag absent, a default world level would be used '
    sys.exit()
else:
    filepath = str(sys.argv[1])

    if str((sys.argv[2]))=='--geo':
        geo = str((sys.argv[3]))
        rad = float(sys.argv[4])
        keywords = sys.argv[5:]
    else:
        keywords = sys.argv[2:]

search = twitterSearch.EmoCrawl(filepath, keywords, geo)

search.makePost();

search.search()
