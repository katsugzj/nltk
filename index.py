import re
import os
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

stopWord = list(set(stopwords.words('english')))

def fIndex(path):

    fileList = [eachFile for eachFile in os.listdir(path)]

    index = {}

    for eachFile in fileList:
        with open(os.path.join(path, eachFile),"r",encoding="UTF-8") as f:
