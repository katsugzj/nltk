import re
import os
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer

sourceFile = ("AP890101", "FR890103", "WSJ7_001", "ZF_001")
for eachFile in sourceFile:
    with open(eachFile,"r",encoding="UTF-8") as f:
        pDoc = re.compile(r"<DOC>([\s\S]*?)</DOC>")
        lDoc = pDoc.findall(f.read())
        f.seek(0,0)
        pDocno = re.compile(r"<DOCNO>(.*?)</DOCNO>")
        lDocno = pDocno.findall(f.read())

        Text = []
        pText = re.compile("<TEXT>([\s\S]*?)</TEXT>")
        for eachDoc in lDoc:
            Text.append(pText.findall(eachDoc))

        index = 0
        lemmatizaer = WordNetLemmatizer()
        porter_stemmer = PorterStemmer()
        enPun = [',', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%','``','\'\'','\'','...','_','<','>','-','--','..']
        stopWord = list(set(stopwords.words('english')))+enPun

        for lText in Text:
            if not os.path.exists(eachFile + 'pre'):
                os.makedirs(eachFile + 'pre')
            outFile = eachFile + 'pre/' + lDocno[index].strip()
            with open(outFile,"w",encoding="UTF-8") as f:
                f.write("<DOC>\n")
                f.write("<DOCNO>%s<DOCNO>\n" % lDocno[index])
                f.write("<TEXT>\n")
                for eachT in lText:
                    pre = [porter_stemmer.stem(lemmatizaer.lemmatize(word)) for word in word_tokenize(eachT) if word not in stopWord]

                    for word in pre:
                        f.write(word+" ")
                f.write("\n</TEXT>\n")
                f.write("</DOC>\n")
            index+=1