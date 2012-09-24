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


def analysis():
    
    dir = globalvar.OUTPUT_NETWORK_DIRECTORY_FOR_COMPONENTS 
    start = globalvar.START_YEAR
    end = start + globalvar.SIZE -1
    pstart = -1
    pend = -1
    #for later use
    ffs = globalvar.OUTPUT_STATISTICS_DIRECTORY_FOR_COMPONENTS + '/allyears/components/images'
    if not os.path.exists(ffs):
        os.makedirs(ffs)
        print('New directory made: ' + str(ffs))
    #for using in this code
    ffs = globalvar.OUTPUT_STATISTICS_DIRECTORY_FOR_COMPONENTS + '/allyears/components/tables'
    if not os.path.exists(ffs):
        os.makedirs(ffs)
        print('New directory made: ' + str(ffs))
    fs =  ffs + '/' + str(globalvar.FIELD) + str(globalvar.RUN)+ '_' + str(globalvar.TYPE) + str(globalvar.START_YEAR) + '-' + str(globalvar.END_YEAR) + '_' + str(globalvar.SIZE) + 'years_' + 'Large-SecondLargeData.csv'
    f = open(fs,'w')
    f.write('Start_Year; End_year; Size_of_Largest_Component; Number_of_Nodes_From_Second_Largest_Ever; Ever_Second_Percent; Number_from_Just_Previous_Second; Just_Previous_Percent; Number_from_Others; Percent_from_others; Number_From_Previous_Largest; Percent_Previous_Largest; New; Percent_New\n')
    S = []
    while(end<=globalvar.END_YEAR):
    	dir1 = dir + '/' + str(start) + '-' + str(end) + '/components/pajek'
        fs2 = dir1 + '/' + str(globalvar.FIELD) + str(globalvar.RUN) + '_' + str(globalvar.TYPE) + str(start) + '-' + str(end) + '_' + str(globalvar.SIZE) + 'years_' + 'LargestComponent.net'
        inp2 = open(fs2, 'r')
        x = inp2.readline()
        ls = int(x[6:len(x)-1])
        inp2.close()
        #print ls
        count = 0
        count4 = 0
        count5 = 0
        count6 = 0
        new = 0
        if(pstart>0):
        	dir1 = dir + '/' + str(pstart) + '-' + str(pend) + '/components/pajek'
        	fs3 = dir1 + '/' + str(globalvar.FIELD) + str(globalvar.RUN)+ '_' + str(globalvar.TYPE)  + str(pstart) + '-' + str(pend) + '_' + str(globalvar.SIZE) + 'years_' + 'LargestComponent.net'
            #print fs3
        	inp3 = open(fs3, 'r')
        	psec = []
        	for line in inp3:
        		#print line[0:len(line)-1]
        		if(line[0] != '*'):
        				psec.append(line[0:len(line)-1])
        	#print len(psec)
        	inp3.close()
        	#print 'here is prev:'
        	#print(str(pstart) + '-' + str(pend))
        	#print psec
            
        	fs4 = dir1 + '/'+ str(globalvar.FIELD) + str(globalvar.RUN)+ '_' + str(globalvar.TYPE) + str(pstart) + '-' + str(pend) + '_' + str(globalvar.SIZE) + 'years_' + 'SecondLargestComponent.net'
        	#print fs3
        	inp4 = open(fs4, 'r')
        	psec4 = []
        	for line in inp4:
        		if(line[0] == '*'):
        			continue
        		au = line[0:len(line)-1]
        		psec4.append(au)
        		if(au not in S):
        			S.append(au)
        	inp4.close()
            
        	fs5 = dir1 + '/'+ str(globalvar.FIELD) + str(globalvar.RUN)+ '_' + str(globalvar.TYPE) + str(pstart) + '-' + str(pend) + '_' + str(globalvar.SIZE) + 'years_' + 'OtherComponents.net'
            #print fs3
        	inp5 = open(fs5, 'r')
        	psec5 = []
        	for line in inp5:
        		if(line[0] == '*'):
        			continue
        		psec5.append(line[0:len(line)-1])
        	inp5.close()
            
        	inp2 = open(fs2, 'r')
        	for line in inp2:
        		if(line[0] =='*'):
        			continue
        		x = line[0:len(line) -1]
        		if(x in S):
        			count = count + 1
        		if(x in psec4):
        			count4 = count4 + 1   
        		if(x in psec5):
        			count5 = count5 + 1
        		if(x in psec):
        			count6 = count6 + 1
        		if((x not in S) and (x not in psec) and (x not in psec5)):
        			new = new + 1
        	inp2.close()
        else:
        	count = 0
        	count4 = 0
        	count5 = 0
        	count6 = 0
        	new = 0
        #new = ls- count- count4 - count5 - count6
        f.write(str(start) + '; ' + str(end) + '; '+ str(ls) + '; ' + str(count) + '; ' + str(100*float(float(count)/float(ls))) + '; ' + str(count4) + '; ' + str(100*float(float(count4)/float(ls))) + '; ' + str(count5) + '; ' + str(100*float(float(count5)/float(ls))) + '; ' + str(count6) + '; ' + str(100*float(float(count6)/float(ls))) + ';' + str(new) + ';' + str(100*float(float(new)/float(ls))) +'\n') 
        pstart = start
        pend = end
        if(globalvar.TYPE == 'discrete'):
        	start = start + globalvar.SIZE
        	end = end + globalvar.SIZE
        elif(globalvar.TYPE == 'accumulative'):
        	end = end + globalvar.SIZE
        else:
        	start = start + 1
        	end = start + globalvar.SIZE
    f.close()
if __name__ == "__main__":
    communities_directory = os.path.realpath(os.getcwd() + '/../../..')
    setFilePaths(communities_directory)
    analysis()