from __future__ import absolute_import, print_function, unicode_literals

from collections import Counter
from streamparse.bolt import Bolt

import psycopg2

class WordCounter(Bolt):

    def initialize(self, conf, ctx):
        self.counts = Counter()
        self.conn = psycopg2.connect(database="postgres", user="postgres", password="pass", host="localhost", port="5432")


    def process(self, tup):
        word = tup.values[0]

        # Write codes to increment the word count in Postgres
        # Use psycopg to interact with Postgres
        # Database name: postgres 
        # Table name: Tweetwordcount 
        # you need to create both the database and the table in advance.
        cur = self.conn.cursor()

        uWord = word
        uCount = self.counts[word] + 1

        cur.execute("SELECT word, count from Tweetwordcount WHERE word=%s",[uWord]);
        records = cur.fetchall()
        #update or insert
        if len(records) > 0:
            self.log('found %s records, before update:' % (len(records)))
            for rec in records:
                self.log('word = %s' % (rec[0]))
                self.log('count = %s' % (rec[1]))
            cur.execute("UPDATE Tweetwordcount SET count=%s WHERE word=%s", (uCount + rec[1], uWord));
            self.conn.commit()
        else:
            self.log('record does not exist, try insert')
            cur.execute("INSERT INTO Tweetwordcount (word,count) VALUES (%s, %s)", (uWord, uCount));
            self.conn.commit()
			
        #Select
        cur.execute("SELECT word, count from Tweetwordcount WHERE word=%s",[uWord]);
        records = cur.fetchall()
        self.log('found %s records, after update:' % (len(records)))
        for rec in records:
            self.log('word = %s' % (rec[0]))
            self.log('count = %s' % (rec[1]))
        

        # Increment the local count
        self.counts[word] += 1
        self.emit([word, self.counts[word]])

        # Log the count - just to see the topology running
        self.log('%s: %d' % (word, self.counts[word]))
		
		
