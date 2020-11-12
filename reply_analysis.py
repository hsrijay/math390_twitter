import json
import re

# figure out what tweets/replies we want to pull
# do sentiment analysis on replies (idk when best time for this is)
# group replies by tweet they are replying to
# group tweets into categories
# final result: overall sentiment for each category created

# Things to do: grab tags (@) and hashtags in tweets and categorize based on them
# figure out when to do the sentiment analysis
# decide what output should look like

def readTweetJSON(file, d):
    with open(file, "r") as read_file:
        tweets = json.load(read_file)
    for item in tweets["results"]:
        d[item["id"]] = item["text"]
        # print (item["text"])
        # print(item["reply_count"])
    return

def readReplyJSON(file, d):
    with open(file, "r") as read_file:
        tweets = json.load(read_file)
    for item in tweets["results"]:
        id = item["in_reply_to_status_id"]
        if id not in d:
            d[id] = []
        d[id].append(item["text"])
    return

def next(file):
    with open(file, "r") as read_file:
        tweets = json.load(read_file)
    return tweets["next"]

def numReplies(file):
    num = 0
    count = 0
    with open(file, "r") as read_file:
        tweets = json.load(read_file)
    for item in tweets["results"]:
        num += item["reply_count"]
        count += 1
    return num, count

def makeCategories(tweetDict):
    d = dict()
    for tweet in tweetDict:
        text = tweetDict[tweet].split(" ")
        for word in text:
            if "@" in word or "#" in word:
                userOrHashtag = cleanUpText(word)
                if userOrHashtag not in d:
                    d[userOrHashtag] = []
                d[userOrHashtag].append(tweet)
    return d

def combineCategories(catDict, cat1, cat2, newTitle):
    list1 = catDict[cat1]
    list2 = catDict[cat2]
    newList = []
    for tweet in list1:
        if tweet not in newList:
            newList.append(tweet)
    for tweet in list2:
        if tweet not in newList:
            newList.append(tweet)
    del catDict[cat1]
    del catDict[cat2]
    catDict[newTitle] = newList

def cleanUpText(txt):
    txt = re.sub(r'@', '', str(txt))
    txt = re.sub(r'#', '', str(txt))
    txt = re.sub(r'\.', '', str(txt))
    regrex_pattern = re.compile(pattern="["
                                        u"\U0001F600-\U0001F64F"  # emoticons
                                        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                        u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                        "]+", flags=re.UNICODE)
    txt = regrex_pattern.sub(r'', txt)

    # txt = txt.strip('\n')
    txt = txt.strip()
    return txt

if __name__ == "__main__":
    # dict of tweet ID to tweet text
    tweetDict = dict()
    folder = "rockets"
    team = "rockets"           # FILL IN
    numFiles = 3       # FILL IN
    for i in range(numFiles):
        file = folder + "/" + team + str(i) + ".json"
        readTweetJSON(file, tweetDict)
        # print (numReplies(file))

    # print (tweetDict)
    categoriesDict = makeCategories(tweetDict)

    combineCategories(categoriesDict, "TissotStyleWatch", "TISSOT", "Tissot_Promotional")
    combineCategories(categoriesDict, "DonJulio", "TitosVodka", "Alcohol_Promotional")
    combineCategories(categoriesDict, "ChickfilA", "PizzaHut", "Food_Promotional")
    combineCategories(categoriesDict, "Food_Promotional", "Alcohol_Promotional", "Promotional")
    combineCategories(categoriesDict, "Tissot_Promotional", "Promotional", "Promotional")

    combineCategories(categoriesDict, "HoustonDynamo", "HoustonFCU", "Other_Houston_Sports")
    combineCategories(categoriesDict, "SportsTalk790", "ChronTXSN", "Media_Partners")

    for cat in categoriesDict:
        print(cat)
        print (len(categoriesDict[cat]))

    # dict of tweet ID to list of reply text
    replyDict = dict()
    numFiles = 0       # FILL IN
    for i in range(numFiles):
        file = folder + "/" + team + "_r" + str(i) + ".json"
        readReplyJSON(file, replyDict)

    print(replyDict)

    # need 3640 replies for 250 tweets for warriors
    # need 1769 replies for 250 tweets for mavs
    # need 3313 replies for 250 tweets for rockets

    # Code used to get next token for each json file
    # i = 33
    # file = folder + "/" + team + str(i) + ".json"
    # file = folder + "/" + team + "_r" + str(i) + ".json"
    # print (next(file))
