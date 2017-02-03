import urlparse
import urllib
import sys
import datetime
import requests
import json


class TwitterAdvancedSearch:

    ''' Get a list of keywords '''
    keywords = []
    since = "2017-01-01"
    till = datetime.datetime.today().strftime('%Y-%m-%d')
    queryBase = "https://twitter.com/search?l=en&q="

    def __init__(self, since = None , till = None ):

        if since != None:
            self.since = since
        if till != None:
            self.till = till



    def getCall(self , queryString ):
        url = "https://twitter.com/search"

        params = {}
        params['l'] = ''
        params['q'] = urllib.quote(queryString)
        params['src'] = 'typd'

        print params


        requestHeaders = {
        'Host': 'twitter.com',
        'Connection': 'keep-alive',
        'Accept':'application/json, text/javascript, */*; q=0.01',
        'X-Push-State-Request': 'true',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
        'X-Asset-Version': '886d3a',
        #'Referer': 'https://twitter.com/search-advanced',
        'Accept-Encoding': 'gzip, deflate, sdch, br',
        'Accept-Language': 'en-US,en;q=0.8,sv;q=0.6,mr;q=0.4,hi;q=0.2'
        #'Cookie': 'ct0=9bcf6f96b74ab9416aa6acaba15ccff2; guest_id=v1%3A148612309356115159; eu_cn=1; _twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCDvO1gNaAToMY3NyZl9p%250AZCIlNjkwMjEwZjJiM2JlN2VjZTQ1ZmY4MDUxMDQ2ZDJjNzk6B2lkIiU2NWFl%250ANjE0Y2M1NmVjMDI5ZDU1NWE0NGFjN2ZkMjVlYg%253D%253D--11449ccd71bf2850774d790c3b68384c06b81eee'
        }
        client = requests.session()
        return client.get(url, headers = requestHeaders, params = params)



    def encodeQuery(self, query  , Exact = True):
        queryString = ''
        if Exact:
            queryString = '"{}"'.format(query) + ' since:' + self.since + ' until:' + self.till
        else:
            queryString = query + ' since:' + self.since + ' until:' + self.till
        return queryString



if __name__ == "__main__":
    query = "Happy holidays"
    searchObj = TwitterAdvancedSearch()
    searchObj. encodeQuery(query , True)

    r = searchObj.getCall(searchObj. encodeQuery(query , True))
    js = json.loads(r.content)
    print js['page']















