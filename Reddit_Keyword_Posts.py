import praw 
import datetime
from datetime import timedelta
import pytz
from concurrent.futures import ThreadPoolExecutor
import pickle

utc = pytz.utc 

reddit = praw.Reddit(client_id='client id',
                     client_secret='secret',
                     user_agent='user agent')

subreddits = ['MusicInTheMaking', 'WeAreTheMusicMakers']
keywords = ['looking', 'show', 'band', 'demo', 'demos', 'song', 'piece', 'recording', 'album', 'songs', 'check out', 'track', 'listen']
usernames = {}

def process_submission(submission):
    if any(keyword in submission.title.lower() or keyword in submission.selftext.lower() for keyword in keywords):
        username = submission.author.name
        subreddit_name = submission.subreddit.display_name
        created_utc = datetime.datetime.fromtimestamp(submission.created_utc, tz=utc)
        if created_utc > (datetime.datetime.now(utc) - timedelta(days=30)):
            if username not in usernames:
                usernames[username] = {'activity_count': 0, 'subreddits': set()}
            usernames[username]['activity_count'] += 1  # Increment activity count
            usernames[username]['subreddits'].add(subreddit_name)  # Add subreddit to user's subreddits


with ThreadPoolExecutor(max_workers=10) as executor:
    for subreddit_name in subreddits:
        subreddit = reddit.subreddit(subreddit_name)
        for submission in subreddit.new(limit=None):
            executor.submit(process_submission, submission)

# Sort the users by activity count in descending order
sorted_users = sorted(usernames.items(), key=lambda x: x[1]['activity_count'], reverse=True)

# Get the top 300 users
top_300_users = sorted_users[:300]

# Convert the list of tuples back to a dictionary if needed
top_300_users_dict_keyword = dict(top_300_users)

# Save the dictionary to a file
with open('top_300_users_dict_keyword.pkl', 'wb') as f:
    pickle.dump(top_300_users_dict_keyword, f)