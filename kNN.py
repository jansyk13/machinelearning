#!/usr/bin/env python
from numpy import *
import operator

def create_data_set():
    group = array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    labels = ['A','A','B','B']
    return group, labels

def classify(inX, data, labels, k):
    dataSize = data.shape[0]
    diffMat = tile(inX, (dataSize,1)) - data
    sqDiffMat = diffMat**2
    sqDistance = sqDiffMat.sum(axis=1)
    distances = sqDistance**0.5
    sortedDistIndicies = distances.argsort()
    classCount = {}
    for i in range(k):
         voteIlabel = labels[sortedDistIndicies[i]]
         classCount[voteIlabel] = classCount.get(voteIlabel, 0) + 1
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]

data, labels = create_data_set()
result = classify([0,0], data, labels, 3)
print result
