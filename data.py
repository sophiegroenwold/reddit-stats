from secrets import mySecrets

import praw
import pandas as pd
from datetime import datetime

subreddit_name = 'UCSantaBarbara'

reddit = praw.Reddit(client_id=mySecrets['client_id'], client_secret=mySecrets['client_secret'], user_agent=mySecrets['user_agent'])

def name(subreddit_name):
    subreddit = reddit.subreddit(subreddit_name)
    return subreddit.display_name

def description(subreddit_name):
    subreddit = reddit.subreddit(subreddit_name)
    return subreddit.public_description

def num_subscribers(subreddit_name):
    subreddit = reddit.subreddit(subreddit_name)
    return subreddit.subscribers

def time_created(subreddit_name):
    subreddit = reddit.subreddit(subreddit_name)
    parsed_date = datetime.utcfromtimestamp(subreddit.created_utc)
    year = parsed_date.year
    month = parsed_date.month
    day = parsed_date.day
    return str(month) + '.' + str(day) + '.' + str(year)

def hot(subreddit_name):
    subreddit = reddit.subreddit(subreddit_name).hot(limit=3)

    # make dataframe with data
    hot_df = pd.DataFrame(columns = ['title', 'url'])
    for post in subreddit:
        hot_df = hot_df.append({
            'title': post.title,
            'url': 'https://www.reddit.com' + post.permalink
        }, ignore_index=True)

    return hot_df

def new(subreddit_name):
    subreddit = reddit.subreddit(subreddit_name).new(limit=3)

    # make dataframe with data
    new_df = pd.DataFrame(columns = ['title', 'url'])
    for post in subreddit:
        new_df = new_df.append({
            'title': post.title,
            'url': 'https://www.reddit.com' + post.permalink
        }, ignore_index=True)

    return new_df

def top_users(subreddit_name, time_filter):
    print(subreddit_name)
    subreddit = reddit.subreddit(subreddit_name).top(time_filter = time_filter)

    user_dict = {}
    for post in subreddit:

        # add score for author
        if post.author != None:
            if post.author.name in user_dict:
                user_dict[post.author.name] += 1
            else:
                user_dict[post.author.name] = 1

        # add score for each commentor
        for comment in post.comments:
            if comment.author != None:
                if comment.author.name in user_dict:
                    user_dict[comment.author.name] += 1
                else:
                    user_dict[comment.author.name] = 1

    # sort so that top users are first
    user_list = sorted(user_dict, key=user_dict.__getitem__, reverse=True)

    # make dataframe with data
    user_df = pd.DataFrame(columns = ['place', 'username'])
    i = 1
    for user in user_list:
        if i < 6:
            user_df = user_df.append({
                'place': i,
                'username': user_list[i - 1]
            }, ignore_index=True)
        else:
            break
        i += 1

    return user_df

top_users('UCSantaBarbara', 'day')








