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
        '''
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
                arg = args[1]
                print("*** ERROR: txt file input error - ! ***"+str(arg), file=sys.stderr)
                print(args, file=sys.stderr)
                self.printHelp()
        


    #Print the Help information
    def printHelp(self):
        help = __doc__.replace('<PROGNAME>',sys.argv[0],1)
        print(help, file=sys.stderr)
        sys.exit()
    '''
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
        #print(algorism, file=sys.stderr)
        self.check()
        
    
    def check(self):
        #get the input about all information
        input = self.prepare(self.sample)
        if self.algorism in ['B','D','I','G','H','A']:
            if self.algorism == 'B':
                testbfs = bfsClass(input)
                testbfs.testbfs()
            if self.algorism == 'D':
                testdfs = dfsClass(input)
                testdfs.testdfs()
            if self.algorism == 'I':
                testids = idsClass(input)
                testids.testids()
            if self.algorism == 'G':
                testgreedy = greedyClass(input)
                testgreedy.testgreedy()
            if self.algorism == 'H':
                testhill = hillClass(input)
                testhill.testhill()
            if self.algorism == 'A':
                testa = a_starClass(input)
                testa.testAstar()
            # if self.algorism == 'T':
            #     testids = idsClass(input)
            #     testids.testids()

    def prepare(self,sample):
        input = {}
        input['start'] = Digits(sample[0])
        input['final'] = Digits(sample[1])
        #to get the banList
        if len(sample)>=3 and len(sample[2]):
            input['banList'] = [int(item) for item in sample[2].split(",")]
        else:
            input['banList'] = []
        #print(sample, file=sys.stderr)
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

#new class for a_star, simply because in IDS or Greedy or Hill-climbing, it don't need uniqueCode to
#identity two Node, but in a_star, it has a uniqueCode for each Node
class Node2Astar:
    def __init__(self, digits):
        self.parent = None
        self.digits = digits
        self.childs = [False,False,False,False,False,False]
        self.depth = None
        self.count = None

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
        self.a_star_completedListRecord = []
        
        self.count = 0
        self.topNode.count = self.count

    def testAstar(self):
        for i in range(10000):
            if i == 0:
                if self.checkTop():
                    break
            if  self.target:
                self.printAstartResult()
                #self.printAstarProcess(self.a_star_completedList)
                self.printProcess(self.a_star_completedListRecord)
                break 
            if len(self.a_star_openList)+len(self.a_star_completedList) > 999 :
                print('No solution found.')
                #self.printAstarProcess(self.a_star_completedList)
                self.printProcess(self.a_star_completedListRecord)
                break
            if len(self.a_star_openList) == 0 :
                print('No solution found.')
                #self.printAstarProcess(self.a_star_completedList)
                self.printProcess(self.a_star_completedListRecord)
                break

            #give a todoNode to start the explore
            #print([item.digits.numberStr for item in self.a_star_openList.values()],i,'open before rank',file=sys.stderr)
            todoNode = self.rankA_star([item for item in self.a_star_openList.values()])
            self.getAstarChild(todoNode)
            #print([item.digits.numberStr for item in self.a_star_completedList.values()],i,'completed',file=sys.stderr)
            #print([item.digits.numberStr for item in self.a_star_openList.values()],i,'todo',file=sys.stderr)
    
    #this method is to get the six possible child of the todoNode 
    def getAstarChild(self, todonode):
        self.a_star_openList.pop(todonode.unique())
        #which is really interesting in python2.7, the element in dic has a sequence
        #self.a_star_completedList[todonode.unique()] = todonode
        self.a_star_completedListRecord.append(todonode)#new
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
                    #which is really interesting in python2.7, the element in dic has a sequence
                    #self.a_star_completedList[newNode.unique()] = newNode
                    self.a_star_completedListRecord.append(newNode)#new
                    self.resultNode = newNode
                #to prevent the top node, which will lead to a circle
                if not self.topNode.digits.numberStr == newNode.digits.numberStr :
                    if not newNode.unique() in self.a_star_openList.keys():
                        
                        newNode.count = self.count
                        self.count += 1

                        self.a_star_openList[newNode.unique()] = newNode
                        #print([item.digits.numberStr for item in self.a_star_openList.values()],i,'appending',file=sys.stderr)

    def rankA_star(self,nodeList):
        rank = {}
        for item in nodeList:
            #use depth as the distance with topNode, this prevent some circle
            rank[item] = self.calculateHeuristic(item,self.targetNode) + item.depth
        #sortedNodeList = sorted(rank, key = lambda i : rank[i], reverse = True)
        #print([item.digits.numberStr for item in rank.keys()],'before rank',file=sys.stderr)
        minimum = 27
        minkey = self.topNode
        for key in rank.keys():
            if rank[key] < minimum:
                minimum = rank[key]
                minkey = key
            if rank[key] == minimum:
                if key.count > minkey.count:
                    minimum = rank[key]
                    minkey = key 
        #print([item.digits.numberStr for item in sortedNodeList],'sorted',file=sys.stderr)
        #print(minkey.digits.numberStr,'sorted',file=sys.stderr)
        #print([item.digits.numberStr for item in sortedNodeList],'1111111')
        
        #if len(sortedNodeList) > 2:
        #    if sortedNodeList[-1].digits.numberStr == sortedNodeList[-2].digits.numberStr:
        #        if sortedNodeList[-2].depth < sortedNodeList[-1].depth:
        #            return sortedNodeList[-2]
        #print(sortedNodeList, file=sys.stderr)
        return minkey
        
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

    # def printAstarProcess(self, quene):
    #     queneStr = ''
    #     for item in quene.keys():
    #         queneStr += quene[item].digits.numberStr+','
    #     print(queneStr[:-1],'sorted',file=sys.stderr)
        
    def printProcess(self, quene):
        queneStr = ''
        for item in quene:
            queneStr += item.digits.numberStr+','
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



