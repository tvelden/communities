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
OUTPUT_NETWORK_DIRECTORY_FOR_COMPONENTS = ''
OUTPUT_STATISTICS_DIRECTORY_FOR_COMPONENTS = ''
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
    global OUTPUT_NETWORK_DIRECTORY_FOR_COMPONENTS
    global OUTPUT_STATISTICS_DIRECTORY_FOR_COMPONENTS
    
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
    
    OUTPUT_NETWORK_DIRECTORY_FOR_COMPONENTS = OUTPUT_PARENT_DIRECTORY_PATH + '/nwa-' + str(FIELD) + '/' + 'runs/' + str(RUN) + '/output/networks/' + str(TYPE) + str(START_YEAR) + '-' + str(END_YEAR) + '_' + str(SIZE) +'years' + '/components'
    if not os.path.exists(OUTPUT_NETWORK_DIRECTORY_FOR_COMPONENTS):
        os.makedirs(OUTPUT_NETWORK_DIRECTORY_FOR_COMPONENTS)
        print('New directory made: ' + str(OUTPUT_NETWORK_DIRECTORY_FOR_COMPONENTS))

    OUTPUT_STATISTICS_DIRECTORY_FOR_COMPONENTS= OUTPUT_PARENT_DIRECTORY_PATH + '/nwa-' + str(FIELD) + '/' + 'runs/' + str(RUN) + '/output/statistics/' + str(FIELD) + str(RUN) + str(TYPE) + str(START_YEAR) + '-' + str(END_YEAR) + '_' + str(SIZE) + 'years' + '/components'
    if not os.path.exists(OUTPUT_STATISTICS_DIRECTORY_FOR_COMPONENTS):
        os.makedirs(OUTPUT_STATISTICS_DIRECTORY_FOR_COMPONENTS)
        print('New directory made: ' + str(OUTPUT_STATISTICS_DIRECTORY_FOR_COMPONENTS))

def analysis():
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
    global OUTPUT_NETWORK_DIRECTORY_FOR_COMPONENTS
    global OUTPUT_STATISTICS_DIRECTORY_FOR_COMPONENTS
    
    dir = OUTPUT_NETWORK_DIRECTORY_FOR_COMPONENTS
    start = START_YEAR
    end = start + SIZE -1
    pstart = -1
    pend = -1
    fs = OUTPUT_STATISTICS_DIRECTORY_FOR_COMPONENTS + '/' + str(TYPE) + str(start) + '-' + str(end) + '_' + str(SIZE) + 'years-' + 'Large-SecondLargeData.txt'
    f = open(fs,'w')
    f.write('Start_Year; End_year; Size_of_Largest_Component; Number_of_Nodes_From_Second_Larges_Ever; Ever_Second_Percent; Number_from_Just_Previous-Second; Just_Previous_Percent\n')
    while(end<=END_YEAR):
        fs2 = dir + '/' + str(TYPE) + str(start) + '-' + str(end) + '_' + str(SIZE) + 'years-' + 'AccumulatedLargestComponent.txt'
        inp2 = open(fs2, 'r')
        x = inp2.readline()
        ls = int(x[7:len(x)-1])
        #print ls
        count = 0
        count4 = 0
        if(pstart>0):
            fs3 = dir + '/' + str(TYPE) + str(pstart) + '-' + str(pend) + '_' + str(SIZE) + 'years-' + 'AccumulatedSecondLargestComponent.txt'
            #print fs3
            inp3 = open(fs3, 'r')
            psec = []
            for line in inp3:
                if(line[0] == '*'):
                    continue
                psec.append(line[0:len(line)-1])
            inp3.close()
            
            fs4 = dir + '/' + str(TYPE) + str(pstart) + '-' + str(pend) + '_' + str(SIZE) + 'years-' + 'SecondLargestComponent.txt'
            #print fs3
            inp4 = open(fs4, 'r')
            psec4 = []
            for line in inp4:
                if(line[0] == '*'):
                    continue
                psec4.append(line[0:len(line)-1])
            inp4.close()
            
                
            for line in inp2:
                if(line[0] =='*'):
                    continue
                x = line[0:len(line) -1]
                if(x in psec):
                    count = count + 1
                if(x in psec4):
                    count4 = count4 + 1    
        else:
            count = 0
            count4 = 0
        inp2.close()
        f.write(str(start) + '; ' + str(end) + '; '+ str(ls) + '; ' + str(count) + '; ' + str(float(float(count)/float(ls))) + '; ' + str(count4) + '; ' + str(float(float(count4)/float(ls))) +'\n') 
        pstart = start
        pend = end
        end = end + SIZE
    f.close()
if __name__ == "__main__":
    setFilePaths()
    analysis()