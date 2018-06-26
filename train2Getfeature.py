from nltk.corpus import PlaintextCorpusReader as PCR
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from nltk import FreqDist
import math

rootPath = "D:/course/nltk/IRFinalProject/"
tarTrain = "2017TAR/training/"
trainDoc = "docs.training.tar/docs.training/topics_raw_docs/"
reArticleTitle = re.compile("<ArticleTitle>(.*?)</ArticleTitle>")
lemmatizaer = WordNetLemmatizer()
porter_stemmer = PorterStemmer()
stopWord = list(set(stopwords.words('english')))

class T2F:
    def pre(self,root,paperlength,avglength):
        filelist = PCR(root,".*")
        index={}
        for eachFile in filelist.fileids():
            # print(eachFile)
            with open(root + "/" + eachFile,"r",encoding="UTF-8") as f:
                articleTitle = reArticleTitle.findall(f.read().strip())
                try:
                    # if articleTitle[0].startswith('['):
                    #     articleTitle = articleTitle[0][1:-2]
                    # else:
                    #     articleTitle = articleTitle[0][:-1]
                    preArticleTitle = [porter_stemmer.stem(lemmatizaer.lemmatize(word)) \
                                       for word in word_tokenize(articleTitle[0]) \
                                       if word not in stopWord and word.isalnum()]
                    paperlength[eachFile] = len(preArticleTitle)
                    # print(preArticleTitle)
                    fDist = FreqDist(preArticleTitle)
                    for eachWord in preArticleTitle:
                        if eachWord in index.keys():
                            docnoDist = index[eachWord]
                            docnoDist[eachFile] = fDist[eachWord]
                        else:
                            docnoDist = {}
                            docnoDist[eachFile] = fDist[eachWord]
                            index[eachWord] = docnoDist
                except:
                    pass
        # sortKey = sorted(index.items())
        # print(type(sortKey))
        # with open(root+'/index', "w", encoding="UTF-8") as f:
        #     for item in sortKey:
        #         f.write(item[0] + ": ")
        #         f.write(str(item[1]) + "\n")
        for each in paperlength.keys():
            avglength += paperlength[each]
        avglength = avglength/len(paperlength)
        return index,len(filelist.fileids()),paperlength,avglength

    def TFIDF(self,preTitle,index,cnt):
        res = {}
        for each in preTitle:
            temp = index[each]
            idf = math.log10(cnt / len(temp))
            for eachPaper in temp.keys():
                tf = temp[eachPaper]
                if eachPaper in res.keys():
                    res[eachPaper] += tf*idf
                else:
                    res[eachPaper] = tf*idf
        return res

    def BM25(self,preTitle,index,cnt,paperlength,avglength):
        res = {}
        for each in preTitle:
            temp = index[each]
            idf = math.log10(cnt/len(temp))
            for eachPaper in temp.keys():
                tf = temp[eachPaper]
                score = 0.25 + 0.75 * paperlength[eachPaper]/avglength
                score = tf + 1.5 * score
                score = tf * 2.5 /score
                score = idf * score
                if eachPaper in res.keys():
                    res[eachPaper] += score
                else:
                    res[eachPaper] = score
        return res

    def train2features(self, train_data=rootPath + tarTrain + "qrels/qrel_abs_train", ways=["TFIDF"]):
        with open(train_data, "r", encoding="UTF-8") as ftrain:
            topictemp = ""
            resTFIDF = {}
            resBM25 = {}
            cnt = 0
            preTitle = []
            for line in ftrain:
                templine = line.strip().split()
                topic = templine[0]
                file = templine[2]
                corr = templine[3]
                if topictemp != topic:
                    paperlength = {}
                    avglength = 0
                    topic_path = rootPath + tarTrain + "extracted_data/" + topic + ".title"
                    with open(topic_path, "r", encoding="UTF-8") as ftopic:
                        title = ftopic.read().strip(topic)
                        preTitle = [porter_stemmer.stem(lemmatizaer.lemmatize(word)) \
                                    for word in word_tokenize(title) \
                                    if word not in stopWord and word.isalnum()]
                        index,cnt,paperlength,avglength = self.pre(rootPath + trainDoc + topic,paperlength,avglength)
                        topictemp = topic

                    for way in ways:
                        if way == "TFIDF":
                            resTFIDF = self.TFIDF(preTitle,index,cnt)
                        if way == "BM25":
                            resBM25 = self.BM25(preTitle,index,cnt,paperlength,avglength)
                # print(topic,file,end=" ")
                # try:
                #     print(resTFIDF[file],end=" ")
                # except:
                #     print(0)
                # try:
                #     print(resBM25[file],end=" ")
                # except:
                #     print(0)




                # index_path = rootPath + trainDoc + topic + "index"
                # with open(index_path,"r",encoding="UTF-8") as findex:
                #     for line in findex:
                #         key, value = line.strip().split(":", maxsplit=1)
                #         if key in preTitle:
                #             valueDic = ast.literal_eval(value.strip())








if __name__ == "__main__":
    t2f = T2F()
    # t2f.pre(rootPath + trainDoc + "CD007394")
    t2f.train2features(ways=["TFIDF","BM25"])
