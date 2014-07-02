# -*- coding: utf-8 -*-
import re
from twitter import *
from dateutil import parser
import pytz
from termcolor import cprint, colored
import os
import time
import sys
import config
import nmap

####Functions
#Clear console screen
def cls():
    os.system(['clear','cls'][os.name == 'nt'])

def header(nbrOfCon):
    cprint(".____/\       ", "magenta")
    cprint("|    )/  _____    ____   ____   ____ ___  ___ ____  ", "magenta")
    cprint("|    |   \__  \  /    \ /    \_/ __ \\  \/  // __ \ ", "magenta")
    cprint("|    |___ / __ \|   |  \   |  \  ___/ >    <\  ___/ ", "magenta")
    cprint("|_______ (____  /___|  /___|  /\___  >__/\_ \\___  >", "magenta")
    cprint("        \/    \/     \/     \/     \/      \/    \/ ", "magenta")
    print("Bienvenue sur le mur de l'annexe - "+ str(nbrOfCon) +" machines connectées au WIFI")
    print("Hashtag " + colored(config.HASHTAG, "cyan") + " pour apparaitre sur le mur")

def clean(nbrOfCon):
    cls()
    header(nbrOfCon)


def loadTweets(twit,nm):
    nm.scan(hosts='192.168.1.0/24', arguments='-n -sP -T4')
    hosts_list = [(x) for x in nm.all_hosts()]
    nbrOfCon = len(hosts_list)
    tweets = twit.search.tweets(q=config.HASHTAG)
    # Max number of tweet to diplay, we cut the array in loop
    nbrofTweet = min(config.MAX_TWEETS, len(tweets['statuses']))
    clean(nbrOfCon)
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
    print u" " + colored(u"\n".join(text.split("\n")[:3]), "yellow"),
    print u" — " + colored(tweet['user']['name'], "red"),

# Authentication based on https://pypi.python.org/pypi/twitter
twit = Twitter(
    auth=OAuth(config.OAUTH_TOKEN, config.OAUTH_SECRET,
               config.CONSUMER_KEY, config.CONSUMER_SECRET))
nm = nmap.PortScanner() # creates an'instance of nmap.PortScanner

#TODO Do this with a scheduler
while True:
    loadTweets(twit,nm)
    time.sleep(config.REFRESH_TIME)
