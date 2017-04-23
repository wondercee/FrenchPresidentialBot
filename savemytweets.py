#!/usr/bin/env python
# encoding: utf-8
# Credit to Yanofsky: https://gist.github.com/yanofsky/5436496

import tweepy
import csv

# Twitter API credentials
consumer_key="njF45n6yKYXnRbbPsDFDgC4k6"
consumer_secret="w2Nhw0ZokrE5fIsWwk5EjHdbJV6RSh9qrm0CXTQB3IIBXq1aNk"
access_key="844581311000035328-rrJrvXbnFzQ8eOMiK7ZP7KlBJugs3Hn"
access_secret="Xj6BciI7N5MAWCECj4IdOn1RNVKeuce8qdZwJKZSh2Wsq"

# Twitter only allows access to 3240 most recent tweets - will have to run script every week.
def get_all_tweets(screen_name):

# Authorize twitter and initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)

# Initialize a list to hold all the tweepy Tweets
	alltweets = []

# Fetch most recent tweets (200 is the maximum allowed)
	new_tweets = api.user_timeline(screen_name = screen_name,count=200)

# Save them
	alltweets.extend(new_tweets)

# Save the ID of oldest tweet less one
	oldest = alltweets[-1].id - 1

# Keep fetching tweets until there are no more left
	while len(new_tweets) > 0:
		print "getting tweets before %s" % (oldest)

# Let's prevent duplicates (with max)
		new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)

# Save most recent tweets
		alltweets.extend(new_tweets)

# Update the ID of oldest tweet less one
		oldest = alltweets[-1].id - 1

		print "...%s tweets downloaded so far" % (len(alltweets))

# Transform the tweepy tweets into a 2D array for the csv file
	outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]

# Create csv file to store tweets
	with open('%s_tweets.csv' % screen_name, 'wb') as f:
		writer = csv.writer(f)
		writer.writerow(["id","created_at","text"])
		writer.writerows(outtweets)

	pass


if __name__ == '__main__':
# Account we want to download the tweets from
	get_all_tweets("Republique2017")
