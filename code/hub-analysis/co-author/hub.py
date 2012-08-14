import os
import sys
import operator
import numpy
import scipy.stats
from operator import itemgetter
import pdb
import networkx as nx
sys.path.append(os.path.realpath('../../tna'))
import globalvar
from globalfuncs import *
from analyzer import *


def gethub(netfilename, allfilename, hubfilename):
    #allfilename = OUTPUT_NETWORK_DIRECTORY_FOR_PAJEK + '/net_files/' + str(TYPE) + str(START_YEAR) + '-' + str(END_YEAR) + '_' + str(SIZE) + 'years' + 'CoauthorshipNetwork.all.txt'
    #netfilename = OUTPUT_NETWORK_DIRECTORY_FOR_PAJEK + '/net_files/' + str(TYPE) + str(START_YEAR) + '-' + str(END_YEAR) + '_' + str(SIZE) + 'years' + 'CoauthorshipNetwork.net'
    #hubfilename = OUTPUT_NETWORK_DIRECTORY_FOR_PAJEK + '/net_files/' + str(TYPE) + str(START_YEAR) + '-' + str(END_YEAR) + '_' + str(SIZE) + 'years' + 'CoauthorshipNetwork.hub'
    
    #allfilename = OUTPUT_NETWORK_DIRECTORY_FOR_PAJEK + 'CoauthorshipNetwork.all.txt'
    
    netfile = open(netfilename, 'r')
    allfile = open(allfilename, 'r')
    hubfile = open(hubfilename, 'w')
    
    A = {}
    for line in netfile:
        if(line == '*Edges\n'):
            break
        if(line[0] == '*'):
            continue
        n = ''
        i = 0
        while(line[i] != ' '):
            n = n + line[i]
            i = i + 1
        number = int(n)
        i = i + 1
        a = line[i:len(line) -1]
        A[number] = a
    #print A
    
    L = []
    for line in allfile:
        l = len(line)
        l = l - 1
        if(line[l-1] == '5' or line[l-1] == '6' or line[l-1] == '7'):
            i = 0
            s = ''
            while(line[i] != ' '):
                s = s + line[i]
                i = i + 1
            number = int(s)
            L.append(number)
    
    for e in L:
        hubfile.write( str(A[e])+ '\n')
    
    allfile.close()
    netfile.close()
    hubfile.close()
    
if __name__ == "__main__":
    communities_directory = os.path.realpath(os.getcwd() + '/../../..')
    setFilePaths(communities_directory)
    gethub()