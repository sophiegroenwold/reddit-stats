import os 
from dotenv import load_dotenv

import json 
import requests
import praw

load_dotenv()
mySecrets_client_id = os.getenv('mySecrets_client_id')
mySecrets_client_secret = os.getenv('mySecrets_client_secret')
mySecrets_user_agent = os.getenv('mySecrets_user_agent')
perspectiveSecret = os.getenv('perspectiveSecret')

reddit = praw.Reddit(client_id=mySecrets_client_id, client_secret=mySecrets_client_secret, user_agent=mySecrets_user_agent)

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
    identity_sum = 0
    threat_sum = 0
    sexually_exp_sum = 0
    for sample in comments:
        n += 1
        api_key = perspectiveSecret
        url = ('https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze' +    
            '?key=' + api_key)
        data_dict = {
            'comment': {'text': sample},
            'languages': ['en'],
            'requestedAttributes': {'TOXICITY': {}, 'PROFANITY': {}, 'INSULT': {}, 'IDENTITY_ATTACK': {}, 'THREAT': {}, 'SEXUALLY_EXPLICIT': {}}
        }

        response = requests.post(url=url, data=json.dumps(data_dict)) 
        response_dict = json.loads(response.content) 
        # print(response_dict)

        # retrieve requested attributes
        tox_score = response_dict['attributeScores']['TOXICITY']['summaryScore']['value']
        profanity_score = response_dict['attributeScores']['PROFANITY']['summaryScore']['value']
        insult_score = response_dict['attributeScores']['INSULT']['summaryScore']['value']
        identity_score = response_dict['attributeScores']['IDENTITY_ATTACK']['summaryScore']['value']
        threat_score = response_dict['attributeScores']['THREAT']['summaryScore']['value']
        sexually_exp_score = response_dict['attributeScores']['SEXUALLY_EXPLICIT']['summaryScore']['value']

        tox_sum += tox_score
        profanity_sum += profanity_score
        insult_sum += insult_score
        identity_sum += identity_score
        threat_sum += threat_score
        sexually_exp_sum += sexually_exp_score
        
    return [str(tox_sum / n), str(profanity_sum / n), str(insult_sum / n), str(identity_sum / n), str(threat_sum / n), str(sexually_exp_sum / n)]

# print(toxicity_percentage('UCSantaBarbara', 1))