class greedyClass():
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
        self.greedy_openList = {self.topNode.unique():self.topNode}
        #self.a_star_NodeList = {self.topNode.unique():self.topNode}
        #this completedList is to store those node which has been explored
        self.greedy_completedList = {}
        self.greedy_completedListRecord = []

        self.count = 0
        self.topNode.count = self.count

    def testgreedy(self):
        for i in range(10000):
            if i == 0:
                if self.checkTop():
                    break
            if  self.target:
                self.printGreedyResult()
                #self.printGreedyProcess(self.greedy_completedList)
                self.printProcess(self.greedy_completedListRecord)
                #print(self.printGreedyResult()+'\n'+self.printGreedyProcess(self.greedy_completedList))
                break 
            if len(self.greedy_openList)+len(self.greedy_completedList) > 999 :
                print('No solution found.')
                #self.printGreedyProcess(self.greedy_completedList)
                self.printProcess(self.greedy_completedListRecord)
                #print('No solution found.\n'+self.printGreedyProcess(self.greedy_completedList))
                break
            if len(self.greedy_openList) == 0 :
                print('No solution found.')
                #self.printGreedyProcess(self.greedy_completedList)
                self.printProcess(self.greedy_completedListRecord)
                #print('No solution found.\n'+self.printGreedyProcess(self.greedy_completedList))
                break

            #give a todoNode to start the explore
            todoNode = self.rankgreedy([item for item in self.greedy_openList.values()])
            self.getGreedyChild(todoNode)
            #print([item.digits.numberStr for item in self.greedy_completedList.values()],i,'completed')
            #print([item.digits.numberStr for item in self.greedy_openList.values()],i,'todo')
    
    #this method is to get the six possible child of the todoNode 
    def getGreedyChild(self, todonode):
        self.greedy_openList.pop(todonode.unique())
        #which is really interesting in python2.7, the element in dic has a sequence
        #self.greedy_completedList[todonode.unique()] = todonode
        self.greedy_completedListRecord.append(todonode)
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
                    #which is really interesting in python2.7, the element in dic has a sequence
                    #self.greedy_completedList[newNode.unique()] = newNode
                    self.greedy_completedListRecord.append(newNode)
                    self.resultNode = newNode
                #to prevent the top node, which will lead to a circle
                if not self.topNode.digits.numberStr == newNode.digits.numberStr :
                    if not newNode.unique() in self.greedy_openList.keys():
                        self.greedy_openList[newNode.unique()] = newNode

                        newNode.count = self.count
                        self.count += 1

    def rankgreedy(self,nodeList):
        rank = {}
        for item in nodeList:
            #use depth as the distance with topNode, this prevent some circle
            rank[item] = self.calculateHeuristic(item,self.targetNode)
        #print([item.digits.numberStr for item in rank],'111') 
        #sortedNodeList = sorted(rank, key = lambda i : rank[i], reverse = True)

        minimum = 27
        minkey = self.topNode
        for key in rank.keys():
            if rank[key] < minimum:
                minimum = rank[key]
                minkey = key
            if rank[key] == minimum:
                if key.count > minkey.count:
                    minimum = rank[key]
                    minkey = key 

        #print([item.digits.numberStr for item in sortedNodeList],'222')
        return minkey
        
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

    # def printGreedyProcess(self, quene):
    #     queneStr = ''
    #     for item in quene.keys():
    #         queneStr += quene[item].digits.numberStr+','
    #     print(queneStr[:-1])
    #     #return queneStr[:-1]

    def printGreedyResult(self):
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
        #return resultStr[:-1]
            
    def printProcess(self, quene):
        queneStr = ''
        for item in quene:
            queneStr += item.digits.numberStr+','
        print(queneStr[:-1])


    def getStr(self, numberList):
        combine = ''
        for item in numberList:
            combine += str(item)
        return combine



