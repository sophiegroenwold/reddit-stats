import praw
from secrets import mySecrets

import pandas as pd

reddit = praw.Reddit(client_id=mySecrets['client_id'], client_secret=mySecrets['client_secret'], user_agent=mySecrets['user_agent'])

def hot():
    subreddit = reddit.subreddit('UCSantaBarbara').hot(limit=5)

    # make dataframe with data
    hot_df = pd.DataFrame(columns = ['title', 'url'])
    for post in subreddit:
        hot_df = hot_df.append({
            'title': post.title,
            'url': 'https://www.reddit.com' + post.permalink
        }, ignore_index=True)

    return hot_df



