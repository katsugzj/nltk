import re
import ast
import os
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from nltk.corpus import PlaintextCorpusReader as PCR

corpusRoot =  "D:/course/nltk/disk12pre"
fileList = PCR(corpusRoot,".*")
lenFile = {}

for eachFile in fileList.fileids():
    path = os.path.join("D:/course/nltk/disk12pre", eachFile)
    lenDoc = os.stat(path).st_size
    lenFile[eachFile] = lenDoc

filename = "D:/course/nltk/topics.151-200"
sumDoc = 741724
avgDoc = 2528
sumLen = 1875557977
a = 0.95

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
        with open("D:/course/nltk/result_SLM_part" + str(int(index / 10)), "w", encoding="UTF-8") as resultFile:
            top = index + 10
            while index < top:
                titleNum = lNum[index].strip()
                print(titleNum)
                searchWords = Title[titleNum]
                res = {}
                with open('D:/course/nltk/index', "r", encoding="UTF-8") as f:
                    for line in f:
                        key, value = line.strip().split(":", maxsplit=1)
                        if key in searchWords:
                            #qtf = searchWords.count(key)
                            valueDic = ast.literal_eval(value.strip())
                            cf = 0
                            for eachDoc in valueDic.keys():
                                cf += valueDic[eachDoc]
                            #df = len(valueDic)
                            #idf = math.log10((sumDoc + 0.0) / df)
                            for eachDoc in valueDic.keys():
                                tf = valueDic[eachDoc]
                                score = a*tf/lenFile[eachDoc] + (1-a)*cf/sumLen
                                '''TF_IDF'''
                                #score = tf * idf
                                '''BM25'''
                                #score = bm25(tf,eachDoc)
                                '''VSM-TF_IDF'''
                                #score = vsm_tfidf(tf,qtf,idf,eachDoc)
                                if eachDoc in res.keys():
                                    res[eachDoc] *= score
                                    #res[eachDoc] += (score / weight[key])
                                else:
                                    res[eachDoc] = score
                                    #res[eachDoc] = (score / weight[key])

                rank = sorted(res.items(), key=lambda item: item[1], reverse=True)
                lenR = len(rank)
                if lenR > 100:
                    lenR = 100

                item = 0
                while item < lenR:
                    docNum, score = rank[item]
                    rankList = titleNum + " katsuzj " + docNum + " " + str(item) + " " + str(score) + " " + "10152130125_gezhongjie_SLM\n"
                    resultFile.write(rankList)
                    item += 1

                index += 1
