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


def makeHubGraphR(L, hubfilename):
	V = {}
	for e in L:
		if(e[1] in V):
			V[e[1]] = V[e[1]] + 1
		else:
			V[e[1]] = 1
	hubmil = open(os.path.dirname(hubfilename) + '/' + str(globalvar.FIELD) + str(globalvar.RUN) + '_' + 'hub_milojevich.txt', 'w')
	hubmil.write('coauthor;frequency\n')
	for e in V:
		hubmil.write(str(e) + ';' + str(V[e]) + '\n')
	hubmil.close()
	
	

def gethub(netfilename, allfilename):
    #allfilename = OUTPUT_NETWORK_DIRECTORY_FOR_PAJEK + '/net_files/' + str(TYPE) + str(START_YEAR) + '-' + str(END_YEAR) + '_' + str(SIZE) + 'years' + 'CoauthorshipNetwork.all.txt'
    #netfilename = OUTPUT_NETWORK_DIRECTORY_FOR_PAJEK + '/net_files/' + str(TYPE) + str(START_YEAR) + '-' + str(END_YEAR) + '_' + str(SIZE) + 'years' + 'CoauthorshipNetwork.net'
    #hubfilename = OUTPUT_NETWORK_DIRECTORY_FOR_PAJEK + '/net_files/' + str(TYPE) + str(START_YEAR) + '-' + str(END_YEAR) + '_' + str(SIZE) + 'years' + 'CoauthorshipNetwork.hub'
    
    #allfilename = OUTPUT_NETWORK_DIRECTORY_FOR_PAJEK + 'CoauthorshipNetwork.all.txt'
    
    netfile = open(netfilename, 'r')
    allfile = open(allfilename, 'r')
    hubfilename = os.path.dirname(allfilename) + '/../../../allyears/whole_net/' + str(globalvar.FIELD) + str(globalvar.RUN) + '_' + 'hublist.txt'
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
    
    N = Network()
    L1 = {}
    N.makeCoauthorshipNetworkFromFile(globalvar.INPUT_REDUCED_FILE_PATH)
    for e in L:
    	L1[A[e][1:len(A[e])-1]] = N.differentDegrees[A[e][1:len(A[e])-1]][0]
    L2 = sorted(L1.iteritems(), key = operator.itemgetter(1))
    #print L2
    for element in L2:
    	hubfile.write(str(element[0]) + '\n')
    makeHubGraphR(L2, hubfilename)
    allfile.close()
    netfile.close()
    hubfile.close()
    
if __name__ == "__main__":
    communities_directory = os.path.realpath(os.getcwd() + '/../../..')
    setFilePaths(communities_directory)
    gethub(sys.argv[1], sys.argv[2])
