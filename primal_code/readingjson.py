import requests
import json

url = "https://www.reddit.com/r/talesfromtechsupport.json"
r = requests.get(
    url, headers={'User-agent': 'GameGodS3'}, allow_redirects=True)

with open('talesfromtechsupport.json', 'wb') as f:
    f.write(r.content)

with open('talesfromtechsupport.json', 'r') as f:
    l = json.load(f)

storycount = len(l["data"]["children"])

with open('story.md', 'w') as f:
    for i in range(1, storycount):

        if i != 1:
            f.write("\n\n")
        f.write("## " + str(i) + ". " + l["data"]
                ["children"][i]["data"]["title"]+"\n\n")
        f.write(l["data"]["children"][i]["data"]["selftext"])


# print(l["data"]["children"][1]["data"]["title"])
# print(l["data"]["children"][1]["data"]["selftext"])
