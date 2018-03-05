#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""\
------------------------------------------------------------
USE: python <PROGNAME>  traindata.txt querydata.txt
OPTIONS:
    -h : print this help message
    
Created on Thu Feb 15 2018

@author: wlt
------------------------------------------------------------\
"""
import sys, getopt, re, nltk, timeit
from collections import Counter

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

    #Open the train file
    def openTrain(self):
        char = re.compile('\w+')
        trainFile = self.file[0]
        with open(trainFile,'r') as infile:
            #use the read() method which has the highest speed
            wordTrain = char.findall(infile.read().lower())
        return wordTrain

    #Open the query file
    def openQuery(self):
        queryFile = self.file[1]
        lines = []
        possibleWords = []
        #Get the possible word which has the "A/B"
        seperate = re.compile('\w+\/\w+')
        with open(queryFile,'r') as infile:
            for line in infile:
                #line = item.readline()
                lines.append(line.split(' :')[0])
                #Notic!!!!
                #if I use findall method, it will return a List 
                possibleWords.append(seperate.findall(line)[0].split('/'))
        return lines,possibleWords

#This class method is to process the return datatype to result and to print the result
class Result:
    def __init__(self,queryLine,queryPossibleWord, unigramResult, bigramResult, bigramWithSmoothResult):
        self.queryLine = queryLine
        self.PossibleWord = queryPossibleWord
        self.unigramResult = unigramResult
        self.bigramResult = bigramResult
        self.bigramWithSmoothResult = bigramWithSmoothResult
        self.printResult()

    #This method is to use the same format to print the result
    def printResult(self):
        for number in range(len(self.queryLine)):
            print()
            print("###############################################")
            print(number+1,":")
            print(queryLine[number])
            print("the result of two possible word '", self.PossibleWord[number][0],"' and '", self.PossibleWord[number][1], "' in three model is :")
            print("---------------------------------")
            print("the model of unigram :")
            print(self.unigramResult[number])
            print("the result of the unigram model is :")
            print(self.getResult(self.unigramResult[number]))
            print("---------------------------------")
            print("the model of bigram :")
            print(self.bigramResult[number])
            print("the result of the bigram model is :")
            print(self.getResult(self.bigramResult[number]))
            print("---------------------------------")
            print("the model of bigram with smooth(smooth = 1) :")
            print(self.bigramWithSmoothResult[number])
            print("the result of the bigram with smooth model is :")
            print(self.getResult(self.bigramWithSmoothResult[number]))
            print("###############################################")
            
    #This method is to process the return datatype into a result
    def getResult(self, probabilityResult):
        result = {}
        resultWord = sorted(probabilityResult, key = lambda p : probabilityResult[p], reverse = True)
        if (probabilityResult[resultWord[0]] == 0 ) and (probabilityResult[resultWord[1]] == 0):
            return "The probability of both two words is 0, the result is not reliable. "
        resultProbability = probabilityResult[resultWord[0]]
        result[resultWord[0]] = resultProbability
        return result

#This class is to build the Unigram model
class Unigram:
    def __init__(self,trainWords,possibleWord):
        self.unigram = Counter(trainWords)
        self.sum = len(trainWords)
        self.possibleWord = possibleWord

    '''
    #to make sure about the total number of words
    def getSum(self):
        sum = 0
        for key in self.unigram.keys():
            sum += self.unigram[key]
        print(sum)
    '''
    #Use the Unigram math equation to get the word probability
    def getUnigramWordProbability(self):
        unigramWordProbability = []
        for p in range(len(self.possibleWord)):
            probability = {}
            for q in range(len(self.possibleWord[p])):
                probability[self.possibleWord[p][q]] = (self.unigram[self.possibleWord[p][q]]/self.sum)
            unigramWordProbability.append(probability)
        return unigramWordProbability
        #The unigramWordProbability has the [{A:a,B:b}] datatype, which can be processed in result 



#This class is to build the Bigrams model using the nlkt.bigrams()
class Bigrams:
    def __init__(self, trainWord, possibleWord, queryLine):
        self.trainWord = trainWord
        self.possibleWord = possibleWord
        self.queryLine = queryLine
        self.bigramWordProbability = self.getBigramWordProbability()
        
    #Use the Bigrams math equation to get the word probability
    def getBigramWordProbability(self):
        bigram = []
        bigram.extend(nltk.bigrams(self.trainWord, pad_left=True, pad_right=True))
        self.bigrams = Counter(bigram)
        bigramsWordProbability = []
        for i in range(len(self.possibleWord)):
            #This part will be seperate by the " " and "____"
            wordList = self.queryLine[i].split(' ')
            index = wordList.index('____')
            probability = {}
            for j in range(len(self.possibleWord[i])):
                bigram1probablity = self.bigrams[wordList[index-1], self.possibleWord[i][j]]/len(self.trainWord)
                bigram2probablity = self.bigrams[self.possibleWord[i][j], wordList[index+1]]/len(self.trainWord)
                probability[self.possibleWord[i][j]] = bigram1probablity*bigram2probablity
            bigramsWordProbability.append(probability)
        return bigramsWordProbability
        #The unigramWordProbability has the [{A:a,B:b}] datatype, which can be processed in result 

class BigramsWithSmooth:
    def __init__(self, unigram, bigram, possibleWord, queryLine, smooth):
        self.unigram = unigram
        self.bigram = bigram
        self.smooth = smooth
        self.possibleWord = possibleWord
        self.queryLine = queryLine
        self.unique_words = len(unigram.keys()) + 2 # For the None paddings
        self.bigramsWithSmooth = self.getBigramsWithSmooth()

    def getBigramsWithSmooth(self):
        bigramsWithSmoothProbability = []
        for i in range(len(self.possibleWord)):
            wordList = self.queryLine[i].split(' ')
            index = wordList.index('____')
            probability = {}
            for j in range(len(self.possibleWord[i])):
                bigramSmooth1probablity = (self.bigram[wordList[index-1], self.possibleWord[i][j]] + self.smooth)/(self.smooth*self.unique_words+self.unigram[index-1])
                bigramSmooth2probablity = (self.bigram[self.possibleWord[i][j], wordList[index+1]] + self.smooth)/(self.smooth*self.unique_words+self.unigram[self.possibleWord[i][j]])
                probability[self.possibleWord[i][j]] = bigramSmooth1probablity*bigramSmooth2probablity
            bigramsWithSmoothProbability.append(probability)
        return bigramsWithSmoothProbability



if __name__ == '__main__': 
    start = timeit.default_timer()
    config = CommandLine()
    openFile = openfile(config.args)
    wordTrain = openFile.openTrain()
    queryLine, queryPossibleWord = openFile.openQuery()

    unigram = Unigram(wordTrain, queryPossibleWord)
    bigram = Bigrams(wordTrain, queryPossibleWord, queryLine)
    smooth = 1
    bigram_smooth = BigramsWithSmooth(unigram.unigram, bigram.bigrams, queryPossibleWord, queryLine, smooth)

    result = Result(queryLine,queryPossibleWord, unigram.getUnigramWordProbability(), bigram.bigramWordProbability, bigram_smooth.bigramsWithSmooth)
    
    elapsed = timeit.default_timer() - start
    print('The program take',elapsed,'seconds to complete.')