#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""\
------------------------------------------------------------
USE: python <PROGNAME>  review_polarity
OPTIONS:
    -h : print this help message
    
Created on Thu Mar 4 2018

@author: wlt
------------------------------------------------------------\
"""
import sys, getopt, re, nltk, timeit, glob, random
from collections import Counter
import pylab as plt
import numpy as np

class CommandLine:
    def __init__(self):
        opts, args = getopt.getopt(sys.argv[1:],'h')
        self.args = args
        if '-h' in opts:
            self.printHelp()
        
        #To ensure the number of the folder
        if not args[0] == "review_polarity":
            print("*** ERROR: need a folder named 'review_polarity' - ! ***", file=sys.stderr)
            self.printHelp()
        
    
    #Print the Help information
    def printHelp(self):
        help = __doc__.replace('<PROGNAME>',sys.argv[0],1)
        print(help, file=sys.stderr)
        sys.exit()

class perceptron:
    def __init__(self, folderName, shuffle, multipalPass, average):
        self.folderName = folderName
        self.shuffle = shuffle
        self.multipalPass = multipalPass
        self.average = average
        self.weight = {}
        
    #to update the weight for every iteration
    def update(self, binary, Weight, subjective):
        for item, value in binary.items():
            if item in Weight.keys():
                if subjective :
                    Weight[item] += value
                else:
                    Weight[item] -= value
            else:
                Weight[item] = value
        return Weight
    
    #to test the file is or not belong to its class
    def predict(self, binary, Weight):
        predictValue = 0
        for item, value in binary.items():
            if item in Weight.keys():
                predictValue += Weight[item]*value
        #print(predictValue)
        if predictValue >= 0:
            return True
        else:
            return False

        #get the evaluation information
    def evaluation(self):
        trueNeg,truePos = self.getResult()
        truePositive = np.array(truePos)
        trueNegtive = np.array(trueNeg)
        trueCorrect =  trueNegtive.sum()+truePositive.sum() 
        if self.average :
            print("the average negtive file number is ",trueNegtive.sum()/self.multipalPass)
            print("the average positive file number is ",truePositive.sum()/self.multipalPass)
            print("total is", trueCorrect/self.multipalPass)
            plt.plot(np.arange(self.multipalPass),(trueNegtive+truePositive)/400,'rx')
            plt.show()
            return trueCorrect/400/self.multipalPass
        else:
            print("the negtive file number is ",trueNegtive.sum())
            print("the positive file number is ",truePositive.sum())
            print("total is", trueCorrect)
            plt.plot(np.arange(self.multipalPass),(trueNegtive+truePositive)/400,'rx')
            plt.show()
            return trueCorrect/400
    
    #to update every weight into a final weight
    def updateMulWeight(self, Weight):
        weight = self.weight
        for item, value in Weight.items():
            if item in weight.keys():
                weight[item] += value/multipalPass
            else:
                weight[item] = value/multipalPass
        self.weight = weight

    def getResult(self):
        folderName = self.folderName
        shuffle = self.shuffle
        pos_filenames = glob.glob(folderName+'/txt_sentoken/pos/*')
        neg_filenames = glob.glob(folderName+'/txt_sentoken/neg/*')
        truePos = []
        trueNeg = []

        for j in range(self.multipalPass):
            Pos = 0
            Neg = 0
            Weight = {}
            #this part is to shuffle the data,
            #every time I shuffle the data and I will update the weight and test corrected number
            if shuffle == 1 :
                random.shuffle(pos_filenames)
                random.shuffle(neg_filenames)
            for i in range(800):
                pos_filename = pos_filenames[i]
                neg_filename = neg_filenames[i]
                #After I check the lecture I change the solution
                #separate = re.compile("\w+\'?\w+")
                #    print(Counter(separate.findall(infile.read())))
                with open(pos_filename,'r') as infile:
                #I have test several times which shows that without lower(), the result is better
                    binary = Counter(re.sub("[^\w']"," ", infile.read()).split())
                    if not (self.predict(binary, Weight)):
                        Weight = self.update(binary, Weight, True)
                with open(neg_filename,'r') as infile:
                    binary = Counter(re.sub("[^\w']"," ", infile.read()).split())
                    if (self.predict(binary, Weight)):
                        Weight = self.update(binary, Weight, False)
            
            #to get the multipal pass Weight which is a average Weight
            self.updateMulWeight(Weight)

            for i in range(200):
                pos_rest_filename = pos_filenames[999-i]
                neg_rest_filename = neg_filenames[999-i]
                with open(pos_rest_filename,'r') as infile:
                    binary = Counter(re.sub("[^\w']"," ", infile.read()).split())
                    if(self.predict(binary,self.weight)):
                        Pos += 1
                
                with open(neg_rest_filename,'r') as infile:
                    binary = Counter(re.sub("[^\w']"," ", infile.read()).split())
                    if not (self.predict(binary,self.weight)):
                        Neg += 1
            truePos.append(Pos)
            trueNeg.append(Neg)
        return trueNeg, truePos    


        


        
if __name__ == '__main__':
    config = CommandLine()
    shuffle = 1
    multipalPass = 2
    average = True
    binaryPerceptron = perceptron(config.args[0], shuffle, multipalPass, average)
    print(binaryPerceptron.evaluation())
    #print(sorted(binaryPerceptron.weight, key = lambda i : binaryPerceptron.weight[i]))
    import pylab as plt
    #x = [1,2,3,4,5,6,7,8,9]
    #y = [9,8,7,6,5,4,3,2,1]
    #plt.plot(x,y,'rx')
    #plt.show()

