'''Utilizes Python to pull reddit history from JSON into a SQL database'''
import json
import sqlite3
import string

LineCount = 0
conn = sqlite3.connect('reddit_wordcloud.sqlite')
cur = conn.cursor()

# Do you want to append the new file into the database?
# Theoretically you could then input multiple files.
Question = input("Do you wish to append to the database? (Y/N)")
if Question == "Y" or Question == "y":
    AppendToTable = True
else:
    AppendToTable = False
 
if AppendToTable == False:
    cur.executescript('DROP TABLE IF EXISTS Words; CREATE TABLE Words (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, word TEXT UNIQUE, count  INTEGER);')

FileName = input('Open which file? ')
if len(FileName) < 1:
    FileName = 'reddit_comment_sample.json'
try:
    FileHandle = open(FileName, encoding="utf8")
except:
    print("Error opening file:", FileName)
    quit()

while True:
    # Commit every 100 comments, makes more sense to do it before the potential break
    if LineCount % 100 == 0:
        conn.commit()

    try:
        json_data = json.loads(FileHandle.readline())
    except:
        conn.commit()
        break

    LineCount += 1
    
    # JSON to Select selftext:""
    RawComment = json_data["selftext"]

    # Remove whitepace surrounding & punctuation
    translator = str.maketrans('', '', string.punctuation)
    comment = RawComment.translate(translator)
    comment = comment.strip()

    # Skip empty, removed, or deleted comments
    if comment is None or comment == "" or comment == "[deleted]" or comment == "[removed]" or comment == "deleted" or comment == "removed":
        continue

    # Keep track
    print(LineCount, comment[:50])

    # Divide comments into words, add new words, increase count for previously added words
    SplitComment = comment.split()
    
    for word in SplitComment:
        cur.execute(
            'SELECT count FROM Words WHERE word = ? ', (word.lower(),))
        row = cur.fetchone()
        if row is None:
            cur.execute('INSERT OR IGNORE INTO Words (word, count) VALUES (?, 1)', (word.lower(),))
        else:
            cur.execute('UPDATE Words SET count = count + 1 WHERE word = ?', (word.lower(),))

# If we reached the end through a break success, let us know
print("End reached through a successful failure to read another line")
conn.commit()