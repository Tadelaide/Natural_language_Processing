#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""\
------------------------------------------------------------
USE: python <PROGNAME>  A simple.txt
------------------------------------------------------------
A includes some algorithms:
    BFS : the abbreviation of BFS is B
    DFS : the abbreviation of DFS is D
    IDS : the abbreviation of IDS is I
    Greedy : the abbreviation of Greedy is G
    A* : the abbreviation of A* is A
    Hill-climbing : the abbreviation of Hill-climbing is H

OPTIONS:
    -h : print this help message

Created on Thu Feb 15 2018
@author: wlt
------------------------------------------------------------\
"""
import sys, getopt, re, timeit


class CommandLine:
    def __init__(self):
        opts, args = getopt.getopt(sys.argv[1:],'h')
        self.args = args
        txtCheck = re.compile(r'\w+.txt')
        algorithmsCheck = re.compile('B|D|I|G|A|H')
        if ('-h','') in opts:
            self.printHelp()
        else:
            #To ensure the number of the file
            if not len(args) == 2:
                print("*** ERROR: need two arguments : an algorism abbreviation, and a txt file - ! ***", file=sys.stderr)
                self.printHelp()
            
            #To check the algorithms
            if not re.match(algorithmsCheck,args[0]):
                print("*** ERROR: Algorithm input error - ! ***", file=sys.stderr)
                self.printHelp()
        
            #To ensure input is txt file
            if not re.match(txtCheck,args[1]):
                print("*** ERROR: txt file input error - ! ***", file=sys.stderr)
                self.printHelp()


    #Print the Help information
    def printHelp(self):
        help = __doc__.replace('<PROGNAME>',sys.argv[0],1)
        print(help, file=sys.stderr)
        sys.exit()

class openfile:
    def __init__(self,file):
        self.file = file
        self.sample = self.readfile()

    def readfile(self):
        with open(self.file,'r') as infile:
            sample = infile.read().split("\n")
        return sample

class Algorithm:
    def __init__(self,algorism,sample):
        self.algorism = algorism
        self.sample = sample
        self.check()
    
    def check(self):
        input = self.prepare(self.sample)
        if self.algorism == 'B':
            bfs = BFS(input)
        if self.algorism == 'D':
            dfs = DFS(input)

    def prepare(self,sample):
        input = {}
        input['start'] = Digits(sample[0])
        #input['startInt'] = int(sample[0])
        input['final'] = Digits(sample[1])
        #input['finalInt'] = int(sample[1])
        input['banList'] = [int(item) for item in sample[2].split(",")]
        return input

class Digits:
    def __init__(self, numberStr):
        self.numberStr = numberStr
        self.numberThreeDigits = self.Str2Digits()
        self.numberInt = int(numberStr)
        self.lastDigits = None
        

    def Str2Digits(self):
        threedigits = []
        if not len(self.numberStr) == 3:
            for i in range(3-len(self.numberStr)):
                threedigits.append(0)
        for number in self.numberStr:
            threedigits.append(int(number))
        return threedigits

class Node:
    def __init__(self, digits):
        self.parent = None
        self.digits = digits

class BFS:
    def __init__(self, input):
        startDigits = input['start']
        self.topNode = Node(startDigits)
        self.topNode.parent = self.topNode
        targetDigits = input['final']
        self.targetNode = Node(targetDigits)
        self.banList = input['banList']
        self.quene = [self.topNode] 
        self.target = False
        self.bfs(input)
    
    def bfs(self,input):
        for i in range(1000):
            if  self.target:
                self.printResult()
                self.printProcess()
                break 
            if len(self.quene) == 999:
                print('No solution found.')
                self.printProcess()
            self.target = self.getChild(self.quene[i])
            
              
    def getChild(self, node):
        for p in range(len(node.digits.numberThreeDigits)):#3
            if not p == node.digits.lastDigits:
                for q in range(2):
                    hasChanged = False
                    currentNumList = node.digits.Str2Digits()
                    if q == 0 :
                        if not currentNumList[p] == 0 :
                            currentNumList[p] -= 1
                            hasChanged = True
                    if q == 1 :
                        if not currentNumList[p] == 9:
                            currentNumList[p] += 1
                            hasChanged = True
                    if hasChanged :
                        if not int(self.getStr(currentNumList)) in self.banList:
                            newDigits = Digits(self.getStr(currentNumList))
                            newDigits.lastDigits = p
                            newNode = Node(newDigits)
                            newNode.parent = node
                            self.quene.append(newNode)
                            if newDigits.numberInt == self.targetNode.digits.numberInt:
                                return True
        return False
        
    def printProcess(self):
        queneStr = ''
        for item in self.quene:
            queneStr += item.digits.numberStr+','
        print(queneStr[:-1])

    def printResult(self):
        resultNode = self.quene[-1]
        resultStr = ''
        resultList = []
        symbol = True
        while symbol:
            resultList.append(resultNode.digits.numberStr)
            resultNode = resultNode.parent
            if resultNode == self.topNode:
                symbol = False
        resultList.append(self.topNode.digits.numberStr)
        for item in resultList[::-1]:
            resultStr += item + ','
        print(resultStr[:-1])

    def getStr(self, numberList):
        combine = ''
        for item in numberList:
            combine += str(item)
        return combine



            

if __name__ =='__main__':
    start = timeit.default_timer()
    config = CommandLine()
    openfile = openfile(config.args[1])
    algorithm = Algorithm(config.args[0],openfile.sample)
  
    