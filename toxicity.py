import json 
import requests
import praw

from secrets import perspectiveSecret
from secrets import mySecrets

reddit = praw.Reddit(client_id=mySecrets['client_id'], client_secret=mySecrets['client_secret'], user_agent=mySecrets['user_agent'])

# comments = ['fuck you, bitch', 'you stupid meanie head']

def get_comments(subreddit_name, num_posts):
    comments = []
    subreddit = reddit.subreddit(subreddit_name).new(limit=num_posts)
    for post in subreddit:
        comments.append(post.title)
        for comment in post.comments:
            comments.append(comment.body)
    return comments

def toxicity_percentage(subreddit_name, num_posts):
    comments = get_comments(subreddit_name, num_posts)
    # print(comments)

    n = 0
    sum = 0
    for sample in comments:
        n += 1
        api_key = perspectiveSecret['api_key']
        url = ('https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze' +    
            '?key=' + api_key)
        data_dict = {
            'comment': {'text': sample},
            'languages': ['en'],
            'requestedAttributes': {'TOXICITY': {}}
        }

        response = requests.post(url=url, data=json.dumps(data_dict)) 
        response_dict = json.loads(response.content) 
        print(response_dict)
        score = response_dict['attributeScores']['TOXICITY']['summaryScore']['value']
        sum += score

    print(sum / n)

toxicity_percentage('UCSantaBarbara', 5)