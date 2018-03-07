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
from nltk.corpus import stopwords
import pylab as plt
import numpy as np
import spacy

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
    def __init__(self, folderName, shuffle, multipalPass, average, Model):
        self.folderName = folderName
        self.shuffle = shuffle
        self.multipalPass = multipalPass
        self.average = average
        self.Model = Model
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
        top10Neg = sorted(self.weight, key = lambda p : self.weight[p])[:10]
        top10Pos = sorted(self.weight, key = lambda p : self.weight[p], reverse=True)[:10]
        #To print the result
        if self.average :
            print("the average negtive file number is ",trueNegtive.sum()/self.multipalPass)
            print("the average positive file number is ",truePositive.sum()/self.multipalPass)
            print("total is", trueCorrect/self.multipalPass)
            print("Negtive Word Top 10 is")
            for item in top10Neg:
                print(item, self.weight[item])
            print("Positive Word Top 10 is")
            for item in top10Pos:
                print(item, self.weight[item])
            plt.figure(figsize=(12,6)) 
            plt.plot(np.arange(self.multipalPass),(trueNegtive+truePositive)/400,'rx')
            plt.title("the accuracy of average multipal pass")
            plt.xlabel("time")
            plt.ylabel("accuracy")
            plt.show()
            return trueCorrect/400/self.multipalPass
        else:
            print("the negtive file number is ",trueNegtive.sum())
            print("the positive file number is ",truePositive.sum())
            print("total is", trueCorrect)
            print("Negtive Word Top 10 is")
            for item in top10Neg:
                print(item, self.weight[item])
            print("Positive Word Top 10 is")
            for item in top10Pos:
                print(item, self.weight[item])
            plt.plot(np.arange(self.multipalPass),(trueNegtive+truePositive)/400,'rx')
            plt.title("the accuracy of multipal pass")
            plt.xlabel("time")
            plt.ylabel("accuracy")
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
                for q in range(self.multipalPass):
                    random.seed(q)
                    random.shuffle(pos_filenames)
                    random.shuffle(neg_filenames)
            #choose the first 800 file as train data
            for i in range(800):
                pos_filename = pos_filenames[i]
                neg_filename = neg_filenames[i]
                #After I check the lecture I change the solution
                #separate = re.compile("\w+\'?\w+")
                #print(Counter(separate.findall(infile.read())))
                with open(pos_filename,'r') as infile:
                    model = self.makeModel(infile)
                    if not (self.predict(model, Weight)):
                        Weight = self.update(model, Weight, True)
                with open(neg_filename,'r') as infile:
                    model = self.makeModel(infile)
                    if (self.predict(model, Weight)):
                        Weight = self.update(model, Weight, False)
            #to get the multipal pass Weight which is a average Weight
            self.updateMulWeight(Weight)
            #choose the rest 200 file as train data
            for i in range(200):
                pos_rest_filename = pos_filenames[999-i]
                neg_rest_filename = neg_filenames[999-i]
                with open(pos_rest_filename,'r') as infile:
                    model = self.makeModel(infile)
                    if(self.predict(model,self.weight)):
                        Pos += 1
                with open(neg_rest_filename,'r') as infile:
                    model = self.makeModel(infile)
                    if not (self.predict(model,self.weight)):
                        Neg += 1
            truePos.append(Pos)#to record the 
            trueNeg.append(Neg)
        return trueNeg, truePos    
        
    #this method is to select the model
    def makeModel(self, openfile):
        if self.Model['binary'] :
            return Counter(re.sub("[^\w']"," ", openfile.read()).lower().split())
        if self.Model['bigram'] :
            bigrams = []
            for line in openfile:
                bigrams.extend(nltk.bigrams(re.sub("[^\w']"," ", line).lower().split(), pad_left=True, pad_right=True))
            return Counter(bigrams)
        if self.Model['trigram'] :
            #the accuracy is a little bad which even worse than binary(bag of words)
            trigrams = []
            for line in openfile:
                trigrams.extend(nltk.trigrams(re.sub("[^\w']"," ", line).lower().split(), pad_left=True, pad_right=True))
            return Counter(trigrams)
        if self.Model['adjective']:
            #I have try use the tag of the spacy, but it take a very long time to a file
            #I give up this method which extract all adjective
            #in one turn, it take 120 second to train one time
            is_adjective = lambda pos: pos[:2] == 'JJ'
            word = [word for (word, pos) in nltk.pos_tag(nltk.word_tokenize(openfile.read())) if is_adjective(pos)] 
            return Counter(word)
        if self.Model['stopListBigram'] :
            #I want to delete all stoplist, but it also take a very long time
            #give up
            #in one turn, it take 300 second to train one time
            stopListBigrams = []
            txt = re.sub("[^\w']"," ", openfile.read()).lower().split()
            processedTxt = [w for w in txt if not w in stopwords.words('english')]
            stopListBigrams.extend(nltk.bigrams(processedTxt, pad_left=True, pad_right=True))
            return Counter(stopListBigrams)


        
if __name__ == '__main__':
    start = timeit.default_timer()
    config = CommandLine()
    shuffle = 1
    multipalPass = 100
    average = True
    Model = {'binary': False, 'bigram': True, 'trigram' : False,'adjective': False,'stopListBigram' : False}
    binaryPerceptron = perceptron(config.args[0], shuffle, multipalPass, average, Model)
    print(binaryPerceptron.evaluation())
    #print(sorted(binaryPerceptron.weight, key = lambda i : binaryPerceptron.weight[i]))
    elapsed = timeit.default_timer() - start
    print("the program use ",elapsed," to finish")

