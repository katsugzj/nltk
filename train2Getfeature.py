from nltk.corpus import PlaintextCorpusReader as PCR
import re
import os
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from nltk import FreqDist
import math
from sklearn.linear_model.logistic import LogisticRegression

rootPath = "D:/course/nltk/IRFinalProject/"
tarTrain = "2017TAR/training/"
tarTest = "2017TAR/testing/"
trainDoc = "docs.training.tar/docs.training/topics_raw_docs/"
testDoc = "docs.tesing.tar/docs.tesing/topics_raw_docs/"
reArticleTitle = re.compile("<ArticleTitle>(.*?)</ArticleTitle>")
lemmatizaer = WordNetLemmatizer()
porter_stemmer = PorterStemmer()
stopWord = list(set(stopwords.words('english')))
clf = LogisticRegression()

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
            try:
                temp = index[each]
            except:
                continue
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
            try:
                temp = index[each]
            except:
                continue
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

    def writeFeature(self,res,file,corr=-1,outfile="trainfeature",topic=None):
        with open(outfile,"a",encoding="UTF-8") as out:
            sep = ","
            for each in res:
                try:
                    print(each[file])
                    out.write(str(each[file])+sep)
                except:
                    print('0')
                    out.write('0'+sep)
            if(corr!=-1):
                out.write(str(corr) + sep + topic + "\n")
            else:
                out.write(str(file) + sep + topic + "\n")



    def train2features(self, train_data=rootPath + tarTrain + "qrels/qrel_abs_train", ways=["TFIDF"]):
        with open(train_data, "r", encoding="UTF-8") as ftrain:
            topictemp = ""
            resTFIDF = {}
            resBM25 = {}
            paperlength = {}
            outfile="trainfeature"
            with open(outfile,"w",encoding="UTF-8"):
                pass
            for line in ftrain:
                templine = line.strip().split()
                topic = templine[0]
                file = templine[2]
                print(file)
                corr = templine[3]
                if topictemp != topic:
                    resTFIDF = {}
                    resBM25 = {}
                    paperlength = {}
                    avglength = 0
                    topic_path = rootPath + tarTrain + "extracted_data/" + topic + ".title"
                    if(os.path.exists(topic_path)and os.path.exists(rootPath+trainDoc+topic+"/"+file)):
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
                    else:
                        continue
                try:
                    length = paperlength[file]
                    res = (resTFIDF, resBM25,paperlength)
                    self.writeFeature(res,file,int(corr),outfile=outfile,topic=topic)
                except:
                    pass

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

    def test2features(self, test_data=rootPath + tarTest + "extracted_data/queries.txt", ways=["TFIDF"]):
        with open(test_data, "r", encoding="UTF-8") as ftest:
            topictemp = ""
            resTFIDF = {}
            resBM25 = {}
            paperlength = {}
            outfile="testfeature"
            with open(outfile,"w",encoding="UTF-8"):
                pass
            for line in ftest:
                templine = line.strip().split()
                topic = templine[0]
                title = line.strip(topic)
                preTitle = [porter_stemmer.stem(lemmatizaer.lemmatize(word)) \
                            for word in word_tokenize(title) \
                            if word not in stopWord and word.isalnum()]
                resTFIDF = {}
                resBM25 = {}
                paperlength = {}
                avglength = 0
                index, cnt, paperlength, avglength = self.pre(rootPath + testDoc + topic, paperlength, avglength)

                for way in ways:
                    if way == "TFIDF":
                        resTFIDF = self.TFIDF(preTitle,index,cnt)
                    if way == "BM25":
                        resBM25 = self.BM25(preTitle,index,cnt,paperlength,avglength)

                topic_path = rootPath + tarTest + "extracted_data/" + topic + ".pids"
                with open(topic_path, "r", encoding="UTF-8") as ftopic:
                    for line in ftopic:
                        file = line.strip().split()[1]
                        print(file)
                        try:
                            length = paperlength[file]
                            res = (resTFIDF, resBM25, paperlength)
                            self.writeFeature(res, file, outfile=outfile, topic=topic)
                        except:
                            pass





    def train(self):
        trainFeatureFile = "trainfeature"
        trainX=[]
        trainY=[]
        topictemp = ""
        doclen = []
        iCnt = -1
        with open(trainFeatureFile,"r",encoding="UTF-8") as tff:
            for line in tff:
                text = line.strip().split(",")
                trainX.append([float(i) for i in text[:3]])
                trainY.append(int(text[3]))
                if topictemp == text[4]:
                    doclen[iCnt]+=1
                else:
                    topictemp = text[4]
                    iCnt += 1
                    doclen.append(1)

        print("append finished")
        ln.train(trainX,trainY,doclen)
        # clf.fit(trainX,trainY)
        print("fit finished")

    def preditct(self):
        testFeatureFile = "testfeature"
        res=[]
        with open(testFeatureFile,"r",encoding="UTF-8") as tff:
            for line in tff:
                text = line.strip().split(",")
                # score = clf.predict_proba([[float(i) for i in text[:3]]])
                score = ln.predict([float(i) for i in text[:3]])
                res.append([text[4],text[3],score])
                # res.append([text[4],text[3],score[0][0]])
                # print(text[3])
        res.sort(key=lambda x:(x[0],x[2]))
        cnt = 1
        temptopic = ""
        # outfile="clf.res"
        outfile="listnet.res"
        with open(outfile,"w",encoding="UTF-8") as result:
            for each in res:
                if temptopic==each[0]:
                    cnt+=1
                else:
                    cnt =1
                    temptopic = each[0]
                result.write(str(each[0])+" katsuzj " + str(each[1]) + " " + str(cnt) + " " + str(each[2]) + " 10152130125_gezhongjie\n")


