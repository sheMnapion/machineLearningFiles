#!/usr/bin/env python

from numpy import *
import operator
import matplotlib.pyplot as plt
from time import ctime
from os import listdir

def createDataSet():
    group=array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    labels=['A','A','B','B']
    return group,labels

def classify0(inX,dataSet,labels,k):
    '''
        classifies the k nearest neighbours
        inX: the input vector for classify
    '''
    dataSetSize=shape(dataSet)[0]
    diffMat=tile(inX,(dataSetSize,1))-dataSet#for calculating the difference between points
    sqDiffMat=diffMat**2
    distances=sqrt(sqDiffMat.sum(axis=1))
    #print distances
    sortedDistIndices=distances.argsort()
    classCount={}
    for i in range(k):
        voteILabel=labels[sortedDistIndices[i]]
        classCount[voteILabel]=classCount.get(voteILabel,0)+1
    classCount=sorted(classCount.iteritems(),key=operator.itemgetter(1),reverse=True)
    return classCount[0][0]

def file2matrix(filename):
    'Open file filename as input matrix'
    f=open(filename)
    lines=f.readlines()
    f.close()
    lineNumber=len(lines)
    dataMat=[]
    labels=[]
    for line in lines:
        line=line.strip().split('\t')
        for i,ele in enumerate(line):
            line[i]=float(line[i])
        dataMat.append(line[0:3])
        labels.append(int(line[-1]))
    return dataMat,labels

def primitivePlot(data,labels,index1=0,index2=1):
    'print index1 line and index2 line for data'
    data=array(data)
    fig=plt.figure()
    ax=fig.add_subplot(111)
    plt.xlabel('%d'%index1)
    plt.ylabel('%d'%index2)
    ax.scatter(data[:,index1],data[:,index2],15.0*array(labels),15.0*array(labels))
    plt.show()

def autoNorm(dataSet):
    'Normalize dataset into range [0,1]'
    dataSet=array(dataSet)
    minVals=dataSet.min(0)
    maxVals=dataSet.max(0)
    ranges=maxVals-minVals
    normDataSet=zeros(shape(dataSet))
    m=dataSet.shape[0]
    normDataSet=dataSet-tile(minVals,(m,1))
    normDataSet=dataSet/tile(ranges,(m,1))
    return normDataSet,ranges,minVals

def datingClassTest():
    'A test on present dating data'
    hoRatio=0.30
    datingDataMat,datingLabels=file2matrix('../datingTestSet2.txt')
    normMat,ranges,minVals=autoNorm(datingDataMat)
    m=normMat.shape[0]
    numTestVecs=int(m*hoRatio)
    errorCount=0.0
    for i in range(numTestVecs):
        #print numTestVecs,i,m
        classifierResult=classify0(normMat[i,:],normMat[numTestVecs:m,:],datingLabels[numTestVecs:m],3)
        print "Classifier came back with %d while the true one is %d" % (classifierResult,datingLabels[i])
        if classifierResult!=datingLabels[i]:
            errorCount+=1.0
    print "Total error rate: %.2f" % (errorCount/float(numTestVecs))

def classifyPerson():
    'Classify a person as given above'
    resultList=['not at all','in small doses','in large doses']
    percentTats=float(raw_input("Percentage of time spent playing video games?"))
    ffMiles=float(raw_input("Frequent flier mile earned per year?"))
    iceCream=float(raw_input("Liters of ice cream consumed per year?"))
    datingDataMat,datingLabels=file2matrix('../datingTestSet2.txt')
    normMat,ranges,minVals=autoNorm(datingDataMat)
    inArr=array([ffMiles,percentTats,iceCream])
    classifierResult=classify0((inArr-minVals)/ranges,normMat,datingLabels,3)
    print "You will probably like this person: ", resultList[classifierResult-1]

def img2vector(filename):
    'Change the file filename into image'
    returnVector=zeros((1,1024))
    f=open(filename)
    lines=f.readlines()
    f.close()
    for i,line in enumerate(lines):
        line=line.strip()
        for j in range(32):
            returnVector[0,32*i+j]=int(line[j])
    return returnVector

def handwritingClassTest():
    hwLabels=[]
    trainingFileList=listdir('../trainingDigits')
    m=len(trainingFileList)
    trainingMat=zeros((m,1024))
    for i in range(m):
        fileNameStr=trainingFileList[i]
        fileStr=fileNameStr.split('.')[0]
        classNumStr=int(fileStr.split('_')[0])
        hwLabels.append(classNumStr)
        trainingMat[i,:]=img2vector('../trainingDigits/%s'%fileNameStr)
    testFileList=listdir('../testDigits')
    errorCount=0.0
    mTest=len(testFileList)
    begin=ctime()
    for i in range(mTest):
        fileNameStr=testFileList[i]
        fileStr=fileNameStr.split('.')[0]
        classNumStr=int(fileStr.split('_')[0])
        testVector=img2vector('../testDigits/%s'%fileNameStr)
        k=random.randint(3,4)
        classifierResult=classify0(testVector,trainingMat,hwLabels,k)
        #print "The classifier came back with %d while the real one is %d" %(classifierResult,classNumStr)
        if (classifierResult!=classNumStr):
            errorCount+=1
    end=ctime()
    print "Total error:%d" % errorCount
    print "Total error rate: %.3lf" % (errorCount/float(mTest))
    print begin
    print end
#data,labels=file2matrix('../datingTestSet2.txt')
#print mat(data),labels
#normData,ranges,minVals=autoNorm(data)
#print normData, ranges,minVals
#primitivePlot(normData,labels,index1=1,index2=2)
#datingClassTest()
#classifyPerson()
handwritingClassTest()
#print classify0([0,0],data,labels,3)
