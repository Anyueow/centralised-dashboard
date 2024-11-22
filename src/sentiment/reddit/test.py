import praw
from constants import CLIENT_ID, CLIENT_SECRET, USER_AGENT

# Initialize the Reddit instance without user authentication
reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent=USER_AGENT
)

# Access the 'movies' subreddit
subreddit = reddit.subreddit('movies')

# Get the top post right now from 'hot' posts
top_post = next(subreddit.hot(limit=1))

print("Top post in r/movies right now:")
print(f"Title: {top_post.title}")
print(f"Score: {top_post.score}")
print(f"URL: {top_post.url}")
print(f"Comments: {top_post.num_comments}")
print(f"Permalink: https://reddit.com{top_post.permalink}")
