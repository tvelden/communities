import os
import sys
import operator
import numpy
import scipy.stats
from operator import itemgetter
import pdb
import networkx as nx
sys.path.append(os.path.realpath('../tna'))
import globalvar
from globalfuncs import *
from analyzer import *


def analysis():
    
    dir = OUTPUT_NETWORK_DIRECTORY_FOR_COMPONENTS
    start = START_YEAR
    end = start + SIZE -1
    pstart = -1
    pend = -1
    fs = OUTPUT_STATISTICS_DIRECTORY_FOR_COMPONENTS + '/' + str(TYPE) + str(start) + '-' + str(end) + '_' + str(SIZE) + 'years-' + 'Large-SecondLargeData.txt'
    f = open(fs,'w')
    f.write('Start_Year; End_year; Size_of_Largest_Component; Number_of_Nodes_From_Second_Largest_Ever; Ever_Second_Percent; Number_from_Just_Previous_Second; Just_Previous_Percent; Number_from_Others; Percent_from_others; Number_From_Previous_Largest; Percent_Previous_Largest; New; Percent_New; Others; Others_Percent\n')
    while(end<=END_YEAR):
        fs2 = dir + '/' + str(TYPE) + str(start) + '-' + str(end) + '_' + str(SIZE) + 'years-' + 'AccumulatedLargestComponent.txt'
        inp2 = open(fs2, 'r')
        x = inp2.readline()
        ls = int(x[7:len(x)-1])
        #print ls
        count = 0
        count4 = 0
        count5 = 0
        count6 = 0
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
            
            fs5 = dir + '/' + str(TYPE) + str(pstart) + '-' + str(pend) + '_' + str(SIZE) + 'years-' + 'OtherComponentsAuthors.txt'
            #print fs3
            inp5 = open(fs5, 'r')
            psec5 = []
            for line in inp5:
                if(line[0] == '*'):
                    continue
                psec5.append(line[0:len(line)-1])
            inp5.close()
                
            fs6 = dir + '/' + str(TYPE) + str(pstart) + '-' + str(pend) + '_' + str(SIZE) + 'years-' + 'AccumulatedLargestComponent.txt'
            #print fs3
            inp6 = open(fs6, 'r')
            psec6 = []
            for line in inp6:
                if(line[0] == '*'):
                    continue
                psec6.append(line[0:len(line)-1])
            inp6.close()
            
            for line in inp2:
                if(line[0] =='*'):
                    continue
                x = line[0:len(line) -1]
                if(x in psec):
                    count = count + 1
                if(x in psec4):
                    count4 = count4 + 1   
                if(x in psec5):
                    count5 = count5 + 1
                if(x in psec6):
                    count6 = count6 + 1
        else:
            count = 0
            count4 = 0
            count5 = 0
            count6 = 0
        inp2.close()
        new = ls- count- count4 - count5 - count6
        ot = count4 + count5
        f.write(str(start) + '; ' + str(end) + '; '+ str(ls) + '; ' + str(count) + '; ' + str(100*float(float(count)/float(ls))) + '; ' + str(count4) + '; ' + str(100*float(float(count4)/float(ls))) + '; ' + str(count5) + '; ' + str(100*float(float(count5)/float(ls))) + '; ' + str(count6) + '; ' + str(100*float(float(count6)/float(ls))) + ';' + str(new) + ';' + str(100*float(float(new)/float(ls)))+ '; ' + str(ot) + '; ' + str(float(float(ot)/float(ls))) +'\n') 
        pstart = start
        pend = end
        end = end + SIZE
    f.close()
if __name__ == "__main__":
    communities_directory = os.path.realpath(os.getcwd() + '/../../..')
    setFilePaths(communities_directory)
    analysis()