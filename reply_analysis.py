import json

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

if __name__ == "__main__":
    # dict of tweet ID to tweet text
    tweetDict = dict()
    folder = "warriors"
    team = "warriors"           # FILL IN
    numFiles = 4        # FILL IN
    for i in range(numFiles):
        file = folder + "/" + team + str(i) + ".json"
        # readTweetJSON(file, tweetDict)
        print (numReplies(file))

    print (tweetDict)

    # dict of tweet ID to list of reply text
    replyDict = dict()
    numFiles = 2        # FILL IN
    for i in range(numFiles):
        file = folder + "/" + team + "_r" + str(i) + ".json"
        # readReplyJSON(file, replyDict)

    print(replyDict)
    # need 3640 replies for 250 tweets
    i = 37
    file = folder + "/" + team + "_r" + str(i) + ".json"
    print (next(file))
