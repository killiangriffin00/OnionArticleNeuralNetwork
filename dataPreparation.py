import matplotlib.pyplot as plt
import numpy as np

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
    
    dataValueList = [()]
    debug = 0
    for x in rawData:
        split = x.split(',')
        
        while len(split) > 2:
            combineElement = split[0] + split[1]  
            split.pop(0)
            split.pop(0)
            split.insert(0, combineElement)
        dataValueList.append((split[0], split[1].strip("\n\",\'")))
    return dataValueList

if __name__ == "__main__":
    rawDataset = importData()
    print(rawDataset)