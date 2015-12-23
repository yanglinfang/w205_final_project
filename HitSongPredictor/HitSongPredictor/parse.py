from __future__ import absolute_import, print_function, unicode_literals

import re
from streamparse.bolt import Bolt
import psycopg2

################################################################################
# Function to check if the string contains only ascii chars
################################################################################
def ascii_string(s):
  return all(ord(c) < 128 for c in s)

class ParseTweet(Bolt):

    def initialize(self, conf, ctx):
        self.conn = psycopg2.connect(database="postgres", user="postgres", password="pass", host="localhost", port="5432")

    def process(self, tup):
        tweet = tup.values[0]  # extract the tweet
        # Split the tweet into words
        words = tweet.split()

        # Filter out the hash tags, RT, @ and urls
        valid_words = []
        for word in words:

            # Filter the hash tags
            if word.startswith("#"): continue

            # Filter the user mentions
            if word.startswith("@"): continue

            # Filter out retweet tags
            if word.startswith("RT"): continue

            # Filter out the urls
            if word.startswith("http"): continue

            # Strip leading and lagging punctuations
            aword = word.strip("\"?><,'.:;)")

            # now check if the word contains only ascii
            if len(aword) > 0 and ascii_string(word):
                valid_words.append([aword])

        if not valid_words: return

        valid_titles = []
        cur = self.conn.cursor()
        
        processed_tweet = " ".join(["%s" % (v) for v in valid_words])
        cur.execute("SELECT title FROM Songs_tweet WHERE position(title in %s) > 0;",[processed_tweet]);
        records = cur.fetchall()
        if len(records) > 0:
            self.log('found %s records in tweet_count table where the title is in the tweet text.' % (len(records)))
            for rec in records:
                uTitle = rec[0]
                valid_titles.append([uTitle])
                self.log('song title mentioned in tweet is:%s' % (uTitle))


        if not valid_titles: return

        # Emit all the words
        self.emit_many(valid_titles)

        # tuple acknowledgement is handled automatically
