#!/usr/bin/python
#
#
import sqlite3
import time,random
from TrumpBotModule import Files
from TrumpBotModule import SQLTools

conn = sqlite3.connect('TrumpBS.sqlite')
conn.text_factory = lambda x: unicode(x, 'utf-8', 'ignore')
cur = conn.cursor()



f = Files()

Categories = dict()
Categories['POL'] = 'politics.txt'
Categories['FP'] = 'fp.txt'
Categories['TRUMP'] = 'trump.txt'
Categories['misc'] = 'misc.txt'
Categories['RNC'] = 'rnc.txt'


speech = list()

cur.execute('''SELECT * FROM TRUMPBS WHERE category = ? ORDER by RANDOM() LIMIT 1''',('OPENING',))

for row in cur:
  if len(row[1]) > 15:
     speech.append(row[1])

def GenBS():
 
  for category,filename in Categories.items():
    count = random.randrange(1, 3)

    cur.execute('''SELECT * FROM TRUMPBS WHERE category = ? ORDER by RANDOM() limit ? ''',(category,count))
    for row in cur:
      if len(row[1]) > 15:
        if "Continue reading the main story" in row[1]:
          pass
        else:
          #speech.append(category + " " + row[1])
          speech.append(row[1])



# SELECT * FROM TRUMPBS WHERE category = 'FP' ORDER BY RANDOM() LIMIT 4;
GenBS()

print "Content-type: text/html\n\n"
print "<!DOCTYPE html>"
print "<html>"
print "<head><title>TrumpBot V 0.1a0</title></head>"
print "<body>"
print "<div>"


for line in speech:
  
  print "<p>" + line.strip().encode('utf-8') + "</p>"

print "</div>"
print "</body></html>"

conn.close()

