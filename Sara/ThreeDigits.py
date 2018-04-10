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
@author: Sara
------------------------------------------------------------\
"""
import sys, getopt, re, timeit


class CommandLine:
    def __init__(self):
        opts, args = getopt.getopt(sys.argv[1:],'h')
        self.args = args
        txtCheck = re.compile(r'\w+.txt')
        algorithmsCheck = re.compile('B|D|I|G|A|H|T')# T for test new algorithm
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
        #get the input about all information
        input = self.prepare(self.sample)
        if self.algorism in ['B','D','I','G','H','A','T']:
            method = Implement(input)
            if self.algorism == 'B':
                method.bfs()
            if self.algorism == 'D':
                method.dfs()
            if self.algorism == 'I':
                method.ids()
            if self.algorism == 'G':
                method.greedy()
            if self.algorism == 'H':
                method.hill_climbing()
            # if self.algorism == 'A':
            #     method.a_star()
            if self.algorism == 'A':
                testa = a_starClass(input)
                testa.testAstar()

    def prepare(self,sample):
        input = {}
        input['start'] = Digits(sample[0])
        #input['startInt'] = int(sample[0])
        input['final'] = Digits(sample[1])
        #input['finalInt'] = int(sample[1])
        #to get the banList
        if len(sample)>=3 and len(sample[2]):
            input['banList'] = [int(item) for item in sample[2].split(",")]
        else:
            input['banList'] = []
        return input

class Digits:
    #this class is to store the number, I use those number class to make Node class
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
        self.uniqueCode = self.unique()
    #define a uniqueCode to indicate the different between the number is same
    #but their child is different
    def unique(self):
        strCode = ''
        strCode += str(self.digits.lastDigits)
        for item in self.childs:
            if item:
                strCode += '1'
            else:
                strCode += '0'
        strCode += self.digits.numberStr
        return strCode

class Implement:
    def __init__(self, input):
        self.startDigits = input['start']
        self.topNode = Node(self.startDigits)
        self.topNode.parent = self.topNode
        self.topNode.depth = 0
        targetDigits = input['final']
        self.targetNode = Node(targetDigits)
        self.banList = input['banList']
        #foundation elements
        self.quene = [self.topNode] 
        self.target = False
        #DFS, IDS, greedy, hill parts has some same element I think, I creat new one to make it easy to read
        #DFS Node to start a new circle
        self.DfsNode = {}
        self.DfsNode[self.topNode.digits.numberStr] = self.topNode
        self.DfsQuene = [self.topNode]
        #IDS part
        self.IDSdepth = True
        self.IDSQueneRecord = []
        #greedy part
        self.greedyQuene = [self.topNode]
        self.greedyNode = Node(self.startDigits)
        #hill part
        self.hill = False
        self.hillDistance = 27 #largest distance
        
        #self.a_star_openList = {}
        #self.a_star_NodeList = {self.topNode.uniqueCode:self.topNode}

        self.check = False

    def bfs(self):
        for i in range(1000):
            if i == 0:
                #check if the topNode is the targetNode
                if self.checkTop():
                    break
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
            if i == 0:
                #check if the topNode is the targetNode
                if self.checkTop():
                    break
            if  self.target:
                self.printResult()
                self.printProcess(self.DfsQuene)
                break
            if len(self.DfsQuene) == 999:
                print('No solution found.')
                self.printProcess(self.DfsQuene)
                break
            if not self.DfsNode[self.DfsQuene[-1].digits.numberStr].childs.count(False) :
                #if all childs is False, pop it
                self.DfsQuene.pop()
            #self.target = self.getDFS_Child(self.DfsQuene[-1])
            self.target = self.getIDS_Child(self.DfsQuene[-1],None)

    def ids(self):
        for i in range(1000):
            if i == 0:
                #check if the topNode is the targetNode
                if self.checkTop():
                    break
            if  self.target:
                self.printResult()
                self.printProcess(self.IDSQueneRecord)
                break
            if len(self.IDSQueneRecord) > 999:
                print('No solution found.')
                self.printProcess(self.IDSQueneRecord)
                break
            self.IDSdepth = True
            #new Node to start topNode
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
                        #if it has explored, pop it
                        if not self.DfsNode[self.DfsQuene[-1].digits.numberStr].childs.count(False) :
                            self.DfsQuene.pop()
                        else:
                            self.target = self.getIDS_Child(self.DfsQuene[-1],i)
    # initial greedy algorithm
    def greedy(self):
        for i in range(1000):
            if i == 0:
                #check if the topNode is the targetNode
                if self.checkTop():
                    break
            if  self.target:
                self.printProcess(self.greedyQuene)
                self.printProcess(self.greedyQuene)
                break 
            if len(self.greedyQuene) == 999:
                print('No solution found.')
                self.printProcess(self.greedyQuene)
                break
            self.IDSdepth = True
            #to innitial new Node as start Node
            #this is complex, because I don't understand the important of depth and I want to reuse 
            #self.getIDS_Child, this is a little stupid, because the situation is different.
            #In this method, the all child of old Node will be True which mean I have explore
            #and its depth is large than 1.
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
            while self.IDSdepth:
                if self.target :
                    self.IDSdepth = False
                else:
                    #if no element in DfsQuene, it mean it explore all childNode
                    if not len(self.DfsQuene):
                        self.IDSdepth = False
                    else:
                        #if it explore, pop it
                        if not self.DfsNode[self.DfsQuene[-1].digits.numberStr].childs.count(False) :
                            self.DfsQuene.pop()
                        else:
                            self.target = self.getIDS_Child(self.DfsQuene[-1],1)
            if not self.target:
                self.greedyNode = self.rankGreedy(self.IDSQueneRecord)
                self.greedyQuene.append(self.greedyNode)
            else:
                self.greedyQuene.append(self.IDSQueneRecord[-1])#for record process

    #like greedy part, just give it a self.hill as direction to evaluate if stop
    def hill_climbing(self):
        for i in range(1000):
            if i == 0:
                #check if the topNode is the targetNode
                if self.checkTop():
                    break
            if  self.target:
                self.printProcess(self.greedyQuene)
                self.printProcess(self.greedyQuene)
                break 
            if len(self.greedyQuene) == 999:
                print('No solution found.')
                self.printProcess(self.greedyQuene)
                break
            if self.hill:
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
                            self.target = self.getIDS_Child(self.DfsQuene[-1],1)
            if not self.target:
                self.greedyNode = self.rankHill_climbing(self.IDSQueneRecord)
                if not self.hill:
                    self.greedyQuene.append(self.greedyNode)
            else:
                self.greedyQuene.append(self.IDSQueneRecord[-1])

    #old version a_star algorithm
    '''
    def a_star(self):
        #count = 0
        for i in range(1000):
            if i == 0:
                if self.checkTop():
                    break
            if  self.target:
                self.printAstartResult()
                self.printProcess(self.greedyQuene)
                break 
            if len(self.greedyQuene) == 999 :
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
            print([item.digits.numberStr for item in self.DfsQuene ],'before')
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
            print([item.digits.numberStr for item in self.IDSQueneRecord ],'1231231231231')
            for item in self.IDSQueneRecord:
                if not item.digits.numberStr == self.topNode.digits.numberStr:
                    if not item.digits.numberStr in self.a_star_openList.keys():
                        self.a_star_openList[item.digits.numberStr] = item
            #if i == 0 :
                #self.banList.append(self.topNode.digits.numberInt)
            if not self.target:
                self.greedyNode = self.rankA_star([item for item in self.a_star_openList.values()])
                self.a_star_openList.pop(self.greedyNode.digits.numberStr)
                #self.banList.append(self.greedyNode.digits.numberInt)
                self.greedyQuene.append(self.greedyNode)
                if self.greedyNode.uniqueCode not in self.a_star_NodeList.keys():
                    self.a_star_NodeList[self.greedyNode.uniqueCode] = self.greedyNode
                print([item.digits.numberStr for item in self.a_star_openList.values() ],'=========')
            else:
                self.greedyQuene.append(self.IDSQueneRecord[-1])
            print(self.greedyNode.digits.numberStr,'---' ,self.greedyNode.parent.digits.numberStr)
            #print(self.greedyNode.childs,'====;;;;;')
            print([item.digits.numberStr for item in self.a_star_NodeList.values()],'-----;;;;;;;')
    '''

        
        

    #rank the NodeList and find the score lowest and lasted added one to return 
    def rankGreedy(self,nodeList):
        rank = {}
        for item in nodeList:
            rank[item] = self.calculateHeuristic(item,self.targetNode)
        return sorted(rank, key = lambda i : rank[i], reverse = True)[-1]

    #use a self.hill to indicate the direction
    def rankHill_climbing(self,nodeList):
        rank = {}
        for item in nodeList:
            rank[item] = self.calculateHeuristic(item,self.targetNode)
        sortedNodeList = sorted(rank, key = lambda i : rank[i], reverse = True)
        if self.hillDistance > rank[sortedNodeList[-1]]:
            self.hillDistance = rank[sortedNodeList[-1]]
        else:
            self.hill = True
        return sortedNodeList[-1]

    # def rankA_star(self,nodeList):
    #     rank = {}
    #     for item in nodeList:
    #         rank[item] = self.calculateHeuristic(item,self.targetNode) + self.calculateHeuristic(item,self.topNode)
    #     sortedNodeList = sorted(rank, key = lambda i : rank[i], reverse = True)
    #     return sortedNodeList[-1]
        
    #calculate Manhattan distance
    def calculateHeuristic(self, firstNode, secondNode):
        heuristic = 0
        firstThreeDigits = firstNode.digits.Str2Digits()
        secondThreeDigits = secondNode.digits.Str2Digits()
        for i in range(3):
            heuristic += abs(firstThreeDigits[i]-secondThreeDigits[i])
        return heuristic


    #to find IDS child, I think this version is too complex and ignore the depth
    #which is a very important information in a_star algorithm, so I start a new 
    #getA_starChild below
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
        #find all six possible condition
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
            #prevent item in banList
            if not int(self.getStr(currentNumList)) in self.banList:
                newDigits = Digits(self.getStr(currentNumList))
                newDigits.lastDigits = childNumber//2
                #print(newDigits.numberStr,'<><><>',childNumber//2)
                newNode = Node(newDigits)
                newNode.parent = node
                #prevent error which node is topNode with None depth
                if not depth == None:              
                    newNode.depth = node.depth + 1
                    if depth - newNode.depth < 0:
                        node.childs[childNumber] = True
                        return False             
                newNode.childs[childNumber//2*2] = True
                newNode.childs[childNumber//2*2+1] = True
                #if it not in DfsNode, add it
                if not newDigits.numberStr in self.DfsNode.keys() :
                    self.DfsNode[newDigits.numberStr] = newNode
                else :
                #if it in DfsNode, update the information
                    self.DfsNode[newDigits.numberStr].childs[childNumber//2*2] = True
                    self.DfsNode[newDigits.numberStr].childs[childNumber//2*2+1] = True
                    self.DfsNode[newDigits.numberStr].lastDigits = childNumber//2
                self.quene.append(newNode)# for print
                self.DfsQuene.append(newNode)#for the sequence of dfs search element
                #prevent topNode error
                if not depth == None: 
                    self.IDSQueneRecord.append(newNode)
                if newDigits.numberInt == self.targetNode.digits.numberInt:
                    return True
        return False

    #get the BFS six child, only limited condition is lastdigits
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

    # def printAstartResult(self):
    #     queneStrList = []
    #     queneStr =  ''
    #     lastNode = self.greedyQuene[-1]
    #     while True: 
    #         queneStrList.append(lastNode.digits.numberStr+',')
    #         lastNode = self.a_star_NodeList[lastNode.parent.uniqueCode]
    #         if lastNode.digits.numberStr == self.topNode.digits.numberStr :
    #             break
    #     queneStrList.append(self.topNode.digits.numberStr+',')
    #     queneStrList.reverse()
    #     for item in queneStrList:
    #         queneStr += item
    #     print(queneStr[:-1])

    def getStr(self, numberList):
        combine = ''
        for item in numberList:
            combine += str(item)
        return combine
    #to check the topNode is or not targetNode
    def checkTop(self):
        if self.topNode.digits.numberStr == self.targetNode.digits.numberStr:
            self.check = True
        if self.check:
            print(self.topNode.digits.numberStr) 
            print(self.topNode.digits.numberStr) 
            return True
        return False

#Because the code above is too complex, I rewrite the a_star algorithm in a
#simple way, this way is much easier to understand.
class a_starClass():
    def __init__(self, input):
        self.startDigits = input['start']
        self.topNode = Node2Astar(self.startDigits)
        self.topNode.parent = self.topNode
        self.topNode.depth = 0
        targetDigits = input['final']
        self.targetNode = Node2Astar(targetDigits)
        self.banList = input['banList']

        self.resultNode = None
        self.target = False
        self.check = False
        #self.distance = self.calculateHeuristic(self.topNode,self.targetNode)
        #this openList is to store the node expanded
        self.a_star_openList = {self.topNode.unique():self.topNode}
        #self.a_star_NodeList = {self.topNode.unique():self.topNode}
        #this completedList is to store those node which has been explored
        self.a_star_completedList = {}

    def testAstar(self):
        for i in range(1000):
            if i == 0:
                if self.checkTop():
                    break
            if  self.target:
                self.printAstartResult()
                self.printAstarProcess(self.a_star_completedList)
                break 
            if len(self.a_star_openList)+len(self.a_star_completedList) >= 999 :
                print('No solution found.')
                self.printAstarProcess(self.a_star_completedList)
                break

            #give a todoNode to start the explore
            todoNode = self.rankA_star([item for item in self.a_star_openList.values()])
            self.getAstarChild(todoNode)
            #print([item.digits.numberStr for item in self.a_star_completedList.values()],i,'completed')
            #print([item.digits.numberStr for item in self.a_star_openList.values()],i,'todo')
    
    #this method is to get the six possible child of the todoNode 
    def getAstarChild(self, todonode):
        self.a_star_openList.pop(todonode.unique())
        self.a_star_completedList[todonode.unique()] = todonode
        #parentNodedistance = self.calculateHeuristic(todonode,self.targetNode)
        for i in range(6):#this is fixed
            hasChanged = False
            currentNumList = todonode.digits.Str2Digits()
            if not todonode.digits.lastDigits == i//2 :
                if i % 2 == 0:
                    if not currentNumList[i//2] == 0 :
                        currentNumList[i//2] -= 1
                        hasChanged = True
                        todonode.childs[i] = True
                    else:
                        todonode.childs[i] = True
                else:
                    if not currentNumList[i//2] == 9 :
                        currentNumList[i//2] += 1
                        hasChanged = True
                        todonode.childs[i] = True
                    else:
                        todonode.childs[i] = True
            if hasChanged and not int(self.getStr(currentNumList)) in self.banList:
                newDigits = Digits(self.getStr(currentNumList))
                newNode = Node2Astar(newDigits)
                #this is important to give newNode lastDigit and childs informaiton
                newNode.digits.lastDigits = i//2
                newNode.childs[i//2] = True
                newNode.childs[i//2+1] = True
                newNode.depth = todonode.depth + 1
                newNode.parent = todonode
                #sonNodedistance = self.calculateHeuristic(newNode,self.targetNode) 
                if newNode.digits.numberStr == self.targetNode.digits.numberStr :
                    self.target = True
                    self.a_star_completedList[newNode.unique()] = newNode
                    self.resultNode = newNode
                #to prevent the top node, which will lead to a circle
                if not self.topNode.digits.numberStr == newNode.digits.numberStr :
                    #if sonNodedistance <= parentNodedistance:
                    self.a_star_openList[newNode.unique()] = newNode

    def rankA_star(self,nodeList):
        rank = {}
        for item in nodeList:
            #use depth as the distance with topNode, this prevent some circle
            rank[item] = self.calculateHeuristic(item,self.targetNode) + item.depth
        sortedNodeList = sorted(rank, key = lambda i : rank[i], reverse = True)
        #print([item.digits.numberStr for item in sortedNodeList],'1111111')
        
        #if len(sortedNodeList) > 2:
        #    if sortedNodeList[-1].digits.numberStr == sortedNodeList[-2].digits.numberStr:
        #        if sortedNodeList[-2].depth < sortedNodeList[-1].depth:
        #            return sortedNodeList[-2]
        return sortedNodeList[-1]
        
    #this method to check the targetNode is or not the topNode, prevent some error
    def checkTop(self):
        if self.topNode.digits.numberStr == self.targetNode.digits.numberStr:
            self.check = True
        if self.check:
            print(self.topNode.digits.numberStr) 
            print(self.topNode.digits.numberStr) 
            return True
        return False
    #calculate heuristic with two Node
    def calculateHeuristic(self, firstNode, secondNode):
        heuristic = 0
        firstThreeDigits = firstNode.digits.Str2Digits()
        secondThreeDigits = secondNode.digits.Str2Digits()
        for i in range(3):
            heuristic += abs(firstThreeDigits[i]-secondThreeDigits[i])
        return heuristic

    def printAstarProcess(self, quene):
        queneStr = ''
        for item in quene.keys():
            queneStr += quene[item].digits.numberStr+','
        print(queneStr[:-1])

    def printAstartResult(self):
        resultStr = ''
        resultList = []
        judge = True
        lastNode = self.resultNode
        while judge :
            resultList.append(lastNode.digits.numberStr)
            if lastNode.digits.numberStr == self.topNode.digits.numberStr :
                judge = False
            lastNode = lastNode.parent
        resultList.reverse()
        for item in resultList:
            resultStr += item+ ','
        print(resultStr[:-1])
            

    def getStr(self, numberList):
        combine = ''
        for item in numberList:
            combine += str(item)
        return combine
#new class for a_star, simply because in IDS or Greedy or Hill-climbing, it don't need uniqueCode to
#identity two Node, but in a_star, it has a uniqueCode for each Node
class Node2Astar:
    def __init__(self, digits):
        self.parent = None
        self.digits = digits
        self.childs = [False,False,False,False,False,False]
        self.depth = None

    def unique(self):
        strCode = ''
        strCode += str(self.digits.lastDigits)
        for item in self.childs:
            if item:
                strCode += '1'
            else:
                strCode += '0'
        strCode += self.digits.numberStr
        return strCode


if __name__ =='__main__':
    start = timeit.default_timer()
    config = CommandLine()
    openfile = openfile(config.args[1])
    algorithm = Algorithm(config.args[0],openfile.sample)
  
    