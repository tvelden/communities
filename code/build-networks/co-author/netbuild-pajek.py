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

def makeCoauthorshipNetworkFilesForPajek():
    
    #output_directory = OUTPUT_NETWORK_DIRECTORY_FOR_PAJEK + '/' + 
    N = Network()
    N.makeCoauthorshipNetworkFromFile(globalvar.INPUT_REDUCED_FILE_PATH)
    if(globalvar.TYPE == 'discrete'):
        start = globalvar.START_YEAR
        end = start + globalvar.SIZE -1
        while(end<=globalvar.END_YEAR):
            Partition = Network()
            Partition.makeSubCoauthorshipNetworkFromSuperCoauthorshipNetwork(N, start, end)
            print 'printing network ...'
            print start, end, globalvar.FIELD, globalvar.RUN, globalvar.TYPE, globalvar.SIZE, globalvar.OUTPUT_NETWORK_DIRECTORY_FOR_PAJEK
            Partition.printNetworkForPajek(globalvar.FIELD, globalvar.RUN, globalvar.TYPE, globalvar.SIZE, globalvar.OUTPUT_NETWORK_DIRECTORY_FOR_PAJEK)
            start = end + 1
            end = end + globalvar.SIZE
    elif(globalvar.TYPE == 'accumulative'):
        start = globalvar.START_YEAR
        end = start + globalvar.SIZE -1
        while(end<=globalvar.END_YEAR):
            Partition = Network()
            Partition.makeSubCoauthorshipNetworkFromSuperCoauthorshipNetwork(N, start, end)
            print 'printing network ...'
            print start, end, globalvar.FIELD, globalvar.RUN, globalvar.TYPE, globalvar.SIZE
            Partition.printNetworkForPajek(globalvar.FIELD, globalvar.RUN, globalvar.TYPE, globalvar.SIZE, globalvar.OUTPUT_NETWORK_DIRECTORY_FOR_PAJEK)
            end = end + globalvar.SIZE
    elif(globalvar.TYPE == 'sliding'):
        start = globalvar.START_YEAR
        end = start + globalvar.SIZE -1
        while(end<=globalvar.END_YEAR):
            Partition = Network()
            Partition.makeSubCoauthorshipNetworkFromSuperCoauthorshipNetwork(N, start, end)
            print 'printing network ...'
            print start, end, globalvar.FIELD, globalvar.RUN, globalvar.TYPE, globalvar.SIZE
            Partition.printNetworkForPajek(globalvar.FIELD, globalvar.RUN, globalvar.TYPE, globalvar.SIZE, globalvar.OUTPUT_NETWORK_DIRECTORY_FOR_PAJEK)
            start = start + 1
            end = end + 1
            


if __name__ == "__main__":
    communities_directory = os.path.realpath(os.getcwd() + '/../../..')
    setFilePaths(communities_directory)
    makeCoauthorshipNetworkFilesForPajek()
