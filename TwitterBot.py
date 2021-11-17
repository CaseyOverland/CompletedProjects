import random
import tweepy
import time
import re
import os


listsLocation = (os.getcwd() + "\\Unsettling Bot INFO")
CONSUMER_KEY = "b9hBsJ9n9Dhih0G4Y8jKJqvhj"
CONSUMER_SECRET = "tuStpZS1JQ5nEmTvDevTA6nSLUXjr79mkCkyo2CuYwrrKew4yH"
ACCESS_KEY = "1375484946672799745-RBh3oxvnKJWzW3nSud4zOSRBNZY5vw"
ACCESS_SECRET = "IaCQ6LQ7L4L11LZlpr36bVfRRMzBS6J3GzwkZHvPVNfS5"
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

twitter_API = tweepy.API(auth)
api = tweepy.API(auth)

#####################
#
# Definitions
#
#####################
global oldPhrase
global verbs
global nouns
global adjectives
global otherWords
global noReplace


def templates():
    template_list = []
    f = open(listsLocation + "\\ListOfPhrases.txt", "r")
    for x in f:
        template_list.append(x.strip())
    length = len(template_list)
    pick_template = template_list[random.randint(1, (length - 1))]
    pick_template = list(pick_template.split(" "))
    print("Template Chosen:\n" + str(pick_template) + "\n")
    return pick_template


def nouns_list():
    nouns_list_clean = []
    f = open(listsLocation + "\\ListOfNouns.txt", "r")
    for x in f:
        nouns_list_clean.append(x.strip())
    return nouns_list_clean


def verbs_list():
    verbs_list_clean = []
    f = open(listsLocation + "\\ListOfVerbs.txt", "r")
    for x in f:
        verbs_list_clean.append(x.strip())
    return verbs_list_clean


def adjectives_list():
    adjectives_list_clean = []
    f = open(listsLocation + "\\ListOfAdjectives.txt", "r")
    for x in f:
        adjectives_list_clean.append(x.strip())
    return adjectives_list_clean


def marker():
    global adjectivesInTemplate
    global nounsInTemplate
    global verbsInTemplate
    global template
    global nouns
    global adjectives
    global verbs

    adjectives = adjectives_list()
    verbs = verbs_list()
    nouns = nouns_list()
    no_replace = True
    while no_replace:
        template = templates()
        adjectivesInTemplate = []
        nounsInTemplate = []
        verbsInTemplate = []
        length = (len(template))
        for x in template:
            if x in adjectives:
                adjectivesInTemplate.append(x)
        for x in template:
            if x in nouns:
                nounsInTemplate.append(x)
        for x in template:
            if x in verbs:
                verbsInTemplate.append(x)

        if (len(adjectivesInTemplate)) > 0:
            print("\nAdjective Found:")
            print(str(adjectivesInTemplate) + '\n')

        if (len(nounsInTemplate)) > 0:
            print("\nNoun Found:")
            print(str(nounsInTemplate) + '\n')

        if (len(verbsInTemplate)) > 0:
            print("\nVerb Found:")
            print(str(verbsInTemplate) + '\n')

        if (len(adjectivesInTemplate)) > 0 or (len(nounsInTemplate)) > 0 or (len(adjectivesInTemplate)) > 0:
            no_replace = False
        else:
            no_replace = True
            print("No Replacement Found")


def replacer():
    global template
    global newPhrase

    print("\nReplacement Started\n")
    empty = " "
    template = (empty.join(template))
    adjective, noun, verb = [], [], []
    for _ in adjectives:
        adjective.append(adjectives[random.randint(0, (len(adjectives) - 1))])
    for _ in nouns:
        noun.append(nouns[random.randint(0, (len(nouns) - 1))])
    for _ in verbs:
        verb.append(verbs[random.randint(0, (len(verbs) - 1))])

    newPhrase = template
    for x in range(len(adjectivesInTemplate)):
        newPhrase = re.sub(adjectivesInTemplate[x], adjective[x], template)
        print(str(newPhrase))

    for x in range(len(nounsInTemplate)):
        newPhrase = re.sub(nounsInTemplate[x], noun[x], newPhrase)
        print(str(newPhrase))

    for x in range(len(verbsInTemplate)):
        newPhrase = re.sub(verbsInTemplate[x], verb[x], newPhrase)
        print(str(newPhrase))


def new_phrases():
    marker()
    replacer()
    print("I will now post \"" + newPhrase + "\"  on twitter")
    api.update_status(newPhrase)


while True:
    new_phrases()
    hours = random.randint(3, 5)
    print("\nsleeping for " + str(hours) + " hours")
    seconds = hours * 200
    time.sleep(seconds)
