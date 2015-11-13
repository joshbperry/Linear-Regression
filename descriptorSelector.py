__author__ = 'haotian'

import numpy as np
import matplotlib.pyplot as plt
from __builtin__ import file
from sklearn.linear_model.base import LinearRegression
import dataProcess as ds
import linearRegression as lr
import random
import dataProcess as dp

'''
run forward selection with cross validation rms error
'''
def forwardSelectionWithCV(title, data, trails, dscCount, outputFile):

    outFile = open(outputFile,'w')

    result_tuples = []

    randomInputFileList = []

    for i in range(0,trails):
        random.shuffle(data)
        newList = list(data)
        randomInputFileList.append(newList)


    for i in range(0, len(title)-1):
        allErr = lr.crossValidation([i],randomInputFileList)
        err = sum(allErr)/len(allErr)
        result = (title[i],err)
        result_tuples.append(result)

    result_tuples = sorted(result_tuples, key = lambda x:x[-1])

    #todo: output result to OutFile

    for i in range(1, dscCount):
        bestResult = result_tuples[0]
        resultDsc = bestResult[:-1]
        dscIndex = [title.index(x) for x in resultDsc]
        result_tuples = []
        for j in range(0,len(title)-1):
            if j not in dscIndex:
                newIndex = list(dscIndex)
                newIndex.append(j)
                allErr = lr.crossValidation(newIndex, randomInputFileList)
                err = sum(allErr)/len(allErr)

                dscText = [title[x] for x in newIndex]
                dscText = tuple(dscText)
                result = dscText +(err,)
                result_tuples.append(result)

        result_tuples = sorted(result_tuples, key = lambda x:x[-1])

    #todo: output result to OutFile

    return result_tuples[0]

'''
    run forward selection with whole data set rms error
'''
def forwardSelectionWithWholeSet(title, data, dscCount, outputFile):

    outFile = open(outputFile,'w')

    result_tuples = []

    inputFileList = data


    for i in range(0, len(title)-1):
        err = lr.wholeSetPrediction([i],inputFileList)
        result = (title[i],err)
        result_tuples.append(result)

    result_tuples = sorted(result_tuples, key = lambda x:x[-1])

    #todo: output result to OutFile

    for i in range(1, dscCount):
        bestResult = result_tuples[0]
        resultDsc = bestResult[:-1]
        dscIndex = [title.index(x) for x in resultDsc]
        result_tuples = []
        for j in range(0,len(title)-1):
            if j not in dscIndex:
                newIndex = list(dscIndex)
                newIndex.append(j)
                err = lr.wholeSetPrediction(newIndex, inputFileList)

                dscText = [title[x] for x in newIndex]
                dscText = tuple(dscText)
                result = dscText +(err,)
                result_tuples.append(result)

        result_tuples = sorted(result_tuples, key = lambda x:x[-1])

    #todo: output result to OutFile

    return result_tuples[0]


def backwardEliminationWithWholeSet(descripter, title, data, outputFile):

    descripterIndex = [title.index(x) for x in descripter]
    print descripterIndex
    result = []

    indexLeft = list(descripterIndex)

    while len(indexLeft) > 1:
        smallestErr = 1000
        for item in indexLeft:
            copyList = list(indexLeft)
            copyList.remove(item)

            err = lr.wholeSetPrediction(copyList, data)

            if err < smallestErr:
                smallestErr = err
                worstIndex = item
        worst = title[worstIndex]
        result.append(worst)
        indexLeft.remove(worstIndex)

    result.append(title[indexLeft[0]])
    result.reverse()
    return result

def backwardEliminationWithCV(descripter, title, data, trails, outputFile):

    descripterIndex = [title.index(x) for x in descripter]
    print descripterIndex
    result = []

    indexLeft = list(descripterIndex)

    randomInputFileList = []

    for i in range(0,trails):
        random.shuffle(data)
        newList = list(data)
        randomInputFileList.append(newList)

    while len(indexLeft) > 1:
        smallestErr = 1000
        for item in indexLeft:
            copyList = list(indexLeft)
            copyList.remove(item)

            err = lr.crossValidation(copyList, randomInputFileList)
            err = sum(err)/len(err)
            if err < smallestErr:
                smallestErr = err
                worstIndex = item
        worst = title[worstIndex]
        result.append(worst)
        indexLeft.remove(worstIndex)

    result.append(title[indexLeft[0]])
    result.reverse()
    return result


if __name__ == '__main__':
    title, data = dp.parseInput('Data/DS4-DSC8.txt')
    forwardSelectionWithWholeSet(title, data, 10, 'abc')
    des = forwardSelectionWithCV(title, data, 1000, 20, 'abc')
    des = des[:-1]
    des2 = backwardEliminationWithCV(des,title,data,1000, 'abc')

    print des
    print des2
