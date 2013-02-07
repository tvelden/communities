import os
import sys
import operator
import numpy
import scipy.stats
from operator import itemgetter
import pdb
import networkx as nx
import glob

        
def rearrange(filename):
    #path = OUTPUT_NETWORK_DIRECTORY_FOR_PAJEK + '/net_files/'
    #for filename in glob.glob(os.path.join(path, '*.net')):
    print filename
    l = len(filename)
            
    A = []
    index = 0
    file = open(filename, 'r')
    for line in file:
        if(index ==0):
            index = index + 1
            continue
        if(line == '*Edges\n'):
            break
        i = 0
        while(line[i]!= ' '):
            i = i + 1
        name = line[i+1:len(line)-1]
        A.append(name)
        
    i = len(filename) - 1
    while(filename[i] != '.'):
        i = i - 1
    treefilename = filename[0:i] + '.tree'
    treefile = open(treefilename, 'r')
    S = {}
    for line in treefile:
        i = 0
        while(line[i] != ' '):
                i = i + 1
        i = i + 1
        while(line[i] != ' '):
                i = i + 1
        i = i + 1
        s = line[i:len(line)-1]
        s0 = line[0:i]
        S[s] = s0
    treefile.close()
        
    i = len(filename) - 1
    while(filename[i] != '.'):
        i = i - 1
    clusterfilename = filename[0:i] + '.clu'
    print clusterfilename
    clusterfile = open(clusterfilename, 'w')
    clusterfile.write('# Code length 2.98541 in 669 modules.\n')
    for e in A:
        t = str(S[e])
        i = 0
        ts = ''
        while(t[i] != ':'):
            ts = ts + t[i]
            i = i + 1
            
        clusterfile.write(str(ts) + '\n')
    clusterfile.close()
    
if __name__ == "__main__":
    rearrange(sys.argv[1])
    