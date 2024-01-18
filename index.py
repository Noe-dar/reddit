from os import getenv
from dotenv import load_dotenv
import praw
import matplotlib.pyplot as plt
from collections import Counter

load_dotenv()

reddit = praw.Reddit(
    client_id=getenv("CLIENT_ID"), 
    client_secret=getenv("CLIENT_SECRET"),
    user_agent="Jesus Christ"
)

def get_words(reddit, sub_reddit):
    words = {}

    for submission in reddit.subreddit(sub_reddit).hot(limit=5):
        submission.comments.replace_more(limit=0)

        for comment in submission.comments:
            for word in comment.body.split():
                word = word.lower()
                if not word.isalpha():
                    continue

                if words.get(word) == None:
                    words[word] = 1
                else:
                    words[word] += 1
    
    return words

def render_pie(words):
    words = dict(Counter(words).most_common(15))
    explode = map(lambda i: 0.2 if i[0] == 0 else 0, enumerate(words.values()))
    plt.pie(words.values(), explode=list(explode), labels=list(map(lambda key: f"{key} ({words[key]})", words.keys())))

    plt.axis("equal")
    plt.savefig("result.png")

words = get_words(reddit, "eesti")
render_pie(words)