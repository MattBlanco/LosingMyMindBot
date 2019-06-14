import praw
import os

def bot_login():
    print ("Logging in..")
    try:
        r = praw.Reddit(username = os.environ["REDDIT_USERNAME"],
                password = os.environ["REDDIT_PASSWORD"],
                client_id = os.environ["CLIENT_ID"],
                client_secret = os.environ["CLIENT_SECRET"],
                user_agent = "kyle")
        print ("Logged in!")
    except:
        print ("Failed to log in!")
    return r