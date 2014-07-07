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
import twitter
from urllib2 import URLError
import json

####Functions
#Clear console screen
def cls():
    os.system(['clear','cls'][os.name == 'nt'])

def header(num_of_con):
    cprint(".____/\       ", "magenta")
    cprint("|    )/  _____    ____   ____   ____ ___  ___ ____  ", "magenta")
    cprint("|    |   \__  \  /    \ /    \_/ __ \\  \/  // __ \ ", "magenta")
    cprint("|    |___ / __ \|   |  \   |  \  ___/ >    <\  ___/ ", "magenta")
    cprint("|_______ (____  /___|  /___|  /\___  >__/\_ \\___  >", "magenta")
    cprint("        \/    \/     \/     \/     \/      \/    \/ ", "magenta")
    print("Bienvenue sur le mur de l'annexe - "+ str(num_of_con) +" machines connectées au WIFI")
    print("Hashtag " + colored(config.HASHTAG, "cyan") + " pour apparaitre sur le mur")

def clean(num_of_con):
    cls()
    header(num_of_con)

def get_num_of_con():
    nm.scan(hosts='192.168.1.0/24', arguments='-n -sP -T4')
    hosts_list = [(x) for x in nm.all_hosts()]
    return len(hosts_list)

def load_tweets(twit,nm):
    clean(get_num_of_con())

    tweets = None
    error = None

    try:
        tweets = twit.search.tweets(q=config.HASHTAG)

    # URLError
    except URLError:
        error = "Oups ! Je n'arrive plus à me connecter au réseau"

    # Exception thrown by the Twitter object when there is an HTTP error interacting with twitter.com.
    # {"errors":[{"message":"Bad Authentication data","code":215}]}
    except twitter.api.TwitterHTTPError as e:
        error = "Oups ! Je n'arrive plus à me connecter à Twitter (" + get_twitter_error_message(e.response_data) + ")"

    # Base Exception thrown by the Twitter object when there is a general error interacting with the API.
    except twitter.api.TwitterError:
        error = "Oups ! Je n'arrive plus à me connecter à Twitter"

    # Other error
    except:
        error = "Oups ! Je n'arrive plus à récupérer les tweets"

    if error is not None:
       print "\r\n" + colored(error, "red")

    if tweets is not None:
        num_of_tweet = min(config.MAX_TWEETS, len(tweets['statuses']))
        counter = num_of_tweet
        for tweet in tweets['statuses'][:num_of_tweet]:
            load_tweet(tweet)
            counter -= 1
            if counter != 0:
                print
            sys.stdout.flush()

def get_twitter_error_message(str):
    try:
        data = json.loads(str.decode("utf8"))
        message = data["errors"][0]["message"];
    except:
        message = "Unknown error"
    return message.encode("utf8")

def load_tweet(tweet):
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
    load_tweets(twit,nm)
    time.sleep(config.REFRESH_TIME)
