from twitter import *
import json
import re

#setting OAUTH
OAUTH_TOKEN = '185728545-U5P4eOXB60JXGOVSDYxHkUf1bDJfN3YG91ssfwW4'
OAUTH_SECRET = 'BDEWuzx3EvbgMWQNm75fWQA4TS5rJv5O6PxBQZRc7s'
CONSUMER_KEY = 'JFbD2IpLnC0Iwm11f6Kltw'
CONSUMER_SECRET = 'JNLMABmIq2qLCIwLTIIr4noGNN9QRelBrlywz2GKoUo'

#set search query and filename to be save
search_query = ":)"
filename="pos%r.txt"

#regex to search username, RT, smiley
regexsearchquery = '(@([A-Za-z0-9_]+))|(RT)|([\&\-\.\/\(\)=:;]+)|((?::|;|=)(?:-)?(?:\)|D|P))'
regexobj = re.compile(regexsearchquery, re.MULTILINE)

t = Twitter(
            auth=OAuth(OAUTH_TOKEN, OAUTH_SECRET,
                       CONSUMER_KEY, CONSUMER_SECRET)
           )

current_max_id = 0

for i in range(1,11):
    #make file name different each 100 line
    filetowrite = (filename % i)
    print filetowrite

    try:
        archive = open(filetowrite,"w")
    except IOError as e:
        err("Cannot save tweets: %s" % str(e))

    if current_max_id == 0:
        print i
        tweets = t.search.tweets(q=search_query, count=100, geocode="-7.76505792,110.41909636,200km")
        current_max_id = tweets['search_metadata']['max_id_str']
    else:
        print i
        tweets = t.search.tweets(q=search_query, count=100, geocode="-7.76505792,110.41909636,200km", since_id = current_max_id)

    for k in range(len(tweets['statuses'])):
        #print tweets['statuses'][k]['text']
        tweetstring = tweets['statuses'][k]['text'].encode('utf8')
        #print tweetstring
        cleanedtweet = regexobj.sub('', tweetstring)
        #print cleanedtweet
        #print "\n"
        archive.write(cleanedtweet)
        archive.write("\n")

    #close the file
    archive.close()
