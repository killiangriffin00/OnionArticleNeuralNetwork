import matplotlib.pyplot as plt
import numpy as np
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer

#nltk.download('wordnet')
#nltk.download('stopwords')
#nltk.download('omw-1.4')

def importData():
    rawData = []
    input = open("archive/onionOrNot.csv", encoding="UTF-8")
    
    input.readline()
    buffer = input.readline()
    while buffer != "":
        while not (buffer.endswith(",0\n") or  buffer.endswith(",1\n")):
            buffer += input.readline()
        rawData.append(buffer) 
        buffer = input.readline()
    
    dataValueList = []
    debug = 0
    for x in rawData:
        split = x.split(',')
        
        while len(split) > 2:
            combineElement = split[0] + split[1]  
            split.pop(0)
            split.pop(0)
            split.insert(0, combineElement)

        split[0] = split[0].split('|')[0]

        if split[0].lower().find("the onion") != -1:
            continue

        dataValueList.append((re.sub('\n', '', split[0]), int(re.sub('[\W_]', ' ', split[1]).strip())))
    return dataValueList

def cleanData(rawData):
    stop_words = stopwords.words('english')
    wnl = WordNetLemmatizer()
    clean = []
    for value in rawData:
        split = re.sub('[\W_]', ' ', value[0]).strip().lower().split()
        split = [wnl.lemmatize(valword) for valword in split if valword not in stop_words]
        value = (' '.join(split), value[1])
        clean.append(value)
    return clean

def bagOfWords(data):
    cv = CountVectorizer()
    X = cv.fit_transform([x[0] for x in data])
    y = [x[1] for x in data]

    return (cv, X, y)

def getCleanData():
    return cleanData(importData())

def getBag():
    return bagOfWords(getCleanData())

if __name__ == "__main__":
    rawDataset = importData()
    rawDataset = cleanData(rawDataset)
    bag = bagOfWords(rawDataset)
    feature = bag[0].get_feature_names_out()

    with open("archive/cleanedData.csv", "w", encoding="utf-8") as f:
        for text, label in rawDataset:
            f.write(f"{text},{label}\n")

    print(rawDataset)