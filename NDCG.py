import math


class DCG():
    def __init__(self):
        self.qrel ={}
        self.res = []

    def get_qrel(self):
        with open(r"C:\Users\葛钟杰\Downloads\10152130120苏和通IRFinalProject\qrel_abs_test")as f:
            for line in f:
                text = line.strip().split()
                query = text[0]
                paper = text[2]
                corr = text[3]
                if query in self.qrel.keys():
                    temp = self.qrel[query]
                    temp[paper] = corr
                else:
                    temp = {}
                    temp[paper] = corr
                    self.qrel[query]=temp

    def get_res(self):
        with open("clf.res","r",encoding="UTF-8") as f:
            tempquery = ""
            rank=1
            cnt=-1
            score = []
            for line in f:
                text = line.strip().split()
                query = text[0]
                paper = text[2]
                if(tempquery==query):
                    rank+=1
                else:
                    rank=1
                    cnt+=1
                    score.append(0)
                if(self.qrel[query][paper]):
                    score[cnt]+=3/math.log(1+rank)
            temp=0
            for i in range(len(score)):
                temp += score[i]
            temp/=len(score)
            print(temp)

dcg= DCG()
dcg.get_qrel()
dcg.get_res()