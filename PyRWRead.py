'''Utilizes Python to pull reddit history from JSON into a SQL database'''
import json
import sqlite3

LineCount = 0
conn = sqlite3.connect('reddit_wordcloud.sqlite')
cur = conn.cursor()

Question = input("Do you wish to append to the database? (Y/N)")
if Question == "Y" or Question == "y":
    AppendToTable = True
else:
    AppendToTable = False
 
if AppendToTable == False:
    cur.executescript('DROP TABLE IF EXISTS Words; CREATE TABLE Words (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, word TEXT UNIQUE, count  INTEGER);')

fname = input('Open which file? ')
if len(fname) < 1:
    fname = 'reddit_comment_sample.json'
try:
    f = open(fname, encoding="utf8")
except:
    print("Error opening file:", fname)
    quit()

while True:
    try:
        json_data = json.loads(f.readline())
    except:
        break
    LineCount += 1
    # JSON to Select selftext:""
    comment = json_data["selftext"]
    if comment is None or comment == "[deleted]" or comment == "[removed]":
        continue
    print(LineCount, comment[:50])

    SplitComment = comment.split()
    
    for word in SplitComment:
        cur.execute(
            'SELECT count FROM Words WHERE word = ? ', (word.lower(),))
        row = cur.fetchone()
        if row is None:
            cur.execute('INSERT OR IGNORE INTO Words (word, count) VALUES (?, 1)', (word.lower(),))
        else:
            cur.execute('UPDATE Words SET count = count + 1 WHERE word = ?', (word.lower(),))
    if LineCount % 100 == 0:
        conn.commit()
    

# Display top 100 at end
sqlstr = 'SELECT word, count FROM Words ORDER BY count DESC LIMIT 100'

for row in cur.execute(sqlstr):
    print(str(row[0]), row[1])

conn.commit()