class hillClass():
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
        self.hill_openList = {self.topNode.unique():self.topNode}
        #self.a_star_NodeList = {self.topNode.unique():self.topNode}
        #this completedList is to store those node which has been explored
        self.hill_completedList = {}

        self.hill = False
        self.hillDistance = 27

        self.hill_completedListRecord = []

        self.count = 0
        self.topNode.count = self.count

    def testhill(self):
        for i in range(10000):
            if i == 0:
                if self.checkTop():
                    break
            if  self.target:
                self.printhillResult()
                #self.printhillProcess(self.hill_completedList)
                self.printProcess(self.hill_completedListRecord)
                break 
            if len(self.hill_openList)+len(self.hill_completedList) > 999 :
                print('No solution found.')
                #self.printhillProcess(self.hill_completedList)
                self.printProcess(self.hill_completedListRecord)
                break
            if len(self.hill_openList) == 0 :
                print('No solution found.')
                #self.printhillProcess(self.hill_completedList)
                self.printProcess(self.hill_completedListRecord)
                break

            #give a todoNode to start the explore
            todoNode = self.rankhill([item for item in self.hill_openList.values()])
            if self.hill :
                print('No solution found.')
                #self.printhillProcess(self.hill_completedList)
                self.printProcess(self.hill_completedListRecord)
                break
            self.gethillChild(todoNode)
            #print([item.digits.numberStr for item in self.hill_completedList.values()],i,'completed')
            #print([item.digits.numberStr for item in self.hill_openList.values()],i,'todo')
    
    #this method is to get the six possible child of the todoNode 
    def gethillChild(self, todonode):
        self.hill_openList.pop(todonode.unique())
        #which is really interesting in python2.7, the element in dic has a sequence
        #self.hill_completedList[todonode.unique()] = todonode
        self.hill_completedListRecord.append(todonode)
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
                    #which is really interesting in python2.7, the element in dic has a sequence
                    #self.hill_completedList[todonode.unique()] = todonode
                    self.hill_completedListRecord.append(newNode)
                    self.resultNode = newNode
                #to prevent the top node, which will lead to a circle
                if not self.topNode.digits.numberStr == newNode.digits.numberStr :
                    if not newNode.unique() in self.hill_openList.keys():
                        self.hill_openList[newNode.unique()] = newNode

                        newNode.count = self.count
                        self.count += 1

    def rankhill(self,nodeList):
        rank = {}
        for item in nodeList:
            #use depth as the distance with topNode, this prevent some circle
            rank[item] = self.calculateHeuristic(item,self.targetNode)
        #print([item.digits.numberStr for item in rank],'111') 
        sortedNodeList = sorted(rank, key = lambda i : rank[i], reverse = True)
        #print([item.digits.numberStr for item in sortedNodeList],'222')

        minimum = 27
        minkey = self.topNode
        for key in rank.keys():
            if rank[key] < minimum:
                minimum = rank[key]
                minkey = key
            if rank[key] == minimum:
                if key.count > minkey.count:
                    minimum = rank[key]
                    minkey = key 

        if self.hillDistance > minimum:
            self.hillDistance = minimum
        else:
            self.hill = True
        return minkey
        
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

    # def printhillProcess(self, quene):
    #     queneStr = ''
    #     for item in quene.keys():
    #         queneStr += quene[item].digits.numberStr+','
    #     print(queneStr[:-1])
                
    def printProcess(self, quene):
        queneStr = ''
        for item in quene:
            queneStr += item.digits.numberStr+','
        print(queneStr[:-1])

    def printhillResult(self):
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

