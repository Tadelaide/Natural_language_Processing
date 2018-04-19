#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""\
------------------------------------------------------------
USE: python <PROGNAME>  train.txt test.txt
OPTIONS:
    -h : print this help message
    
Created on Thu Apr 15 2018

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
                    newWord_Lable = Word_Label()
                    newWord_Lable.word = wordList[i]
                    newWord_Lable.label = wordList[i+length]
                    if i > 0:
                        newWord_Lable.previous = tempList[i-1]
                    else :
                        newWord_Lable.previous = Word_Label()
                        newWord_Lable.previous.label = 'start'
                    tempList.append(newWord_Lable)
                for j in range(len(tempList)-1):
                    tempList[j].next = tempList[j+1]
                tempList[-1].next = Word_Label()
                tempList[-1].next.label = 'end'
                #Word_Label_List.extend(tempList)
                Word_Label_List.append(tempList)
        return Word_Label_List
#random seed fixed, but I think there has a lot problem in decide the seed
#learn it from lab4_solution
random.seed(6)
RRule = random.random()

#create a new class to 
class Word_Label:
    def __init__(self):
        self.word = None
        self.label = None
        self.previous = None
        self.next = None
        self.sub = None 

class Binary_perceptron:
    def __init__(self, train, test, multipalTime):
        self.multipalTime = multipalTime
        self.train = train
        self.test = test
        self.weight = {}#weight = {'word':{'O':1,'PER':2,...,'MISC':2},}
        self.trainProcess()
        self.testProcess()
        
    def trainProcess(self):
        for i in range(self.multipalTime):
            trainData = self.train
            random.shuffle(trainData, lambda: RRule)
            for item in trainData:
                for node in item:
                    predictLabel = self.predict(node)
                    if not predictLabel == node.label:
                        self.update(node, predictLabel)
        
    def predict(self, node):
        if node.word in self.weight.keys():
            return sorted(self.weight[node.word],key = lambda i : self.weight[node.word][i], reverse = True)[0]
        else:
            return 'O'

    def update(self, node, predictLabel):
        labelList = {'O': 0, 'PER': 0, 'LOC': 0, 'ORG': 0, 'MISC': 0}
        if node.word in self.weight.keys():
            self.weight[node.word][node.label] += 1/self.multipalTime
            self.weight[node.word][predictLabel] -= 1/self.multipalTime
        else:
            labelList[node.label] += 1/self.multipalTime
            labelList[predictLabel] -= 1/self.multipalTime
            self.weight[node.word] = labelList

    def testProcess(self):
        correct = []
        predicted = []
        for item in self.test:
            for node in item:
                correct.append(node.label)
                predicted.append(self.predict(node))
        f1_micro = f1_score(correct, predicted, average='micro', labels=['ORG', 'MISC', 'PER', 'LOC'])
        print('----------------------------------------')
        print('current word-current label \nfi_micro is:',f1_micro)
        print('----------------------------------------')
        self.top10()
        print('----------------------------------------')

    def top10(self):
        print('The List of O top 10 is :\n',[item for item in sorted(self.weight, key = lambda i : self.weight[i]['O'],reverse=True)[:10]])
        print('The List of PER top 10 is :\n',[item for item in sorted(self.weight, key = lambda i : self.weight[i]['PER'],reverse=True)[:10]])
        print('The List of LOC top 10 is :\n',[item for item in sorted(self.weight, key = lambda i : self.weight[i]['LOC'],reverse=True)[:10]])
        print('The List of ORG top 10 is :\n',[item for item in sorted(self.weight, key = lambda i : self.weight[i]['ORG'],reverse=True)[:10]])
        print('The List of MISC top 10 is :\n',[item for item in sorted(self.weight, key = lambda i : self.weight[i]['MISC'],reverse=True)[:10]])

        
