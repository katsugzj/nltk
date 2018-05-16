import re
import ast
import math
import os
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn

filename = "D:/course/nltk/topics.151-200"
sumDoc = 741724
avgDoc = 1875557977 / 741724

def vsm_tfidf(tf,qtf,idf,eachDoc):
    path = os.path.join("D:/course/nltk/disk12pre", eachDoc)
    lenDoc = os.stat(path).st_size
    temp = tf * idf
    temp2 = qtf * idf
    return temp * temp2 / lenDoc

def bm25(tf,eachDoc):
    path = os.path.join("D:/course/nltk/disk12pre", eachDoc)
    lenDoc = os.stat(path).st_size
    idf = math.log10((sumDoc - df + 0.5) / (df + 0.5))
    temp = 0.25 + 0.75 * lenDoc / avgDoc
    temp = tf + (1.5 * temp)
    temp = tf * 2.5 / temp
    return idf * temp

with open(filename,"r",encoding="UTF-8") as f:

    pNum = re.compile(r"<num> Number:(.*)")
    lNum = pNum.findall(str(f.read()))
    f.seek(0,0)
    pTitle = re.compile(r"<title> Topic:(.*)")
    lTitle = pTitle.findall(str(f.read()))

    index = 0
    lemmatizaer = WordNetLemmatizer()
    porter_stemmer = PorterStemmer()
    stopWord = list(set(stopwords.words('english')))
    Title = {}

    for eachT in lTitle:
        pre = [porter_stemmer.stem(lemmatizaer.lemmatize(word)) for word in word_tokenize(eachT) if word not in stopWord and word.isalnum()]
        Title[lNum[index].strip()] = pre
        index += 1

    index = 0
    while index < 50:
        with open("D:/course/nltk/result_rocchio_part" + str(int(index / 10)), "w", encoding="UTF-8") as resultFile:
            top = index + 10
            while index < top:
                titleNum = lNum[index].strip()
                print(titleNum)
                searchWords = Title[titleNum]
                result = {}
                with open('D:/course/nltk/index', "r", encoding="UTF-8") as f:
                    for line in f:
                        key, value = line.strip().split(":", maxsplit=1)
                        if key in searchWords:
                            qtf = searchWords.count(key)
                            valueDic = ast.literal_eval(value.strip())
                            df = len(valueDic)
                            idf = math.log10((sumDoc + 0.0) / df)
                            if key not in result.keys():
                                result[key] = qtf * idf
                            for eachDoc in valueDic.keys():
                                tf = valueDic[eachDoc]
                                score = vsm_tfidf(tf,qtf,idf,eachDoc)
                                with open('D:/course/nltk/qrels_for_disk12/qrels.151-200.disk1.disk2.part' + str(int(index / 10) + 1), "r", encoding="UTF-8")as rnr:
                                    for line in rnr:
                                        temp = line.strip().split(' ')
                                        if titleNum > temp[0]:
                                            break
                                        else:
                                            if eachDoc == temp[2]:
                                                if temp[3] == 1:
                                                    result[key] += (0.75 * score)
                                                else:
                                                    result[key] -= (0.25 * score)
                res = {}
                with open('D:/course/nltk/index', "r", encoding="UTF-8") as f:
                    for line in f:
                        key, value = line.strip().split(":", maxsplit=1)
                        if key in searchWords:
                            qtf = searchWords.count(key) * result[key]
                            valueDic = ast.literal_eval(value.strip())
                            df = len(valueDic)
                            idf = math.log10((sumDoc + 0.0) / df)

                            for eachDoc in valueDic.keys():
                                tf = valueDic[eachDoc]

                                '''TF_IDF'''
                                #score = tfidf(tf,idf)

                                '''BM25'''
                                #score = bm25(tf,eachDoc)

                                '''VSM-TF_IDF'''
                                #score = vsm_tfidf(tf,qtf,idf,eachDoc)

                                if eachDoc in res.keys():
                                    res[eachDoc] += score
                                else:
                                    res[eachDoc] = score

                rank = sorted(res.items(), key=lambda item: item[1], reverse=True)
                lenR = len(rank)
                if lenR > 100:
                    lenR = 100

                item = 0
                while item < lenR:
                    docNum, score = rank[item]
                    rankList = titleNum + " katsuzj " + docNum + " " + str(item) + " " + str(score) + " " + "vsm-qrel\n"
                    resultFile.write(rankList)
                    item += 1

                index += 1
