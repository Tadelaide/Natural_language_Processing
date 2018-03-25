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
        print(args)
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
        self.readfile()

    def readfile(self):
        with open(self.file,'r') as infile:
            simaple = infile.read()
        print(simaple)

if __name__ =='__main__':
    start = timeit.default_timer()
    config = CommandLine()
    openfile(config.args[1])
  
    