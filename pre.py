import re
import os
import gzip
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer

sourceFile = ("D:/nltk/disk12/disk1/AP/AP890101.gz", "D:/nltk/disk12/disk1/FR/FR890103.gz", "D:/nltk/disk12/disk1/WSJ/WSJ7_001.gz", "D:/nltk/disk12/disk1/ZIFF/ZF_001.gz")
for eachFile in sourceFile:
    with gzip.open(eachFile,"r") as f:
        pDoc = re.compile(r"<DOC>([\s\S]*?)</DOC>")
        lDoc = pDoc.findall(str(f.read(),encoding="UTF-8"))
        f.seek(0,0)
        pDocno = re.compile(r"<DOCNO>(.*?)</DOCNO>")
        lDocno = pDocno.findall(str(f.read(),encoding="UTF-8"))

        Text = []
        pText = re.compile("<TEXT>([\s\S]*?)</TEXT>")
        for eachDoc in lDoc:
            Text.append(pText.findall(eachDoc))

        index = 0
        lemmatizaer = WordNetLemmatizer()
        porter_stemmer = PorterStemmer()
        stopWord = list(set(stopwords.words('english')))

        for lText in Text:
            if not os.path.exists(eachFile[:-3] + 'pre'):
                os.makedirs(eachFile[:-3] + 'pre')
            outFile = eachFile[:-3] + 'pre/' + lDocno[index].strip()
            with open(outFile,"w",encoding="UTF-8") as f:
                f.write("<DOC>\n")
                f.write("<DOCNO>%s<DOCNO>\n" % lDocno[index])
                f.write("<TEXT>\n")
                for eachT in lText:
                    pre = [porter_stemmer.stem(lemmatizaer.lemmatize(word)) for word in word_tokenize(eachT) if word not in stopWord and word.isalnum()]

                    for word in pre:
                        f.write(word+" ")
                f.write("\n</TEXT>\n")
                f.write("</DOC>\n")
            index+=1