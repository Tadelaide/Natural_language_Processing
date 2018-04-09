#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""\
------------------------------------------------------------
USE: python <PROGNAME>  train.txt test.txt
OPTIONS:
    -h : print this help message
    
Created on Thu Feb 15 2018

@author: wlt
------------------------------------------------------------\
"""
import sys, getopt, re, nltk, timeit, random
from collections import Counter
from sklearn.metrics import f1_score

class CommandLine:
    def __init__(self):
        opts, args = getopt.getopt(sys.argv[1:],'h')
        self.args = args
        #print(args)
        #This is to ensure the load file is two txt file
        txtCheck = re.compile('[\S]+\.txt')
        
        if '-h' in opts:
            self.printHelp()
        
        #To ensure the number of the file
        if not len(args) == 2:
            print("*** ERROR: need two file : a trainData file and a queryData file - ! ***", file=sys.stderr)
            self.printHelp()
        
        #To ensure the type of the file
        for item in args:
            if not (re.match(txtCheck,item)):
                print("*** ERROR: the correct file format is : trainData.txt and queryData.txt - ! ***", file=sys.stderr)
                self.printHelp()  
    
    #Print the Help information
    def printHelp(self):
        help = __doc__.replace('<PROGNAME>',sys.argv[0],1)
        print(help, file=sys.stderr)
        sys.exit()

#Open the training file & the query file
class openfile:
    def __init__(self,file):
        self.file = file
        self.train = self.openFile(file[0])
        self.test = self.openFile(file[1])

    #Open the train file
    def openFile(self, file):
        Word_Label_List = []
        with open(file,'r') as infile:
            for line in infile:
                wordList = line.split()
                length = len(wordList)//2
                tempList = []
                for i in range(length):                    
                    newWord_Lable = Word_Label(wordList[i],wordList[i+length])
                    if i > 0:
                        newWord_Lable.previous = tempList[i-1]
                    tempList.append(newWord_Lable)
                for j in range(len(tempList)-1):
                    tempList[j].next = tempList[j+1]
                Word_Label_List.extend(tempList)
        return Word_Label_List


class Word_Label:
    def __init__(self, word, label):
        self.word = word
        self.label = label
        self.previous = None
        self.next = None 

class Binary_perceptron:
    def __init__(self, train, test, multipalTime):
        random.seed(2)
        self.RRule = random.random()
        self.multipalTime = multipalTime
        self.train = train
        self.test = test
        self.weight = {}#weight = {'word':{'O':1,'PER':2,...,'MISC':2},}
        self.trainProcess()
        self.testProcess()
        
    def trainProcess(self):
        for i in range(self.multipalTime):
            trainData = self.train
            random.shuffle(trainData, lambda: self.RRule)
            for item in trainData:
                if not self.predict(item) == item.label:
                    self.update(item)
        
    def predict(self, node):
        if node.word in self.weight.keys():
            return sorted(self.weight[node.word],key = lambda i : self.weight[node.word][i], reverse = True)[0]
        else:
            return 'O'

    def update(self, node):
        labelList = {'O': 0, 'PER': 0, 'LOC': 0, 'ORG': 0, 'MISC': 0}
        if node.word in self.weight.keys():
            self.weight[node.word][node.label] += 1/self.multipalTime
        else:
            labelList[node.label] += 1/self.multipalTime
            self.weight[node.word] = labelList

    def testProcess(self):
        correct = []
        predicted = []
        for item in self.test:
            correct.append(item.label)
            predicted.append(self.predict(item))
        f1_micro = f1_score(correct, predicted, average='micro', labels=['ORG', 'MISC', 'PER', 'LOC'])
        print('----------------------------------------')
        print('current word-current label \nfi_micro is:',f1_micro)
        print('----------------------------------------')
        self.top10()
        print('----------------------------------------')

    def top10(self):
        ORGList = [item for item in sorted(self.weight, key = lambda i : self.weight[i]['ORG'],reverse=True)[:10]]
        print('The List of ORG top 10 is :',ORGList)
        MISCList = [item for item in sorted(self.weight, key = lambda i : self.weight[i]['MISC'],reverse=True)[:10]]
        print('The List of MISC top 10 is :',MISCList)
        PERList = [item for item in sorted(self.weight, key = lambda i : self.weight[i]['PER'],reverse=True)[:10]]
        print('The List of PER top 10 is :',PERList)
        LOCList = [item for item in sorted(self.weight, key = lambda i : self.weight[i]['LOC'],reverse=True)[:10]]
        print('The List of LOC top 10 is :',LOCList,)


if __name__ == '__main__': 
    start = timeit.default_timer()
    config = CommandLine()
    #print(config.args)
    openFile = openfile(config.args)
    multipalTime = 10
    bigram = Binary_perceptron(openFile.train, openFile.test, multipalTime)
    elapsed = timeit.default_timer() - start
    print('The program take',elapsed,'seconds to complete.')