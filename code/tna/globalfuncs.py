import os
import sys
import operator
import numpy
import scipy.stats
from operator import itemgetter
import pdb
import networkx as nx
import globalvar

def setFilePaths():
    communities_directory = os.path.realpath('../..')
    #print communities_directory
    parameterfile = open(globalvar.RELATIVE_INPUT_PARAMETER_FILE, 'r')
    for line in parameterfile:
        l = len(line)
        #print line[0:10]
        if(line[0:6] == 'FIELD='):
            globalvar.FIELD= line[6:(l-1)]
            print globalvar.FIELD
        elif(line[0:4] == 'RUN='):
            globalvar.RUN = line[4:(l-1)]
            print globalvar.RUN
        elif(line[0:11] == 'START_YEAR='):
            globalvar.START_YEAR = int(line[11:(l-1)])
            print globalvar.START_YEAR
        elif(line[0:9] == 'END_YEAR='):
            globalvar.END_YEAR = int(line[9:(l-1)])
            print globalvar.END_YEAR
        elif(line[0:5] == 'TYPE='):
            globalvar.TYPE = line[5:(l-1)]
            print globalvar.TYPE
        elif(line[0:5] == 'SIZE='):
            globalvar.SIZE = int(line[5:(l-1)])
            print globalvar.SIZE
        elif(line[0:9] == 'NET_PATH='):
            globalvar.OUTPUT_PARENT_DIRECTORY_PATH = os.path.realpath(communities_directory + '/../' + line[9:(len(line)-1)])
            print globalvar.OUTPUT_PARENT_DIRECTORY_PATH
        elif(line[0:10] == 'DATA_PATH='):
            globalvar.INPUT_REDUCED_FILE_PATH = str(os.path.realpath(globalvar.OUTPUT_PARENT_DIRECTORY_PATH + '/nwa-' + str(globalvar.FIELD) + '/' + 'data/' + line[10:(len(line)-1)]))
            print globalvar.INPUT_REDUCED_FILE_PATH

    globalvar.OUTPUT_NETWORK_DIRECTORY_FOR_PAJEK = str(os.path.realpath(globalvar.OUTPUT_PARENT_DIRECTORY_PATH + '/nwa-' + str(globalvar.FIELD) + '/' + 'runs/' + str(globalvar.RUN) + '/output/networks/' + str(globalvar.TYPE) + '_' + str(globalvar.START_YEAR) + '-' + str(globalvar.END_YEAR) + '_' + str(globalvar.SIZE) +'years' + '/generic'))
    if not os.path.exists(globalvar.OUTPUT_NETWORK_DIRECTORY_FOR_PAJEK):
        os.makedirs(globalvar.OUTPUT_NETWORK_DIRECTORY_FOR_PAJEK)
        print('New directory made: ' + str(globalvar.OUTPUT_NETWORK_DIRECTORY_FOR_PAJEK))
    
    globalvar.OUTPUT_NETWORK_DIRECTORY_FOR_COMPONENTS = str(os.path.realpath(globalvar.OUTPUT_PARENT_DIRECTORY_PATH + '/nwa-' + str(globalvar.FIELD) + '/' + 'runs/' + str(globalvar.RUN) + '/output/networks/' + str(globalvar.TYPE)  + '_' +str(globalvar.START_YEAR) + '-' + str(globalvar.END_YEAR) + '_' + str(globalvar.SIZE) +'years' + '/generic'))
    if not os.path.exists(globalvar.OUTPUT_NETWORK_DIRECTORY_FOR_COMPONENTS):
        os.makedirs(globalvar.OUTPUT_NETWORK_DIRECTORY_FOR_COMPONENTS)
        print('New directory made: ' + str(globalvar.OUTPUT_NETWORK_DIRECTORY_FOR_COMPONENTS))
        
    globalvar.OUTPUT_STATISTICS_DIRECTORY = str(os.path.realpath(globalvar.OUTPUT_PARENT_DIRECTORY_PATH + '/nwa-' + str(globalvar.FIELD) + '/' + 'runs/' + str(globalvar.RUN) + '/output/statistics/' + str(globalvar.TYPE) + '_' + str(globalvar.START_YEAR) + '-' + str(globalvar.END_YEAR) + '_' + str(globalvar.SIZE) +'years' + '/generic'))
    if not os.path.exists(globalvar.OUTPUT_STATISTICS_DIRECTORY):
        os.makedirs(globalvar.OUTPUT_STATISTICS_DIRECTORY)
        print('New directory made: ' + str(globalvar.OUTPUT_STATISTICS_DIRECTORY))
        
        