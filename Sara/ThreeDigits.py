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
        if self.algorism in ['B','D','I','G']:
            method = Implement(input)
            if self.algorism == 'B':
                method.bfs()
            if self.algorism == 'D':
                method.dfs()
            if self.algorism == 'I':
                method.ids()
            if self.algorism == 'G':
                method.greedy()
    def prepare(self,sample):
        input = {}
        input['start'] = Digits(sample[0])
        #input['startInt'] = int(sample[0])
        input['final'] = Digits(sample[1])
        #input['finalInt'] = int(sample[1])
        if len(sample)==3 :
            input['banList'] = [int(item) for item in sample[2].split(",")]
        else:
            input['banList'] = []
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
        self.childs = [False,False,False,False,False,False]
        self.depth = None

class Implement:
    def __init__(self, input):
        self.startDigits = input['start']
        self.topNode = Node(self.startDigits)
        self.topNode.parent = self.topNode
        self.topNode.depth = 0
        targetDigits = input['final']
        self.targetNode = Node(targetDigits)
        self.banList = input['banList']
        self.quene = [self.topNode] 
        self.target = False
        self.DfsNode = {}
        self.DfsNode[self.topNode.digits.numberStr] = self.topNode
        self.DfsQuene = [self.topNode]

        self.IDSdepth = True
        self.IDSQueneRecord = []
        self.greedyQuene = [self.topNode]
        self.greedyNode = Node(self.startDigits)

    def bfs(self):
        for i in range(1000):
            if  self.target:
                self.printResult()
                self.printProcess(self.quene)
                break 
            if len(self.quene) == 999:
                print('No solution found.')
                self.printProcess(self.quene)
                break
            self.target = self.getBFS_Child(self.quene[i])
    
    def dfs(self):
        for i in range(1000):
            if  self.target:
                self.printResult()
                self.printProcess(self.DfsQuene)
                break
            if len(self.quene) == 999:
                print('No solution found.')
                self.printProcess(self.DfsQuene)
                break
            if not self.DfsNode[self.DfsQuene[-1].digits.numberStr].childs.count(False) :
                self.DfsQuene.pop()
            #self.target = self.getDFS_Child(self.DfsQuene[-1])
            self.target = self.getIDS_Child(self.DfsQuene[-1],None)

    def ids(self):
        for i in range(1000):
            if  self.target:
                self.printResult()
                self.printProcess(self.IDSQueneRecord)
                break
            if len(self.IDSQueneRecord) > 999:
                print('No solution found.')
                self.printProcess(self.IDSQueneRecord)
                break
            self.IDSdepth = True
            idsTopNode = Node(self.startDigits)
            idsTopNode.depth = 0
            self.DfsQuene = [idsTopNode]
            self.DfsNode = {}
            self.DfsNode[idsTopNode.digits.numberStr] = idsTopNode
            self.IDSQueneRecord.append(idsTopNode)
            while self.IDSdepth:
                if self.target :
                    self.IDSdepth = False
                else:
                    if not len(self.DfsQuene):
                        self.IDSdepth = False
                    else:
                        if not self.DfsNode[self.DfsQuene[-1].digits.numberStr].childs.count(False) :
                            self.DfsQuene.pop()
                        else:
                            self.target = self.getIDS_Child(self.DfsQuene[-1],i)
  
    def greedy(self):
        #count = 0
        for i in range(1000):
            if  self.target:
                self.printProcess(self.greedyQuene)
                self.printProcess(self.greedyQuene)
                break 
            if len(self.quene) == 999:
                print('No solution found.')
                self.printProcess(self.greedyQuene)
                break
            self.IDSdepth = True
            greedyTopNode = Node(self.greedyNode.digits)
            greedyTopNode.depth = 0
            greedyTopNode.digits.lastDigits = self.greedyNode.digits.lastDigits
            if not self.greedyNode.digits.lastDigits == None :
                greedyTopNode.childs[self.greedyNode.digits.lastDigits*2] = True
                greedyTopNode.childs[self.greedyNode.digits.lastDigits*2+1] = True
            self.DfsQuene = [greedyTopNode]
            self.IDSQueneRecord = []

            self.DfsNode = {}
            self.DfsNode[greedyTopNode.digits.numberStr] = greedyTopNode 
            #print([item.digits.numberStr for item in self.DfsQuene ],'before')
            #print(self.DfsNode[self.DfsQuene[-1].digits.numberStr].childs)
            while self.IDSdepth:
                if self.target :
                    self.IDSdepth = False
                else:
                    if not len(self.DfsQuene):
                        self.IDSdepth = False
                    else:
                        if not self.DfsNode[self.DfsQuene[-1].digits.numberStr].childs.count(False) :
                            self.DfsQuene.pop()
                            #print('=-=-=-=-=-=-')
                        else:
                            self.target = self.getIDS_Child(self.DfsQuene[-1],1)
                            #print([item.digits.numberStr for item in self.DfsQuene],'in')
                            #print([item.childs for item in self.DfsQuene],'in childs')
                            #count +=1 
                            #if count >100:
                            #    self.target = True
            #print([item.digits.numberStr for item in self.DfsQuene ],'after')
            #print([item.digits.numberStr for item in self.IDSQueneRecord ],'1231231231231')
            if not self.target:
                self.greedyNode = self.rankGreedy(self.IDSQueneRecord)
                self.greedyQuene.append(self.greedyNode)
            else:
                self.greedyQuene.append(self.IDSQueneRecord[-1])
            #print(self.greedyNode.digits.numberStr,'---')

    def rankGreedy(self,nodeList):
        rank = {}
        for item in nodeList:
            rank[item] = self.calculateHeuristic(item,self.targetNode)
        return sorted(rank, key = lambda i : rank[i], reverse = True)[-1]


    def calculateHeuristic(self, firstNode, secondNode):
        heuristic = 0
        firstThreeDigits = firstNode.digits.Str2Digits()
        secondThreeDigits = secondNode.digits.Str2Digits()
        for i in range(3):
            heuristic += abs(firstThreeDigits[i]-secondThreeDigits[i])
        return heuristic

    def getIDS_Child(self, node, depth):
        if node.digits.numberStr in self.DfsNode.keys():
            node = self.DfsNode[node.digits.numberStr]
        #print(node.digits.numberStr,'parent',node.parent.digits.numberStr)
        #print(node.childs)
        if not node.childs.count(False) :
            return False
        childNumber = node.childs.index(False)
        currentNumList = node.digits.Str2Digits()
        #print(node.childs,'first----',node.digits.numberStr)
        hasChanged = False
        if childNumber == 0 :
            if not node.digits.lastDigits == 0 :
                if not currentNumList[0] == 0 :
                    currentNumList[0] -= 1
                    hasChanged = True
                    node.childs[0] = True
                else:
                    node.childs[0] = True
        elif childNumber == 1 :
            if not node.digits.lastDigits == 0 :
                if not currentNumList[0] == 9 :
                    currentNumList[0] += 1
                    hasChanged = True
                    node.childs[1] = True
                else:
                    node.childs[1] = True
        elif childNumber == 2 :
            if not node.digits.lastDigits == 1 :
                if not currentNumList[1] == 0 :
                    currentNumList[1] -= 1
                    hasChanged = True
                    node.childs[2] = True
                else:
                    node.childs[2] = True
        elif childNumber == 3 :
            if not node.digits.lastDigits == 1 :
                if not currentNumList[1] == 9 :
                    currentNumList[1] += 1
                    hasChanged = True
                    node.childs[3] = True
                else:
                    node.childs[3] = True
        elif childNumber == 4 :
            if not node.digits.lastDigits == 2 :
                if not currentNumList[2] == 0 :
                    currentNumList[2] -= 1
                    hasChanged = True
                    node.childs[4] = True
                else:
                    node.childs[4] = True
        else :
            if not node.digits.lastDigits == 2 :
                if not currentNumList[2] == 9 :
                    currentNumList[2] += 1
                    hasChanged = True
                    node.childs[5] = True
                else:
                    node.childs[5] = True
        if hasChanged :
            if not int(self.getStr(currentNumList)) in self.banList:
                newDigits = Digits(self.getStr(currentNumList))
                newDigits.lastDigits = childNumber//2
                #print(newDigits.numberStr,'<><><>',childNumber//2)
                newNode = Node(newDigits)
                newNode.parent = node
                if not depth == None:              
                    newNode.depth = node.depth + 1
                    if depth - newNode.depth < 0:
                        node.childs[childNumber] = True
                        return False             
                newNode.childs[childNumber//2*2] = True
                newNode.childs[childNumber//2*2+1] = True

                if not newDigits.numberStr in self.DfsNode.keys() :
                    self.DfsNode[newDigits.numberStr] = newNode
                else :
                    self.DfsNode[newDigits.numberStr].childs[childNumber//2*2] = True
                    self.DfsNode[newDigits.numberStr].childs[childNumber//2*2+1] = True
                    self.DfsNode[newDigits.numberStr].lastDigits = childNumber//2
                self.quene.append(newNode)# for print
                self.DfsQuene.append(newNode)#for the sequence of dfs search element
                if not depth == None: 
                    self.IDSQueneRecord.append(newNode)
                if newDigits.numberInt == self.targetNode.digits.numberInt:
                    return True
        return False
    
    def getBFS_Child(self, node):
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


    '''
    import sys
    sys.setrecursionlimit(9999)
    def getDFS_Child(self, node):
        if node.digits.numberStr in self.DfsNode.keys():
            node = self.DfsNode[node.digits.numberStr]
        #print(node.digits.numberStr,'parent',node.parent.digits.numberStr)
        #print(node.childs)
        if not node.childs.count(False) :
            return False
        childNumber = node.childs.index(False)
        currentNumList = node.digits.Str2Digits()
        #print(node.childs,'first----',node.digits.numberStr)
        hasChanged = False
        if childNumber == 0 :
            if not node.digits.lastDigits == 0 :
                if not currentNumList[0] == 0 :
                    currentNumList[0] -= 1
                    hasChanged = True
                    node.childs[0] = True
                else:
                    node.childs[0] = True
        elif childNumber == 1 :
            if not node.digits.lastDigits == 0 :
                if not currentNumList[0] == 9 :
                    currentNumList[0] += 1
                    hasChanged = True
                    node.childs[1] = True
                else:
                    node.childs[1] = True
        elif childNumber == 2 :
            if not node.digits.lastDigits == 1 :
                if not currentNumList[1] == 0 :
                    currentNumList[1] -= 1
                    hasChanged = True
                    node.childs[2] = True
                else:
                    node.childs[2] = True
        elif childNumber == 3 :
            if not node.digits.lastDigits == 1 :
                if not currentNumList[1] == 9 :
                    currentNumList[1] += 1
                    hasChanged = True
                    node.childs[3] = True
                else:
                    node.childs[3] = True
        elif childNumber == 4 :
            if not node.digits.lastDigits == 2 :
                if not currentNumList[2] == 0 :
                    currentNumList[2] -= 1
                    hasChanged = True
                    node.childs[4] = True
                else:
                    node.childs[4] = True
        else :
            if not node.digits.lastDigits == 2 :
                if not currentNumList[2] == 9 :
                    currentNumList[2] += 1
                    hasChanged = True
                    node.childs[5] = True
                else:
                    node.childs[5] = True
        if hasChanged :
            if not int(self.getStr(currentNumList)) in self.banList:
                newDigits = Digits(self.getStr(currentNumList))
                newDigits.lastDigits = childNumber//2
                #print(newDigits.numberStr,'<><><>',childNumber//2)
                newNode = Node(newDigits)
                newNode.parent = node
                
                newNode.childs[childNumber//2*2] = True
                newNode.childs[childNumber//2*2+1] = True
                newNode.depth = node.depth + 1

                #print(newNode.parent.digits.numberStr,'qwertrytyuiupoiuyretw',newDigits.numberStr)
                #print(newNode.parent.childs,'old')
                if not newDigits.numberStr in self.DfsNode.keys() :
                    self.DfsNode[newDigits.numberStr] = newNode
                else :
                    self.DfsNode[newDigits.numberStr].childs[childNumber//2*2] = True
                    self.DfsNode[newDigits.numberStr].childs[childNumber//2*2+1] = True
                    self.DfsNode[newDigits.numberStr].lastDigits = childNumber//2
                #print(newNode.childs,'=-=-=-=-=')
                #print(self.DfsNode[newDigits.numberStr].childs,'new')
                #print(childNumber//2)
                self.quene.append(newNode)# for print
                self.DfsQuene.append(newNode)#for the sequence of dfs search element
                if newDigits.numberInt == self.targetNode.digits.numberInt:
                    return True
        return False
    '''




    def printProcess(self, quene):
        queneStr = ''
        for item in quene:
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
            if resultNode.digits.numberStr == self.topNode.digits.numberStr:
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
  
    