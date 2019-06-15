import praw
import time
import os

previous_id="0"

def bot_login():
    print ("Logging in..")
    try:
        r = praw.Reddit(username = os.environ["REDDIT_USERNAME"],
                password = os.environ["REDDIT_PASSWORD"],
                client_id = os.environ["CLIENT_ID"],
                client_secret = os.environ["CLIENT_SECRET"],
                user_agent = "LSM Bot")
        print ("Logged in!")
    except:
        print ("Failed to log in!")
    return r
        
def run_bot(bot):
    print ("\nFetching comments..")
    try:
        # Grab all the Recent Comments in every subreddit. This will return 100 of the newest comments on Reddit
        for results in bot.subreddit('all').comments():
            global previous_id  # Import the global variable

            body = results.body  # Grab the Comment
            body = body.lower() # Convert the comment to lowercase so we can search it no matter how it was written
            comment_id = results.id  # Get the Comment ID

            if comment_id == previous_id:  # Check if we already replied to this comment
                return "Error"

            found = body.find('loosing')  # Search for loosing.

            if found != -1:
                previous_id = comment_id  # Add to our global variable

                try:
                    # Reply to the Comment
                    print ("\n\nFound a comment with loosing!")
                    comment_reply = "Noticed you used *loosing*. Did you mean **losing?**"
                    comment_reply += "\n\n\n\n---\n\n^(Beep boop. I am a bot. If there are any issues, contact my) [^master ](https://www.reddit.com/message/compose/?to=PositivePlayer1&subject=/u/LosingMyMindBot)\n\n"
                    results.reply(comment_reply)
                except Exception as e:
                    # Probably low karma so can't comment as frequently
                    time_remaining = 15
                    if (str(e).split()[0] == "RATELIMIT:"):
                        for i in str(e).split():
                            if (i.isdigit()):
                                time_remaining = int(i)
                                break
                        if (not "seconds" or not "second" in str(e).split()):
                            time_remaining *= 60
                    print (str(e.__class__.__name__) + ": " + str(e))
                    for i in range(time_remaining, 0, -5):
                        print ("Retrying in", i, "seconds..")
                        time.sleep(5)	
                    break
    except Exception as e:
        print (str(e.__class__.__name__) + ": " + str(e))

if __name__ == "__main__":
    while True:
        try:
            reddit_bot = bot_login()
            run_bot(reddit_bot)
            time.sleep(10)

        except Exception as e:
            print (str(e.__class__.__name__) + ": " + str(e))
            time.sleep(15)