class bfsClass():
    def __init__(self, input):
        self.startDigits = input['start']
        self.topNode = Node2Astar(self.startDigits)
        self.topNode.parent = self.topNode
        self.topNode.depth = 0
        self.topNode.digits.lastDigits = 100
        targetDigits = input['final']
        self.targetNode = Node2Astar(targetDigits)
        self.banList = input['banList']

        self.resultNode = None
        self.target = False
        self.check = False
        #self.distance = self.calculateHeuristic(self.topNode,self.targetNode)
        #this openList is to store the node expanded
        self.bfs_SequenceList = [self.topNode]
        self.bfs_openList = {self.topNode.unique():self.topNode}
        #self.a_star_NodeList = {self.topNode.unique():self.topNode}
        #this completedList is to store those node which has been explored
        #self.bfs_completedList = {}


    def testbfs(self):
        for i in range(10000):
            if i == 0:
                if self.checkTop():
                    break
            if  self.target:
                self.printbfsResult()
                self.printProcess(self.bfs_SequenceList)
                break 
            if len(self.bfs_SequenceList) > 999 :
                print('No solution found.')
                self.printProcess(self.bfs_SequenceList)
                break
            if len(self.bfs_openList) == 0 :
                print('No solution found.')
                self.printProcess(self.bfs_SequenceList)
                break
            preventBlock = len(self.bfs_SequenceList)            
            #give a todoNode to start the explore
            todoNode = self.bfs_SequenceList[i]
            self.getbfsChild(todoNode)
            if preventBlock == len(self.bfs_SequenceList) and i == len(self.bfs_SequenceList)-1:
                print('No solution found.')
                self.printProcess(self.bfs_SequenceList)
                break
            #print([item.digits.numberStr for item in self.bfs_completedList.values()],i,'completed')
            #print([item.digits.numberStr for item in self.bfs_openList.values()],i,'todo')
    
    #this method is to get the six possible child of the todoNode 
    def getbfsChild(self, todonode):
        #self.bfs_openList.pop(todonode.unique())
        #self.bfs_completedList[todonode.unique()] = todonode
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
            if hasChanged and not int(self.getStr(currentNumList)) in self.banList :
                newDigits = Digits(self.getStr(currentNumList))
                newNode = Node2Astar(newDigits)
                #this is important to give newNode lastDigit and childs informaiton
                newNode.digits.lastDigits = i//2
                newNode.childs[i//2] = True
                newNode.childs[i//2+1] = True
                newNode.depth = todonode.depth + 1
                newNode.parent = todonode
                if not newNode.unique() in self.bfs_openList.keys():
                    self.bfs_SequenceList.append(newNode)
                    self.bfs_openList[newNode.unique()] = newNode
                    #print(newNode.digits.numberStr,'1231231231',newNode.unique(),'-------')
                #sonNodedistance = self.calculateHeuristic(newNode,self.targetNode) 
                if newNode.digits.numberStr == self.targetNode.digits.numberStr :
                    self.target = True
                    self.resultNode = newNode
                    break
                #to prevent the top node, which will lead to a circle
                #if not self.topNode.digits.numberStr == newNode.digits.numberStr :
                #if not newNode.unique() in self.bfs_openList.keys():
                    

        
    #this method to check the targetNode is or not the topNode, prevent some error
    def checkTop(self):
        if self.topNode.digits.numberStr == self.targetNode.digits.numberStr:
            self.check = True
        if self.check:
            print(self.topNode.digits.numberStr) 
            print(self.topNode.digits.numberStr) 
            return True
        return False

    def printbfsResult(self):
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
    
    def printProcess(self, quene):
        queneStr = ''
        for item in quene:
            queneStr += item.digits.numberStr+','
        print(queneStr[:-1])
            

    def getStr(self, numberList):
        combine = ''
        for item in numberList:
            combine += str(item)
        return combine

#Because the code above is too complex, I rewrite the a_star algorithm in a
#simple way, this way is much easier to understand.
class dfsClass():
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
        self.dfs_openList = {self.topNode.unique():self.topNode}#check Node unique
        self.todoList = [self.topNode]#store Node
        self.dfs_SequenceList = [self.topNode]#store all expand Node

    def testdfs(self):
        for i in range(10000):
            if i == 0:
                if self.checkTop():
                    break
            if  self.target:
                self.printdfsResult()
                self.printProcess(self.dfs_SequenceList)
                break 
            if len(self.dfs_SequenceList) > 999 :
                print('No solution found.')
                self.printProcess(self.dfs_SequenceList)
                break
            if len(self.dfs_SequenceList) == 0 :
                print('No solution found.')
                self.printProcess(self.dfs_SequenceList)
                break
            #give a todoNode to start the explore

            #print([item.digits.numberStr for item in self.todoList],'====')

            if len(self.todoList) :
                todoNode = self.todoList[-1]
            else : 
                print('No solution found.')
                self.printProcess(self.dfs_SequenceList)
                break
            if len(self.todoList) == 1 and self.todoList[0].childs.count(False) == 0 :
                print('No solution found.')
                self.printProcess(self.dfs_SequenceList)
                break
            if not self.getdfsChild(todoNode):
                self.todoList.pop()
            
    #this method is to get the six possible child of the todoNode 
    def getdfsChild(self, todonode):
        #print(todonode.digits.numberStr,'----',todonode.childs)
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
                    self.resultNode = newNode
                #to prevent the top node, which will lead to a circle
                if not newNode.unique() in self.dfs_openList.keys():
                    self.dfs_openList[newNode.unique()] = newNode
                    self.dfs_SequenceList.append(newNode)
                    self.todoList.append(newNode)
                    return True
        return False    

    #this method to check the targetNode is or not the topNode, prevent some error
    def checkTop(self):
        if self.topNode.digits.numberStr == self.targetNode.digits.numberStr:
            self.check = True
        if self.check:
            print(self.topNode.digits.numberStr) 
            print(self.topNode.digits.numberStr) 
            return True
        return False

    def printProcess(self, quene):
        queneStr = ''
        for item in quene:
            queneStr += item.digits.numberStr+','
        print(queneStr[:-1])

    def printdfsResult(self):
        resultStr = ''
        resultList = []
        judge = True
        lastNode = self.resultNode
        while judge :
            resultList.append(lastNode.digits.numberStr)
            if lastNode.unique() == self.topNode.unique() :
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

#Because the code above is too complex, I rewrite the a_star algorithm in a
#simple way, this way is much easier to understand.
class idsClass():
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
        self.ids_openList = {self.topNode.unique():self.topNode}#check Node unique
        self.todoList = [self.topNode]#store Node
        self.ids_SequenceList = []#store all expand Node
        self.preventCircle = []#record the item prevent circle
    def testids(self):
        for i in range(10000):
            if i == 0:
                if self.checkTop():
                    break
            if  self.target:
                self.printidsResult()
                self.printProcess(self.ids_SequenceList)
                break 
            if len(self.ids_SequenceList) > 999 :
                print('No solution found.')
                self.printProcess(self.ids_SequenceList)
                break
            #problem set up
            self.preventCircle = []
            self.ids_SequenceList.append(self.topNode)
            self.ids_openList = {self.topNode.unique():self.topNode}
            self.todoList = [self.topNode]
            while True:
                if len(self.todoList) :
                    todoNode = self.todoList[-1]
                else : 
                    break
                if not len(self.ids_SequenceList) > 999:
                    if not self.getidsChild(todoNode, i):
                        if self.target:
                            break
                        self.todoList.pop()
                else:
                    break
            if not i == 0 and not i in [item.depth for item in self.preventCircle]:
                print('No solution found.')
                self.printProcess(self.ids_SequenceList)
                break
            
    #this method is to get the six possible child of the todoNode 
    def getidsChild(self, todonode, maxdepth):
        #print(todonode.digits.numberStr,'----',todonode.childs)
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
                if newNode.depth > maxdepth:
                    return False
                newNode.parent = todonode
                #sonNodedistance = self.calculateHeuristic(newNode,self.targetNode) 
                if newNode.digits.numberStr == self.targetNode.digits.numberStr :
                    self.target = True
                    self.ids_SequenceList.append(newNode)
                    self.resultNode = newNode
                    self.preventCircle.append(newNode)
                    return False
                #to prevent the top node, which will lead to a circle
                if not newNode.unique() in self.ids_openList.keys():
                    self.ids_openList[newNode.unique()] = newNode
                    self.ids_SequenceList.append(newNode)
                    self.todoList.append(newNode)
                    self.preventCircle.append(newNode)
                    return True
        return False    

    #this method to check the targetNode is or not the topNode, prevent some error
    def checkTop(self):
        if self.topNode.digits.numberStr == self.targetNode.digits.numberStr:
            self.check = True
        if self.check:
            print(self.topNode.digits.numberStr) 
            print(self.topNode.digits.numberStr) 
            return True
        return False

    def printProcess(self, quene):
        queneStr = ''
        for item in quene:
            queneStr += item.digits.numberStr+','
        print(queneStr[:-1])

    def printidsResult(self):
        resultStr = ''
        resultList = []
        judge = True
        lastNode = self.resultNode
        while judge :
            resultList.append(lastNode.digits.numberStr)
            if lastNode.unique() == self.topNode.unique() :
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

if __name__ =='__main__':
    start = timeit.default_timer()
    config = CommandLine()
    openfile = openfile(config.args[1])
    algorithm = Algorithm(config.args[0],openfile.sample)
  
    