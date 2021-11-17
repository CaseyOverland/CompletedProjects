from bs4 import BeautifulSoup
import requests
import re
import random
import tweepy
import time
import os
from tqdm import tqdm

#            DEFINITIONS             #

keys_clean = []
nouns_list_clean = []
verbs_list_clean = []
adjectives_list_clean = []
all_headlines = []
links = []
urls_clean = []
headline = ""
adjectivesInHeadline = ""
nounsInHeadline = ""
verbsInHeadline = ""
nouns = ""
adjectives = ""
verbs = ""
doc = ""
check = ""
a_tags = []

listsLocation = (os.getcwd() + "\\Misinfo_bot Files")
keys = open(listsLocation + "\\Misinfo_bot Keys.txt", "r").readlines()

for j in keys:
    keys_clean.append(j.strip("\n"))
while "" in keys_clean:
    keys_clean.remove("")
keys = [keys_clean[1], keys_clean[3], keys_clean[7], keys_clean[9]]
CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET = keys[0], keys[1], keys[2], keys[3]
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

twitter_API = tweepy.API(auth)
api = tweepy.API(auth)
urls = open(listsLocation + "\\URL List.txt", "r").readlines()
for y in urls:
    urls_clean.append(y.strip("\n"))
urls = urls_clean


#           FUNCTIONS           #


def get_last_received(my_dms):
    for dm in my_dms:
        if dm.message_create['target']['recipient_id'] == 'my_user_id':
            print(dm)
            return dm


def headline_scrapper():
    global check, doc, all_headlines, links
    links = []
    all_headlines = []
    check = 0
    for x in tqdm(urls):
        url = x
        result = requests.get(url).text
        doc = BeautifulSoup(result, "html.parser")
        h3_tag = doc.findChildren("h3")
        for a in h3_tag:
            a_tag = a.find(["a"])
            a_tags.append(a_tag)
            headline_found = a_tag.find(text=True)
            all_headlines.append(headline_found)
        for a in doc.find_all("h3"):
            for link in a.find_all("a"):
                link = link.get("href")
                link = link[1:]
                links.append(link)
    print("\n" * 10)
    print("\nToday's Headlines:\n")
    for x in all_headlines:
        print('"' + x + '"')


def headline_picker():
    print("Choosing Headline...")
    headline_chosen = all_headlines[random.randint(1, len(all_headlines))]
    print("\nHeadline Chosen: \n")
    headline_chosen = list(headline_chosen.split(" "))
    print(headline_chosen)
    return headline_chosen


def nouns_list():
    f = open(listsLocation + "\\ListOfNouns.txt", "r")
    for x in f:
        nouns_list_clean.append(x.strip())
    return nouns_list_clean


def verbs_list():
    f = open(listsLocation + "\\ListOfVerbs.txt", "r")
    for x in f:
        verbs_list_clean.append(x.strip())
    return verbs_list_clean


def adjectives_list():
    f = open(listsLocation + "\\ListOfAdjectives.txt", "r")
    for x in f:
        adjectives_list_clean.append(x.strip())
    return adjectives_list_clean


def marker():
    global adjectivesInHeadline
    global nounsInHeadline
    global verbsInHeadline
    global headline
    global nouns
    global adjectives
    global verbs

    adjectives = adjectives_list()
    verbs = verbs_list()
    nouns = nouns_list()
    no_replace = True
    while no_replace:
        headline = headline_picker()
        adjectivesInHeadline = []
        nounsInHeadline = []
        verbsInHeadline = []
        print("Looking for Adjectives...")
        for x in tqdm(headline, leave=False):
            if x in adjectives:
                adjectivesInHeadline.append(x)
        print("Looking for Nouns...")
        for x in tqdm(headline, leave=False):
            if x in nouns:
                nounsInHeadline.append(x)
        print("Looking for Verbs...")
        for x in tqdm(headline, leave=False):
            if x in verbs:
                verbsInHeadline.append(x)

        if (len(adjectivesInHeadline)) > 0:
            print("\nAdjective(s) Found")
        if (len(nounsInHeadline)) > 0:
            print("\nNoun(s) Found")
        if (len(verbsInHeadline)) > 0:
            print("\nVerb(s) Found")

        if (len(adjectivesInHeadline)) > 0 or (len(nounsInHeadline)) > 0 or (len(verbsInHeadline)) > 0:
            for x in nounsInHeadline:
                if x in verbsInHeadline:
                    if random.randint(1, 2) == 1:
                        verbsInHeadline.remove(x)
                    else:
                        nounsInHeadline.remove(x)
            print("Adjectives: \n" + str(adjectivesInHeadline) + '\n')
            print("Nouns: \n" + str(nounsInHeadline) + '\n')
            print("Verbs: \n" + str(verbsInHeadline) + '\n')
            no_replace = False
        else:
            no_replace = True
            print("No Replacement Found")


def replacer():
    global headline
    global new_phrase

    print("\nReplacement Started\n")
    empty = " "
    headline = (empty.join(headline))
    adjective, noun, verb = [], [], []
    for _ in adjectives:
        adjective.append(adjectives[random.randint(0, (len(adjectives) - 1))])
    for _ in nouns:
        noun.append(nouns[random.randint(0, (len(nouns) - 1))])
    for _ in verbs:
        verb.append(verbs[random.randint(0, (len(verbs) - 1))])

    new_phrase = headline
    for x in range(len(adjectivesInHeadline)):
        new_phrase = re.sub(adjectivesInHeadline[x], adjective[x], headline)
        print(str(new_phrase))

    for x in range(len(nounsInHeadline)):
        new_phrase = re.sub(nounsInHeadline[x], noun[x], new_phrase)
        print(str(new_phrase))

    for x in range(len(verbsInHeadline)):
        new_phrase = re.sub(verbsInHeadline[x], verb[x], new_phrase)
        print(str(new_phrase))


def tweet_maker():
    global twitter_post
    global link_finder
    link_finder = all_headlines.index(headline)
    twitter_post = (new_phrase + "\n\n-Misinfo_Bot")


run_again = True
read_messages = []
print("Misinfo_Bot backend\n")
while run_again:
    tweets = []
    links = []
    new_phrase = ""
    twitter_post = ""
    link_finder = ""

    print("Begining Search...")
    headline_scrapper()
    marker()
    time.sleep(1)
    print("Starting Replacement...")
    replacer()
    print("Replacement Finished!\nForming Tweet...")
    tweet_maker()

    print("\nI will now post \"" + new_phrase + "\" on Twitter.\n")
    api.update_status(twitter_post)
    time.sleep(30)
    while len(tweets) < 1:
        print("Searching... ")
        tweets = api.user_timeline(screen_name="@Misinfo_Bot", count=1, include_rts=False, tweet_mode='extended')
        time.sleep(5)
    tweet = tweets[0]
    print("Tweet Found...")
    if new_phrase in tweet.full_text:
        sn = tweet.user.screen_name
        m = "@Misinfo_Bot\nOriginal Link to Headline:\n- https://news.google.com" + links[link_finder]
        s = api.update_status(m, tweet.id, auto_populate_reply_metadata=True)
        print("\nReplying to Tweet.\n")

    hours = random.randint(3, 6)
    print("Sleeping for " + str(hours) + " hours\n")
    seconds = hours * 200
    time.sleep(seconds)
