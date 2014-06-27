# -*- coding: utf-8 -*-
import re
from twitter import *
from dateutil import parser
import pytz
from termcolor import cprint, colored
import os
import time
import sys


HASHTAG="#WALLNEX"
REFRESH_TIME=30
MAX_TWEETS=10
OAUTH_TOKEN="****"
OAUTH_SECRET="****"
CONSUMER_KEY="****"
CONSUMER_SECRET="****"

####Functions
#Clear console screen
def cls():
    os.system(['clear','cls'][os.name == 'nt'])
    
def header():
    cprint(".____/\       ", "magenta")
    cprint("|    )/  _____    ____   ____   ____ ___  ___ ____  ", "magenta")
    cprint("|    |   \__  \  /    \ /    \_/ __ \\  \/  // __ \ ", "magenta")
    cprint("|    |___ / __ \|   |  \   |  \  ___/ >    <\  ___/ ", "magenta")
    cprint("|_______ (____  /___|  /___|  /\___  >__/\_ \\___  >", "magenta")
    cprint("        \/    \/     \/     \/     \/      \/    \/ ", "magenta")
    print("Bienvenue sur le mur de l'annexe")
    print("Hashtag " + colored(HASHTAG, "cyan") + " pour apparaitre sur le mur")
    
def clean():
    cls()
    header()


def loadTweets(twit):
    tweets = twit.search.tweets(q=HASHTAG)
    # Max number of tweet to diplay, we cut the array in loop
    nbrofTweet = min(MAX_TWEETS, len(tweets['statuses']))
    clean()
    counter = nbrofTweet
    for tweet in tweets['statuses'][:nbrofTweet]:
    	loadTweet(tweet)
        counter -= 1
        if counter != 0:
            print
        sys.stdout.flush()

def loadTweet(tweet):
    print(" ")
    date_utc = parser.parse(tweet['created_at']).replace(tzinfo=pytz.utc)
    local_tz = pytz.timezone("Europe/Paris")
    date = date_utc.astimezone(local_tz)
    text = tweet['text']

    # Strip URLs
    text = re.sub(r'https?:\/\/[a-zA-Z0-9\.\/\+\?]+', '', text).strip()

    print colored(date.strftime("[%H:%M:%S]"), "cyan"),
    print " " + colored("\n".join(text.split("\n")[:3]), "yellow"),
    print u" — " + colored(tweet['user']['name'], "red"),

# Authentication based on https://pypi.python.org/pypi/twitter
twit = Twitter(
    auth=OAuth(OAUTH_TOKEN, OAUTH_SECRET,
               CONSUMER_KEY, CONSUMER_SECRET))


#TODO Do this with a scheduler
while True:
    loadTweets(twit)
    time.sleep(REFRESH_TIME)
