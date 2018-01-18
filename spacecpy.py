'''
Usage:

python spacecpy.py ocroutputfile dictionaryfile

'''
#from methods import *
import time
import sys
import re
curindex=-1


import time
import sys
import re


global NodeCount
global WordCount

# Keep some interesting statistics
NodeCount = 0
WordCount = 0

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def maxlen(s1,s2):
    if s1 is None:
        s1l=0
    else:
        s1l=len(s1)
    if s2 is None:
        s2l=0
    else:
        s2l=len(s2)
    #print "comparing ",s1," ",s2
    if(s1l>s2l):
       return s1l
    else:
       return s2l
# The Trie data structure keeps a set of words, organized with one node for
# each letter. Each node has a branch for each letter that may follow it in the
# set of words.
class TrieNode:
    def __init__(self):
        self.word = None
        self.children = {}

        global NodeCount
        NodeCount += 1

    def insert( self, word ):
        node = self
        for letter in word:
            if letter not in node.children: 
                node.children[letter] = TrieNode()

            node = node.children[letter]

        node.word = word


# The search function returns a list of all words that are less than the given
# maximum distance from the target word
def search( word, maxCost ):
    global curresult
    curresult=['nosuggestions',100,word]
    # build first row
    currentRow = range( len(word) + 1 )
    for kk in range(len(currentRow)):
      currentRow[kk]=currentRow[kk]*delcostm

    results = []

    # recursively search each branch of the trie
    for letter in trie.children:
        searchRecursive( trie.children[letter], letter, word, currentRow, 
            results, maxCost )

    #return results
    return curresult

# This recursive helper is used by the search function above. It assumes that
# the previousRow has been filled in already.
def searchRecursive( node, letter, word, previousRow, results, maxCost ):
    global curresult
    columns = len( word ) + 1
    currentRow = [ previousRow[0] + inscostm ]

    # Build one row for the letter, with a column for each letter in the target
    # word, plus one for the empty string at column 0
    for column in xrange( 1, columns ):

        deleteCost = (currentRow[column-1] + delcostm)
        insertCost = (previousRow[column] + inscostm)
   
        
        if word[column - 1] != letter:
            replaceCost = (previousRow[ column - 1 ] + subcostm)
        else:                
            replaceCost = (previousRow[ column - 1 ])

        currentRow.append( min( insertCost, deleteCost, replaceCost ))

    # if the last entry in the row indicates the optimal cost is less than the
    # maximum cost, and there is a word in this trie node, then add it.
    
    if float(currentRow[-1])/maxlen(node.word,word) <= maxCost and node.word != None:
        if float(currentRow[-1])/maxlen(node.word,word) < curresult[1]:
          #print float(currentRow[-1])/maxlen(node.word,word),"is lesser than",curresult[1]
          curresult=[node.word,float(currentRow[-1])/maxlen(node.word,word),word]
        #results.append( (node.word, float(currentRow[-1])/maxlen(node.word,word),word) )
          
        #print currentRow[-1]/maxlen(node.word,word) 
    # if any entries in the row are less than the maximum cost, then 
    # recursively search each branch of the trie
    if float(min( currentRow ))/maxlen(node.word,word) <= maxCost:
        for letter in node.children:
            searchRecursive( node.children[letter], letter, word, currentRow, 
                results, maxCost )

def ocrOutputSplit(file):
    text = open(file, "rt").read()
    words=re.split(';',text)
    #print words

    fields = []

    for word in words:
        word=word.split(':')
        if len(word)==2:
            del word[0]
        fields.append(word[0])

    #print fields
    bfields = []
    for field in fields:
        bfields.append(field.split());

    bfields.pop()
    return bfields


#have to do .lower and put in methods
       


#Start of execution

FILE = sys.argv[1]
bfields = ocrOutputSplit(FILE)
'''
f2=open("ocroutlec21.py","w")
for field in bfields:
    f2.write(field[0]+"\n")
'''

MAX_COST = 0.3
DICTIONARY = sys.argv[2]

inscostm=1
delcostm=1
subcostm=1

lecnum = FILE.split(".")



list_words=[]
global curresult


# read dictionary file into a trie
trie = TrieNode()
for word in open(DICTIONARY, "rt").read().split():
    WordCount += 1
    trie.insert( word )

print "Read %d words into %d nodes" % (WordCount, NodeCount)


flag=0

fp=open("output.txt","w")
fo=open("sugwords"+lecnum[0]+".txt","w")
start = time.time()
for TARGET in bfields:
        curindex=curindex+1
        #print TARGET
        index=len(TARGET)-2
        string=""
        for kk in range(0,len(TARGET)-2):
           string=string+TARGET[kk]
        if float(TARGET[index])<80:
           results = search( string, MAX_COST )
        else:
           results=[string,0,string]
#	for result in results: 
#           if result[1]==0:
#               flag=1
#        if flag==0:
#              for result in results:
#                   fp.write(str(result)+"\n")
#                   #print str(result)+"\n"    
#        flag=0
#        if results[1]!=0:
        if results[0]=="nosuggestions":
            #print "found"
            #print results[0]
            #print results[2]
            results[0] = results[2]
        fp.write(str(results)+"\n")
        fo.write(results[0]+"\n")
end = time.time()

fp.close()
   
#print "insertcost",inscostm
#print "deletecost",delcostm
#print "subcost",subcostm
print "Search took %g s" % (end - start)


