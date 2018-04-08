import re
import os
import gzip
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from nltk.corpus import PlaintextCorpusReader as PCR


corpusRoot =  ('D:/nltk/disk12')
fileList = PCR(corpusRoot,".*")
print(fileList.fileids())
for eachFile in fileList.fileids():
    with gzip.open(corpusRoot + '/' + eachFile ,"r") as f:
        pDoc = re.compile(r"<DOC>([\s\S]*?)</DOC>")
        lDoc = pDoc.findall(str(f.read(),encoding="UTF-8"))
        f.seek(0,0)
        pDocno = re.compile(r"<DOCNO>([\s\S]*?)</DOCNO>")
        lDocno = pDocno.findall(str(f.read(),encoding="UTF-8"))
        Text = []
        pText = re.compile(r"<TEXT>([\s\S]*?)</TEXT>")
        for eachDoc in lDoc:
            Text.append(pText.findall(eachDoc))
        index = 0
        lemmatizaer = WordNetLemmatizer()
        porter_stemmer = PorterStemmer()
        stopWord = list(set(stopwords.words('english')))
        for lText in Text:
            if not os.path.exists('D:/nltk/disk12' + 'pre'):
                os.makedirs('D:/nltk/disk12' + 'pre')
            outFile = 'D:/nltk/disk12' + 'pre/' + lDocno[index].strip()
            print(outFile)
            with open(outFile,"w",encoding="UTF-8") as f:
                for eachT in lText:
                    pre = [porter_stemmer.stem(lemmatizaer.lemmatize(word)) for word in word_tokenize(eachT) if word not in stopWord and word.isalnum()]
                    for word in pre:
                        f.write(word+" ")
            index+=1