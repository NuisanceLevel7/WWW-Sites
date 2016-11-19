#!/usr/bin/python
#
#
import sqlite3
import time,random,operator

conn = sqlite3.connect('TrumpBS.sqlite')
conn.text_factory = lambda x: unicode(x, 'utf-8', 'ignore')
cur = conn.cursor()



wordcounter = dict()

cur.execute('''SELECT * FROM TRUMPBS ''',)
punctuation = '. , ! ? ; : '
for row in cur:
  if len(row[1]) > 15:
     words = row[1].split()
     for word in words:
       strippedword = ''
       for c in word:
         if c not in punctuation:
           strippedword += c.lower()
       if len(strippedword) > 1:
         wordcounter[strippedword] = wordcounter.get(strippedword, 0) + 1

wordlist = wordcounter.keys()
total = len(wordlist)
print "Total number of unique words: ",total
words = sorted(wordcounter.items(), key=operator.itemgetter(1),reverse=True)
for pairs in words:
  print pairs[0], pairs[1]

conn.close()

