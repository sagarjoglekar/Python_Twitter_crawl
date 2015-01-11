import sys
import twitterSearch


keywords = []
geo = 'en'
filepath = ''

if len(sys.argv) < 3:
    print 'Use search correctly: twitterSearch user.config --geo geotag keyword1 keyword2 .... '
    print ' If geotag absent, a default would be used '
    sys.exit()
else:
    filepath = str(sys.argv[1])

    if str((sys.argv[2]))=='--geo':
        geo = str((sys.argv[3]))
        keywords = sys.argv[4:]
    else:
        keywords = sys.argv[2:]

search = twitterSearch.EmoCrawl(filepath, keywords, geo)

search.makePost();

search.search()
