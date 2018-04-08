from nltk.corpus import PlaintextCorpusReader as PCR
from nltk import FreqDist

root = 'D:/nltk/disk12pre'
wordLists = PCR(root,'.*')
index = {}
for fileId in wordLists.fileids():
    print(fileId)
    word = wordLists.words(fileId)
    fDist = FreqDist(word)
    for item in fDist.keys():
        if item in index.keys():
            docnoDist = index[item]
            docnoDist[fileId] = fDist[item]
        else:
            docnoDist = {}
            docnoDist[fileId] = fDist[item]
            index[item] = docnoDist
sortKey = sorted(index.items())
with open('index',"w",encoding="UTF-8") as f:
    for item in sortKey:
        f.write(item[0] + ": ")
        f.write(str(item[1]) + "\n")