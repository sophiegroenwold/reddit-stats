import os 
from dotenv import load_dotenv

import praw
from praw.models import MoreComments

import pandas as pd
from datetime import datetime

load_dotenv()
mySecrets_client_id = os.getenv('mySecrets_client_id')
mySecrets_client_secret = os.getenv('mySecrets_client_secret')
mySecrets_user_agent = os.getenv('mySecrets_user_agent')

reddit = praw.Reddit(client_id=mySecrets_client_id, client_secret=mySecrets_client_secret, user_agent=mySecrets_user_agent)

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
        title = post.title
        if len(title) > 56:
            title = title[:56] + '...'
        hot_df = hot_df.append({
            'title': title,
            'url': 'https://www.reddit.com' + post.permalink
        }, ignore_index=True)

    return hot_df

def new(subreddit_name):
    subreddit = reddit.subreddit(subreddit_name).new(limit=3)

    # make dataframe with data
    new_df = pd.DataFrame(columns = ['title', 'url'])
    for post in subreddit:
        title = post.title
        if len(title) > 56:
            title = title[:56] + '...'
        new_df = new_df.append({
            'title': title,
            'url': 'https://www.reddit.com' + post.permalink
        }, ignore_index=True)

    return new_df

def top_users(subreddit_name, time_filter):
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
        post.comments.replace_more(limit=0) # removes instances of MoreComments objs
        for comment in post.comments:
            # if isinstance(comment, MoreComments):
            #     print('hit MoreComments')
            #     continue
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








