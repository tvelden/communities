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


            
def makeComponents():
    fsd = globalvar.OUTPUT_NETWORK_DIRECTORY_FOR_COMPONENTS 
    N = Network()
    
    tot = [] #number of total authors in the all years long chunk
    N.makeCoauthorshipNetworkFromFile(globalvar.INPUT_REDUCED_FILE_PATH)
    for e in N.nodes:
    	tot.append(e)
    
    acc = [] #number of authors up to the year being considered
    
    if(globalvar.TYPE == 'discrete'):
        start = globalvar.START_YEAR
        end = start + globalvar.SIZE -1
        while(end<=globalvar.END_YEAR):
            Partition = Network()
            Partition.makeSubCoauthorshipNetworkFromSuperCoauthorshipNetwork(N, start, end)
            rest = []
            for e in Partition.nodes:
            	if e not in acc:
            		acc.append(e)
            
            for e in tot:
            	if e not in acc:
            		rest.append(e)
            fsd2 = fsd + '/' + str(start) + '-' + str(end)  + '/components/pajek' 
            if not os.path.exists(fsd2):
            	os.makedirs(fsd2)
            fs = fsd2 + '/' + str(globalvar.FIELD) + str(globalvar.RUN) + '_' + str(globalvar.TYPE) + str(start) + '-' + str(end) + '_' + str(globalvar.SIZE) + 'years_unborn.net'
            frest = open(fs, 'w')
            frest.write('*Number of unborn authors:'+ str(len(rest)) + '\n')
            for e in rest:
            	frest.write(str(e)+ '\n')
            frest.close()
            Partition.printNetworkComponents(globalvar.FIELD, globalvar.RUN, globalvar.TYPE, globalvar.SIZE, globalvar.OUTPUT_NETWORK_DIRECTORY_FOR_COMPONENTS)
            start = end + 1
            end = end + globalvar.SIZE
    elif(globalvar.TYPE == 'accumulative'):
        start = globalvar.START_YEAR
        end = start + globalvar.SIZE -1
        while(end<=globalvar.END_YEAR):
            Partition = Network()
            Partition.makeSubCoauthorshipNetworkFromSuperCoauthorshipNetwork(N, start, end)
            rest = []
            for e in Partition.nodes:
            	if e not in acc:
            		acc.append(e)
            for e in tot:
            	if e not in acc:
            		rest.append(e)
            fsd2 = fsd + '/' + str(start) + '-' + str(end)  + '/components/pajek' 
            if not os.path.exists(fsd2):
            	os.makedirs(fsd2)
            fs = fsd2 + '/' + str(globalvar.FIELD) + str(globalvar.RUN) + '_' + str(globalvar.TYPE) + str(start) + '-' + str(end) + '_' + str(globalvar.SIZE) + 'years_unborn.net'
            frest = open(fs, 'w')
            frest.write('*Number of unborn authors:'+ str(len(rest)) + '\n')
            for e in rest:
            	frest.write(str(e)+ '\n')
            frest.close()
            Partition.printNetworkComponents(globalvar.FIELD, globalvar.RUN, globalvar.TYPE, globalvar.SIZE, globalvar.OUTPUT_NETWORK_DIRECTORY_FOR_COMPONENTS)
            end = end + globalvar.SIZE
    elif(globalvar.TYPE == 'sliding'):
        start = globalvar.START_YEAR
        end = start + globalvar.SIZE -1
        while(end<=globalvar.END_YEAR):
            Partition = Network()
            Partition.makeSubCoauthorshipNetworkFromSuperCoauthorshipNetwork(N, start, end)
            rest = []
            for e in Partition.nodes:
            	if e not in acc:
            		acc.append(e)
            for e in tot:
            	if e not in acc:
            		rest.append(e)
            fsd2 = fsd + '/' + str(start) + '-' + str(end)  + '/components/pajek' 
            if not os.path.exists(fsd2):
            	os.makedirs(fsd2)
            fs = fsd2 + '/' + str(globalvar.FIELD) + str(globalvar.RUN) + '_' + str(globalvar.TYPE) + str(start) + '-' + str(end) + '_' + str(globalvar.SIZE) + 'years_unborn.net'
            frest = open(fs, 'w')
            frest.write('*Number of unborn authors:'+ str(len(rest)) + '\n')
            for e in rest:
            	frest.write(str(e)+ '\n')
            frest.close()
            Partition.printNetworkComponents(globalvar.FIELD, globalvar.RUN, globalvar.TYPE, globalvar.SIZE, globalvar.OUTPUT_NETWORK_DIRECTORY_FOR_COMPONENTS)
            start = start + 1
            end = end + 1


if __name__ == "__main__":
    communities_directory = os.path.realpath(os.getcwd() + '/../../..')
    setFilePaths(communities_directory)
    makeComponents()