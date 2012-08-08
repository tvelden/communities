import os
import sys
import operator
import numpy
import scipy.stats
from operator import itemgetter
import pdb
import networkx as nx



#--Global Variables--
RELATIVE_INPUT_PARAMETER_FILE = '../../../parameters/parameters-global.txt'
INPUT_PARAMETER_FILE = ''
INPUT_ORIGINAL_FILE_PATH = ''
INPUT_REDUCED_FILE_PATH = ''
OUTPUT_PARENT_DIRECTORY_PATH = ''
OUTPUT_NETWORK_DIRECTORY_FOR_PAJEK = ''
OUTPUT_STATISTICS_DIRECTORY = ''
FIELD = ''
RUN = ''
START_YEAR = 0
END_YEAR = 0
TYPE = ''
SIZE = 0

def setFilePaths():
    global INPUT_PARAMETER_FILE 
    global RELATIVE_INPUT_PARAMETER_FILE
    global FIELD
    global RUN
    global SIZE
    global TYPE
    global START_YEAR
    global END_YEAR
    global INPUT_REDUCED_FILE_PATH
    global OUTPUT_NETWORK_DIRECTORY_FOR_PAJEK
    global OUTPUT_STATISTICS_DIRECTORY
    global OUTPUT_PARENT_DIRECTORY_PATH
    

    communities_directory = '../../..' 
    parameterfile = open(RELATIVE_INPUT_PARAMETER_FILE, 'r')
    for line in parameterfile:
        l = len(line)
        #print line[0:10]
        if(line[0:6] == 'FIELD='):
            FIELD= line[6:(l-1)]
            print FIELD
        elif(line[0:4] == 'RUN='):
            RUN = line[4:(l-1)]
            print RUN
        elif(line[0:11] == 'START_YEAR='):
            START_YEAR = int(line[11:(l-1)])
            print START_YEAR
        elif(line[0:9] == 'END_YEAR='):
            END_YEAR = int(line[9:(l-1)])
            print END_YEAR
        elif(line[0:5] == 'TYPE='):
            TYPE = line[5:(l-1)]
            print TYPE
        elif(line[0:5] == 'SIZE='):
            SIZE = int(line[5:(l-1)])
            print SIZE
        elif(line[0:9] == 'NET_PATH='):
            OUTPUT_PARENT_DIRECTORY_PATH = communities_directory + '/' + line[9:(len(line)-1)]
            print OUTPUT_PARENT_DIRECTORY_PATH
        elif(line[0:10] == 'DATA_PATH='):
            INPUT_REDUCED_FILE_PATH = OUTPUT_PARENT_DIRECTORY_PATH + '/' + 'nwa-' + str(FIELD) + '/' + 'data/' + line[10:(len(line)-1)]
            print INPUT_REDUCED_FILE_PATH

    OUTPUT_NETWORK_DIRECTORY_FOR_PAJEK = OUTPUT_PARENT_DIRECTORY_PATH + '/nwa-' + str(FIELD) + '/' + 'runs/' + str(RUN) + '/output/networks/' + str(TYPE) + str(START_YEAR) + '-' + str(END_YEAR) + '_' + str(SIZE) +'years' + '/whole_net/pajek'
    if not os.path.exists(OUTPUT_NETWORK_DIRECTORY_FOR_PAJEK):
        os.makedirs(OUTPUT_NETWORK_DIRECTORY_FOR_PAJEK)
        print('New directory made: ' + str(OUTPUT_NETWORK_DIRECTORY_FOR_PAJEK))
    
    #OUTPUT_STATISTICS_DIRECTORY = OUTPUT_PARENT_DIRECTORY_PATH + '/nwa-' + str(FIELD) + '/' + 'runs/' + str(RUN) + '/output/statistics/' + str(FIELD) + str(RUN) + str(TYPE) + str(START_YEAR) + '-' + str(END_YEAR) + '_' + str(SIZE) + 'years-statistics_files'
    #if not os.path.exists(OUTPUT_STATISTICS_DIRECTORY):
        #os.makedirs(OUTPUT_STATISTICS_DIRECTORY)
        #print('New directory made: ' + str(OUTPUT_STATISTICS_DIRECTORY))


def gethub():
    allfilename = OUTPUT_NETWORK_DIRECTORY_FOR_PAJEK + '/net_files/' + str(TYPE) + str(START_YEAR) + '-' + str(END_YEAR) + '_' + str(SIZE) + 'years' + 'CoauthorshipNetwork.all.txt'
    netfilename = OUTPUT_NETWORK_DIRECTORY_FOR_PAJEK + '/net_files/' + str(TYPE) + str(START_YEAR) + '-' + str(END_YEAR) + '_' + str(SIZE) + 'years' + 'CoauthorshipNetwork.net'
    hubfilename = OUTPUT_NETWORK_DIRECTORY_FOR_PAJEK + '/net_files/' + str(TYPE) + str(START_YEAR) + '-' + str(END_YEAR) + '_' + str(SIZE) + 'years' + 'CoauthorshipNetwork.hub'
    
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
    setFilePaths()
    gethub()