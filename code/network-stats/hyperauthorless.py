import os
import sys
import operator
import math
import numpy
import scipy.stats
from operator import itemgetter
import pdb
import networkx as nx
sys.path.append(os.path.realpath('../tna'))
import globalvar
from globalfuncs import *
from analyzer import *


def makeHyperAuthorlessAuthorDistributionAmongPapersFile():
    print 'Gathering data for Author distribution among the papers in entire network ...'
    directoryPath = globalvar.OUTPUT_STATISTICS_DIRECTORY + '/allyears/whole_net/tables' 
    if not os.path.exists(directoryPath):
            os.makedirs(directoryPath)
            print('New directory made: ' + str(directoryPath))
    print directoryPath
    #Mfile = directoryPath + '/'+ str(globalvar.FIELD) + str(globalvar.RUN) + '_' + str(globalvar.TYPE) + str(globalvar.START_YEAR) + '-' + str(globalvar.END_YEAR) + '_' + str(globalvar.SIZE) + 'years_wholenet_HyperAuthorlessAuthorDistribution.csv'
    Sfile = directoryPath + '/'+ str(globalvar.FIELD) + str(globalvar.RUN) + '_' + str(globalvar.TYPE) + str(globalvar.START_YEAR) + '-' + str(globalvar.END_YEAR) + '_' + str(globalvar.SIZE) + 'years_wholenet_SignificantPapers.csv'
    #MF = open(Mfile, 'w')
    SF = open(Sfile, 'w')
    #MF.write('No_of_Authors; Frequency_of_Papers \n')
    N = Network()
    N.makeCoauthorshipNetworkFromFile(globalvar.INPUT_REDUCED_FILE_PATH)
    X = N.getAuthorDistributionAmongPapers()
    # for x in X:
#     	print x,X[x][0]
#     print '***********'
    ind = -1
    V = []
    for k in X:
        for e in X[k][1]:
          V.append(k)
          ind = ind + 1

    if(ind%2 == 0):
        med = ind /2
    else:
        med = (ind + 1) /2
        
    V.sort() 
    median = V[med]
    print('Median =  ' + str(median))
    dev = []
    for i in range(0,ind+1):
        dev.append(abs(V[i]-median))
        #print dev[i]
        
#     print '############'
#     for i in range(0,ind+1):
#     	print V[i], dev[i]
#     print '############'
#     
    tdev = []
    for e in dev:
    	tdev.append(e)
    tdev.sort()
    devmedian = tdev[med]
    
    
    print('Median deviation from the Median is: ' + str(devmedian))
    print 'The frequency and deviation/median_deviation values are:'
    ratio = []
    for i in range(0,ind+1):
        ratio.append(float(dev[i])/float(devmedian))
    Y = {}
    for i in range(0, ind + 1):
        Y[V[i]] = ratio[i]
    for y in Y:
    	print y, X[y][0], Y[y]
    threshold = input('Please input the Threshold value: ')
    SP = []
    for k in X:
        #print k, X[k]
        if(k ==0):
            continue
        if(Y[k]<=threshold):
            for e in X[k][1]:
            	if e not in SP:
            		SP.append(e)
    for p in SP:
        SF.write(str(p) + '\n')
    SF.close()
    print 'Finished gathering data for Author distribution!!'


def makeHyperAuthorshipLessNetwork():
    print 'Making HyperAuthor Free Network ...'
    
    directoryPath = globalvar.OUTPUT_STATISTICS_DIRECTORY + '/allyears/whole_net/tables'
    
    print directoryPath
    
    if not os.path.exists(directoryPath):
        os.makedirs(directoryPath)
        print('New directory made: ' + str(directoryPath))
    
    Sfile = os.path.realpath(directoryPath + '/'+ str(globalvar.FIELD) + str(globalvar.RUN) + '_' + str(globalvar.TYPE) + str(globalvar.START_YEAR) + '-' + str(globalvar.END_YEAR) + '_' + str(globalvar.SIZE) + 'years_wholenet_SignificantPapers.csv')
    Ofile = os.path.realpath(directoryPath + '/'+ str(globalvar.FIELD) + str(globalvar.RUN) + '_' + str(globalvar.TYPE) + str(globalvar.START_YEAR) + '-' + str(globalvar.END_YEAR) + '_' + str(globalvar.SIZE) + 'years_wholenet_HyperAuthorLessInput.txt')
    
    N = Network()
    N.makeCoauthorshipNetworkFromFile(globalvar.INPUT_REDUCED_FILE_PATH)
    N.removeHyperAuthorshipPapers(Sfile, Ofile)
    

if __name__ == "__main__":
    communities_directory = os.path.realpath(os.getcwd() + '/../..')
    setFilePaths(communities_directory)
    makeHyperAuthorlessAuthorDistributionAmongPapersFile()
    makeHyperAuthorshipLessNetwork()