class structuredPerceptronLabel:
    def __init__(self, train, test, multipalTime, subFeatures):
        self.multipalTime = multipalTime
        self.train = train
        self.test = test
        self.subFeatures = subFeatures
        self.weight = {'wordLabel':{},
        'previousLabel':{'start':{'O': 0, 'PER': 0, 'LOC': 0, 'ORG': 0, 'MISC': 0}
                        ,'O':{'O': 0, 'PER': 0, 'LOC': 0, 'ORG': 0, 'MISC': 0}
                        ,'PER':{'O': 0, 'PER': 0, 'LOC': 0, 'ORG': 0, 'MISC': 0}
                        ,'LOC':{'O': 0, 'PER': 0, 'LOC': 0, 'ORG': 0, 'MISC': 0}
                        ,'ORG':{'O': 0, 'PER': 0, 'LOC': 0, 'ORG': 0, 'MISC': 0}
                        ,'MISC':{'O': 0, 'PER': 0, 'LOC': 0, 'ORG': 0, 'MISC': 0}}}
        self.trainProcess()
        self.testProcess()
    
    def trainProcess(self):
        for i in range(self.multipalTime):
            trainData = self.train
            random.shuffle(trainData, lambda: RRule)
            for item in trainData:
                predictstructuredLabel = self.predict(item)
                if not predictstructuredLabel == [node.label for node in item]:
                    self.update(item, predictstructuredLabel)

