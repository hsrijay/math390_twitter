import json
import re


# Adds Tweets from the given JSON to a dictionary mapping Tweet ID to text of Tweet
def readTweetJSON(file, d):
    with open(file, "r") as read_file:
        tweets = json.load(read_file)
    for item in tweets["results"]:
        d[item["id"]] = item["text"]
    return

# Same purpose as above function, but code differed slightly for files of Tweet Replies
def readReplyJSON(file, d):
    with open(file, "r") as read_file:
        tweets = json.load(read_file)
    for item in tweets["results"]:
        id = item["in_reply_to_status_id"]
        if id not in d:
            d[id] = []
        d[id].append(item["text"])
    return

# Due to Twitter only allowing us to grab 100 tweets at a time and using pagination to determine the
# next group of tweets, I used this code to get the "next" token in the JSON file I just pulled,
# and then added that "next" token to my next API call
def next(file):
    with open(file, "r") as read_file:
        tweets = json.load(read_file)
    return tweets["next"]

# Returned a tuple of the total amount of Replies the Tweets in a given file had,
# and the total number of Tweets in the file
# Used to determine roughly number of Replies to grab for each team, found the following:
# need 3640 replies for 250 tweets for warriors
# need 1769 replies for 250 tweets for mavs
# need 3313 replies for 250 tweets for rockets
def numReplies(file):
    num = 0
    count = 0
    with open(file, "r") as read_file:
        tweets = json.load(read_file)
    for item in tweets["results"]:
        num += item["reply_count"]
        count += 1
    return num, count

# Takes in dictionary of Tweet ID to Tweet text
# Returns new dictionary of "categories" (hashtags or mentions) mapped to list of Tweet IDs that
# contained that hashtag or mention
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

# Modified given dictionary by combing two given categories into one new combined category
# "newTitle" is the name given for the new combined category
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

# Used to remove "@", "#", ".", emojis, and extra whitespace from Tweets
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

# code to create single dictionary of Tweets for a given team
def makeTweetDict(teamName, numFiles):
    tweetDict = dict()
    for i in range(numFiles):
        file = teamName + "/" + teamName + str(i) + ".json"
        readTweetJSON(file, tweetDict)
    return tweetDict

# Similarly, code to create single dictionary of Tweet replies for a given team
def makeReplyDict(teamName, numFiles):
    replyDict = dict()
    for i in range(numFiles):
        file = teamName + "/" + teamName + "_r" + str(i) + ".json"
        readReplyJSON(file, tweetDict)
    return replyDict

if __name__ == "__main__":

    # dict of tweet ID to tweet text
    tweetDict = dict("warriors", 4)
    # tweetDict = dict("rockets", 3)
    # tweetDict = dict("mavs", 3)

    # dict of tweet ID to list of reply text
    replyDict = makeReplyDict("warriors", 38)
    # replyDict = makeReplyDict("rockets", 34)
    # replyDict = makeReplyDict("mavs", 18)

    # dict of a category (hashtag or mention) to list of Tweet IDs in that category
    categoriesDict = makeCategories(tweetDict)

    # Below are the manual combinations I did to take related terms and condense them into a single category

    # Rockets Combinations
    # combineCategories(categoriesDict, "TissotStyleWatch", "TISSOT", "Tissot_Promotional")
    # combineCategories(categoriesDict, "DonJulio", "TitosVodka", "Alcohol_Promotional")
    # combineCategories(categoriesDict, "ChickfilA", "PizzaHut", "Food_Promotional")
    # combineCategories(categoriesDict, "Food_Promotional", "Alcohol_Promotional", "Promotional")
    # combineCategories(categoriesDict, "Tissot_Promotional", "Promotional", "Promotional")
    #
    # combineCategories(categoriesDict, "HoustonDynamo", "HoustonFCU", "Other_Houston_Sports")
    # combineCategories(categoriesDict, "SportsTalk790", "ChronTXSN", "Media_Partners")

    # Mavs Combinations
    # combineCategories(categoriesDict, "Chime", "ChoctawCasinos", "Promotional")
    # combineCategories(categoriesDict, "Lexus", "Promotional", "Promotional")
    # combineCategories(categoriesDict, "BEDGEAR:", "Promotional", "Promotional")
    # combineCategories(categoriesDict, "SleepFuels", "Promotional", "Promotional")
    # combineCategories(categoriesDict, "BEDGEAR", "Promotional", "Promotional")
    # combineCategories(categoriesDict, "Biofreeze", "Promotional", "Promotional")
    # combineCategories(categoriesDict, "modelousa", "Promotional", "Promotional")
    # combineCategories(categoriesDict, "fcbrewing", "Promotional", "Promotional")
    # combineCategories(categoriesDict, "SomosMavs:", "Promotional", "Promotional")
    #
    # combineCategories(categoriesDict, "DallasStars:", "GoStars", "Other_Dallas_Sports")
    # combineCategories(categoriesDict, "FOXSportsSW", "1033fmESPN", "Media_Partners")

    # Warriors Combinations
    # combineCategories(categoriesDict, "CarMax", "googlecloud", "Promotional")
    # combineCategories(categoriesDict, "Verizon", "Promotional", "Promotional")
    # combineCategories(categoriesDict, "StateFarm:", "Promotional", "Promotional")
    # combineCategories(categoriesDict, "Kia", "Promotional", "Promotional")
    # combineCategories(categoriesDict, "budweiserusa", "Promotional", "Promotional")
    # combineCategories(categoriesDict, "PlayStation", "Promotional", "Promotional")
    # combineCategories(categoriesDict, "verizon", "Promotional", "Promotional")
    # combineCategories(categoriesDict, "Rakuten", "Promotional", "Promotional")
    # combineCategories(categoriesDict, "Xfinity:", "Promotional", "Promotional")
    # combineCategories(categoriesDict, "Viber", "Promotional", "Promotional")
    # combineCategories(categoriesDict, "Rakuten", "Promotional", "Promotional")
    # combineCategories(categoriesDict, "Xfinity:", "Promotional", "Promotional")
    #
    # combineCategories(categoriesDict, "StanfordWBB:", "StanfordWBB", "Other_SF_Sports")
    # combineCategories(categoriesDict, "CalWBBall:", "Other_SF_Sports", "Other_SF_Sports")
    # combineCategories(categoriesDict, "GoBears", "Other_SF_Sports", "Other_SF_Sports")
    # combineCategories(categoriesDict, "NBCSAuthentic", "957thegame", "Media_Partners")
    # combineCategories(categoriesDict, "nbcsauthentic", "Media_Partners", "Media_Partners")

    # Code used to get next token for each json file
    # i = 33
    # file = folder + "/" + team + str(i) + ".json"
    # file = folder + "/" + team + "_r" + str(i) + ".json"
    # print (next(file))