iter = 8  # 迭代次数
dim = 3  # 特征数
class listnet():
    def __init__(self):
        self.weight = []
    def train(self,trainX,trainY,doclen):
        # doclen=doclen[-5:-4]
        yita = 0.004
        for i in range(dim):
            self.weight.append(1.0)
        for n in range(iter):
            start = 0
            delta = []
            for i in range(len(doclen)):
                length = doclen[i]
                fw = []
                delta = []
                for j in range(length):
                    fw.append(trainY[j])
                    for k in range(dim):
                        fw[j] += self.weight[k] * trainX[start+j][k]
                    fw[j]/=10
                x = []
                y=0.0
                z=[]
                for j in range(dim):
                    x.append(0.0)
                    z.append(0.0)
                for j in range(length):
                    p = 1.0
                    temp = []
                    for k in range(dim):
                        temp.append(0.0)
                        den = 0.0
                        for l in range(length):
                            den += math.exp(fw[l])
                        for l in range(length):
                            p *= math.exp(fw[l] / den)
                        temp[k] += p * trainX[start+j][k]
                        x[k] += temp[k]
                for j in range(length):
                    y+=math.exp(fw[j])
                for j in range(length):
                    temp = []
                    for k in range(dim):
                        temp.append(0.0)
                        temp[k] += math.exp(fw[j]) * trainX[start + j][k]
                        z[k] += temp[k]
                for j in range(dim):
                    delta.append(x[j]+z[j]/y)
                    self.weight[j] -= delta[j]*yita

                start += length
                print(start)
            tag = 0
            for i in range(dim):
                tag += abs(delta[i])
            print("tag:"+str(tag))
            print(self.weight)

    def predict(self,feature):
        score = 0.0
        for i in range(len(self.weight)):
            score += self.weight[i] * feature[i]
        return score





if __name__ == "__main__":
    t2f = T2F()
    ln = listnet()
    # t2f.pre(rootPath + trainDoc + "CD007394")
    # way=["TFIDF","BM25"]
    # t2f.train2features(ways=way)
    # t2f.test2features(ways=way)
    t2f.train()
    t2f.preditct()