#I divide predict process into two part, one part for the first two process,
#after that, I repeat a viterbi process
    def predict(self, nodeList):
        firstColumn = {}
        secondColumn = {}
        if nodeList[0].word in self.weight['wordLabel'].keys():
            for item in self.weight['previousLabel']['start'].keys():
                firstColumn[item] = self.weight['previousLabel']['start'][item] + self.weight['wordLabel'][nodeList[0].word][item]
        else:
            firstColumn = {'O': 0, 'PER': 0, 'LOC': 0, 'ORG': 0, 'MISC': 0}
        if len(nodeList) == 1 :
            if self.subFeatures['number']:
                if self.numberJudge(nodeList[0]):
                    return ['O']
                else:
                    return [sorted(firstColumn, key = lambda i : firstColumn[i],reverse = True)[0]]
            else:
                return [sorted(firstColumn, key = lambda i : firstColumn[i],reverse = True)[0]]
        if nodeList[1].word in self.weight['wordLabel'].keys():
            for item in firstColumn.keys():
                for label in self.weight['wordLabel'][nodeList[1].word].keys():
                    secondColumn[(item,label)] = firstColumn[item] + self.weight['wordLabel'][nodeList[1].word][label]
            predictLabel = [item for item in sorted(secondColumn, key = lambda i: secondColumn[i], reverse = True)[0]]
        else:
            predictLabel = [sorted(firstColumn, key = lambda i : firstColumn[i],reverse = True)[0],'O']
        if len(nodeList) == 2:
            if self.subFeatures['number']:
                for q in range(len(nodeList)):
                    if self.numberJudge(nodeList[q]):
                        predictLabel[q] = 'O'
                return predictLabel
            else:
                return predictLabel
        for i in range(len(nodeList)-2):
            predictLabel.extend(self.viterbi(i, predictLabel[-1], nodeList))
        if self.subFeatures['number']:
            for m in range(len(nodeList)):
                if self.numberJudge(nodeList[m]):
                    predictLabel[m] = 'O'
        return predictLabel

    def viterbi(self,time , previousLabel, nodeList):
        column = {}
        if nodeList[time+2].word in self.weight['wordLabel'].keys():
            for label in self.weight['wordLabel'][nodeList[time+2].word].keys():
                column[label] = self.weight['wordLabel'][nodeList[time+2].word][label] + self.weight['previousLabel'][previousLabel][label]
            return [sorted(column, key = lambda i : column[i], reverse = True)[0]]
        else:
            return ['O']

    def update(self, nodeList, predictLabelList):
        nodeLabelList = [item.label for item in nodeList]
        for i in range(len(nodeList)):
            if nodeList[i].word in self.weight['wordLabel'].keys():
                self.weight['wordLabel'][nodeList[i].word][nodeList[i].label] += 1/self.multipalTime
                self.weight['wordLabel'][nodeList[i].word][predictLabelList[i]] -= 1/self.multipalTime
            else:
                Labellist = {'O': 0, 'PER': 0, 'LOC': 0, 'ORG': 0, 'MISC': 0}
                Labellist[nodeList[i].label] += 1/self.multipalTime
                Labellist[predictLabelList[i]] -= 1/self.multipalTime
                self.weight['wordLabel'][nodeList[i].word] = Labellist
        #for start
        self.weight['previousLabel']['start'][nodeLabelList[0]] += 1/self.multipalTime
        self.weight['previousLabel']['start'][predictLabelList[0]] -= 1/self.multipalTime
        #print(predictLabelList)
        for i in range(len(nodeLabelList)-1):
            self.weight['previousLabel'][nodeLabelList[i]][nodeLabelList[i+1]] += 1/self.multipalTime
            self.weight['previousLabel'][predictLabelList[i]][predictLabelList[i+1]] -= 1/self.multipalTime

    #weight stucture 
        #weight = weight = {
                        #   'wordLabel' :{'word':{'O':1,'PER':2,...,'MISC':2},}, 
                        #   'previousLabel':{'start':{'O':1,'PER':2,...,'MISC':2},
                        #                      ....
                        #                     #'end' is not a previous label for anyone
                        #       
                        #                    }
                        # }

    def testProcess(self):
        correct = []
        predicted = []
        top10 = {'O': [], 'PER': [], 'LOC': [], 'ORG': [], 'MISC': []}
        for item in self.test:
            labelList = self.predict(item)
            for i in range(len(item)):
                correct.append(item[i].label)
                predicted.append(labelList[i])
                top10[labelList[i]].append(item[i].word)
            
        f1_micro = f1_score(correct, predicted, average='micro', labels=['ORG', 'MISC', 'PER', 'LOC'])
        print('----------------------------------------')
        if self.subFeatures['number']:
            print('current word-current label & previous label-current label\nwith number pre-process\nfi_micro is:',f1_micro)
        else:
            print('current word-current label & previous label-current label\nfi_micro is:',f1_micro)
        print('----------------------------------------')
        print('The List of O top 10 is : \n',[item for item in sorted(Counter(top10['O']), key = lambda i : Counter(top10['O'])[i], reverse = True)[:10]])
        print('The List of PER top 10 is : \n',[item for item in sorted(Counter(top10['PER']), key = lambda i : Counter(top10['PER'])[i], reverse = True)[:10]])
        print('The List of LOC top 10 is : \n',[item for item in sorted(Counter(top10['LOC']), key = lambda i : Counter(top10['LOC'])[i], reverse = True)[:10]])
        print('The List of ORG top 10 is : \n',[item for item in sorted(Counter(top10['ORG']), key = lambda i : Counter(top10['ORG'])[i], reverse = True)[:10]])
        print('The List of MISC top 10 is : \n',[item for item in sorted(Counter(top10['MISC']), key = lambda i : Counter(top10['MISC'])[i], reverse = True)[:10]])
        print('----------------------------------------')

    def numberJudge(self, node):
        for item in node.word:
            if item.isdigit():
                return True
        return False

