# encoding: utf-8

import tweepy
import time

# Authentication
consumer_key="mPfu2lmfwbVnS8JCzCLhJKGwQ"
consumer_secret="MbSLQQmZDukRUoYe48mrW0i3ZfF23mccqOnH2Saxa1BtJn0M8d"
access_token="844581311000035328-dCEi5eKIsmcukTP8qAYeml3QzPkMiGY"
access_token_secret="4qLK9NhMV9uLvMRsNOLiFUUEI2HHOKjJQLvtRD0HjUZxh"

# Connection to Twitter STREAM API
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# Group candidates into a class
class Candidate:
    """ Each candidate is represented by their name
            And their Twitter ID.
    """
# Define attributes
    def __init__(self, twitter_id, first_name, last_name):
        self.id = twitter_id
        self.first_name = first_name
        self.last_name = last_name
        self.last_tweet = 1                 # Request tweets with a higher id than the last one fetched.

# Common errors I need to avoid
ERRORS_TWEEPY = {
    327 :   u'You have already retweeted this tweet.',
    88  :   u'Rate limit exceeded',
    185 :   u'User is over daily status update limit.'
    }

# Candidates to the French election + information mentioned in lines 23-26
CANDIDATES = [
    Candidate('38170599',   'Nicolas',  'Dupont-Aignan'),
    Candidate('200659061',  'Francois', 'Asselineau'),
    Candidate('551669623',  'Francois', 'Fillon'),
    Candidate('374392774',  'Philippe', 'Poutou'),
    Candidate('150201042',  'Jacques',  'Cheminade'),
    Candidate('1976143068', 'Emmanuel', 'Macron'),
    Candidate('1003575248', 'Nathalie', 'Arthaud'),
    Candidate('217749896',  'Marine',   'Le Pen'),
    Candidate('14389177',   'Benoit',   'Hamon'),
    Candidate('102722347',  'Jean',     'Lassalle'),
    Candidate('80820758',   'Jean-Luc', 'Melenchon'),
    ]

# Loop - so the code goes on indefinitely
while True:

# Fetching tweets for each candidate (one by one)
        for candidate in CANDIDATES:
            print('Examining {0} {1}...'.format(candidate.first_name, candidate.last_name))

# Fetch tweets that have not yet been retweeted (using last_tweet).
            for tweet in api.user_timeline(candidate.id, since_id=candidate.last_tweet):

# Fetching a maximum amount of tweets now to avoid fetching as many/the same tweets next time
                candidate.last_tweet = max(candidate.last_tweet, tweet.id)

# If we've already retweeted the tweet, let's ignore it
                if tweet.retweeted:
                    print('Tweet {0} is a retweet and will be avoided (It has been retweeted {1} times !).'.format(tweet.id, tweet.retweet_count))
                    continue

# But if we haven't, let's retweet it
                try:
                    api.retweet(tweet.id)
                    print ('Retweet ! : {0}'.format(tweet.text.encode('utf-8')))

# If there's a Tweepy error (listed in lines 30-33, or not), print message in Terminal to let me know
                except tweepy.TweepError as e:
                    print(e.message)

# Update me on what is happening in my Terminal
            print('Candidate retweeted. Moving on to the next one.')
        print('All candidates have been retweeted for now. Will check again later.')

# To avoid spamming and being blocked by Twitter API
        time.sleep(900)

# Even if an error occurs (other than tweepy.TweepError), keep going - the code must never break!
    except Exception as uncaught_error:
        print('Unexpected exception, but the show must go on.')
