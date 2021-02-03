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

def fake_value():
    return str(0.5)

def toxicity_percentage(subreddit_name, num_posts):
    comments = get_comments(subreddit_name, num_posts)
    # print(comments)

    n = 0
    tox_sum = 0
    profanity_sum = 0
    insult_sum = 0
    for sample in comments:
        n += 1
        api_key = perspectiveSecret['api_key']
        url = ('https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze' +    
            '?key=' + api_key)
        data_dict = {
            'comment': {'text': sample},
            'languages': ['en'],
            'requestedAttributes': {'TOXICITY': {}, 'PROFANITY': {}, 'INSULT': {}}
        }

        response = requests.post(url=url, data=json.dumps(data_dict)) 
        response_dict = json.loads(response.content) 
        # print(response_dict)

        tox_score = response_dict['attributeScores']['TOXICITY']['summaryScore']['value']
        profanity_score = response_dict['attributeScores']['PROFANITY']['summaryScore']['value']
        insult_score = response_dict['attributeScores']['INSULT']['summaryScore']['value']

        tox_sum += tox_score
        profanity_sum += profanity_score
        insult_sum += insult_score
        
    return [str(tox_sum / n), str(profanity_sum / n), str(insult_sum / n)]

# print(toxicity_percentage('UCSantaBarbara', 1))