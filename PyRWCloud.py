import sqlite3

conn = sqlite3.connect('reddit_wordcloud.sqlite')
cur = conn.cursor()
counts = dict()

# Select the top 100 entries in the database
sqlstr = 'SELECT word, count FROM Words ORDER BY count DESC LIMIT 100'

for word in cur.execute(sqlstr):
    counts[str(word[0])]=int(word[1])

# The following code which calculates the font size based on the range
# of values, as well as generates the gword.js file was taken from the 
# gmane section of the PY4E certificate course materials which can be 
# found in whole at https://github.com/csev/py4e/tree/master/code3/gmane
x = sorted(counts, key=counts.get, reverse=True)
highest = None
lowest = None
for k in x[:100]:
    if highest is None or highest < counts[k] :
        highest = counts[k]
    if lowest is None or lowest > counts[k] :
        lowest = counts[k]
print('Range of counts:',highest,lowest)

# Spread the font sizes across 20-120 based on the count
bigsize = 120
smallsize = 20

fhand = open('gword.js','w')
fhand.write("gword = [")
first = True
for k in x[:100]:
    if not first : fhand.write( ",\n")
    first = False
    size = counts[k]
    size = (size - lowest) / float(highest - lowest)
    size = int((size * bigsize) + smallsize)
    fhand.write("{text: '"+k+"', size: "+str(size)+"}")
fhand.write( "\n];\n")
fhand.close()

print("Output written to gword.js")
print("Open gword.htm in a browser to see the visualization")
