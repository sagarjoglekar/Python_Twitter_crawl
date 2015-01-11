# Python_Twitter_crawl
A pet project to use Python Twitter API to crawl Hashtags and evaluate emotions

This small app is in the works but you can completely use it to post messages, search friends etc.

You will need a .config file similar to the sample config that is checked it.
Thus change the fields with appropriate fields.
The mail requirements are
* Consumer token
* Consumer Secret
* Access Token
* Access Secret
* Owner

Once you make a .config file with above fields, you should be able to get a connection to your twitter account using

python Oauthtwitter.py 'path/to/valid/user.config'

Actual project will begin now:

For Searching Twitter:

python EmotionCrawl.py user.config --geo 'language' keayword1 keyword2 ...


Third party Libraries Used:
* twitter (python-twitter)
* TwitterSearch