#this project I choose sub word feature
class sub_perceptron:
    def __init__(self, train, test, multipalTime):
        self.multipalTime = multipalTime
        self.train = train
        self.test = test
        self.weight = {}
        #weight = {'word':{'ed':{'O':1,'PER':2,...,'MISC':2}
                          #{'ing':{'O':1,'PER':2,...,'MISC':2}},
                          #                          }
        self.trainProcess()
        self.testProcess()
        
    def trainProcess(self):
        for i in range(self.multipalTime):
            trainData = self.train
            random.shuffle(trainData, lambda: RRule)
            for item in trainData:
                for node in item:
                    self.sub(node)
                    predictLabel = self.predict(node)
                    if not predictLabel == node.label:
                        self.update(node, predictLabel)
        
    def predict(self, node):
        if node.word in self.weight.keys():
            if node.sub in self.weight[node.word]:
                return sorted(self.weight[node.word][node.sub],key = lambda i : self.weight[node.word][node.sub][i], reverse = True)[0]
            else:
                return 'O'
        else:
            return 'O'

    def update(self, node, predictLabel):
        labelList = {'O': 0, 'PER': 0, 'LOC': 0, 'ORG': 0, 'MISC': 0}
        if node.word in self.weight.keys():
            if node.sub in self.weight[node.word].keys():
                self.weight[node.word][node.sub][node.label] += 1/self.multipalTime
                self.weight[node.word][node.sub][predictLabel] -= 1/self.multipalTime
            else:
                labelList[node.label] += 1/self.multipalTime
                labelList[predictLabel] -= 1/self.multipalTime
                self.weight[node.word][node.sub] = labelList
        else:
            labelList[node.label] += 1/self.multipalTime
            labelList[predictLabel] -= 1/self.multipalTime
            self.weight[node.word] = {}
            self.weight[node.word][node.sub] = labelList

    def testProcess(self):
        correct = []
        predicted = []
        for item in self.test:
            for node in item:
                self.sub(node)
                correct.append(node.label)
                predicted.append(self.predict(node))
        f1_micro = f1_score(correct, predicted, average='micro', labels=['ORG', 'MISC', 'PER', 'LOC'])
        print('----------------------------------------')
        print('sub word feature \nfi_micro is:',f1_micro)
        print('----------------------------------------')
        Odict = self.findDict('O')
        print('The List of O top 10 is :\n',[item for item in sorted(Odict, key = lambda i : Odict[i],reverse=True)[:10]])
        PERdict = self.findDict('PER')
        print('The List of PER top 10 is :\n',[item for item in sorted(PERdict, key = lambda i : PERdict[i],reverse=True)[:10]])
        LOCdict = self.findDict('LOC')
        print('The List of LOC top 10 is :\n',[item for item in sorted(LOCdict, key = lambda i : LOCdict[i],reverse=True)[:10]])
        ORGdict = self.findDict('ORG')
        print('The List of ORG top 10 is :\n',[item for item in sorted(ORGdict, key = lambda i : ORGdict[i],reverse=True)[:10]])
        MISCdict = self.findDict('MISC')
        print('The List of MISC top 10 is :\n',[item for item in sorted(MISCdict, key = lambda i : MISCdict[i],reverse=True)[:10]])
        print('----------------------------------------')

    def findDict(self, name):
        dic = {}
        for word in self.weight:
            count = 0
            for sub in self.weight[word]:
                count += self.weight[word][sub][name]
            dic[word] = count
        return dic

    def sub(self,node):
        if len(node.word) >= 3 :
            node.sub = node.word[-3:]
        else:
            node.sub = node.word

if __name__ == '__main__': 
    start = timeit.default_timer()
    config = CommandLine()
    #print(config.args)
    openFile = openfile(config.args)
    multipalTime = 10
    subFeatures = {'number':False}
    bigram = Binary_perceptron(openFile.train, openFile.test, multipalTime)
    structuredPrevious = structuredPerceptronLabel(openFile.train, openFile.test, multipalTime, subFeatures)
    subFeatures = {'number':True}
    structuredPrevious = structuredPerceptronLabel(openFile.train, openFile.test, multipalTime, subFeatures)
    sub_perceptron = sub_perceptron(openFile.train, openFile.test, multipalTime)
    elapsed = timeit.default_timer() - start
    print('The program take',elapsed,'seconds to complete.')