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

def makeComponents2(ws):

	globalvar.SIZE = ws

	fsd = globalvar.OUTPUT_NETWORK_DIRECTORY_FOR_COMPONENTS 
	N = Network()
	
	tot = [] #number of total authors in the all years long chunk
	N.makeCoauthorshipNetworkFromFile(globalvar.INPUT_REDUCED_FILE_PATH)
	for e in N.nodes:
		tot.append(e)
	
	acc = [] #number of authors up to the year being considered
	totA = []
	
	
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
			
			
			com = fsd2 + '/' + str(globalvar.FIELD) + str(globalvar.RUN) + '_' + str(globalvar.TYPE) + str(start) + '-' + str(end) + '_' + str(globalvar.SIZE) + 'years_components.net'
			fcom = open(com, 'r')
			totl = 0
			for line in fcom:
				if (line[0:len('Number of Vertices:')] == 'Number of Vertices:'):
					totl = int(line[len('Number of Vertices:'):len(line)-1])
					break
			#print totl
			
			lsz = 0
			lar = fsd2 + '/' + str(globalvar.FIELD) + str(globalvar.RUN) + '_' + str(globalvar.TYPE) + str(start) + '-' + str(end) + '_' + str(globalvar.SIZE) + 'years_LargestComponent.net'
			flar = open(lar, 'r')
			for line in flar:
				if (line[0:len('*Size:')] == '*Size:'):
					lsz = int(line[len('*Size:'):len(line)-1])
					break
			#print lsz
			totA.append((start,end,100.0*float(lsz)/float(totl)))
			
			fcom.close()
			flar.close()
			start = end + 1
			end = end + globalvar.SIZE
		print totA		
		largest = fsd + '/' + str(globalvar.FIELD) + str(globalvar.RUN) + '_' + str(globalvar.TYPE) + str(globalvar.START_YEAR) + '-' + str(globalvar.END_YEAR) + '_' + str(globalvar.SIZE) + 'years_LargestGrowth.csv'
		flargest = open(largest, 'w') 
		flargest.write('Start_Year; End_Year; Percent\n')
		for e in totA:
			flargest.write(str(e[0]) + '; ' + str(e[1]) + '; ' + str(e[2]) + '\n')
		flargest.close()

		
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

def setFilePaths2(communities_directory, ws):
    communities_directory =  os.path.realpath(communities_directory)
    print communities_directory
    globalvar.RELATIVE_INPUT_PARAMETER_FILE = os.path.realpath(communities_directory +'/parameters/parameters-global.txt')
    print globalvar.RELATIVE_INPUT_PARAMETER_FILE
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
            globalvar.SIZE = ws
            print globalvar.SIZE
        elif(line[0:9] == 'NET_PATH='):
            globalvar.OUTPUT_PARENT_DIRECTORY_PATH = str(os.path.realpath(communities_directory + '/' + line[9:(len(line)-1)]))
            print globalvar.OUTPUT_PARENT_DIRECTORY_PATH
        elif(line[0:10] == 'DATA_PATH='):
            globalvar.INPUT_REDUCED_FILE_PATH = os.path.realpath(globalvar.OUTPUT_PARENT_DIRECTORY_PATH + '/nwa-' + str(globalvar.FIELD) + '/data/' + line[10:(len(line)-1)])
            print globalvar.INPUT_REDUCED_FILE_PATH
        
    globalvar.OUTPUT_NETWORK_DIRECTORY_FOR_PAJEK = str(os.path.realpath(globalvar.OUTPUT_PARENT_DIRECTORY_PATH + '/nwa-' + str(globalvar.FIELD) + '/' + 'runs/' + str(globalvar.RUN) + '/output/networks/' + str(globalvar.TYPE) + str(globalvar.START_YEAR) + '-' + str(globalvar.END_YEAR) + '_' + str(globalvar.SIZE) +'years' + '/generic'))
    if not os.path.exists(globalvar.OUTPUT_NETWORK_DIRECTORY_FOR_PAJEK):
        print globalvar.OUTPUT_NETWORK_DIRECTORY_FOR_PAJEK
        os.makedirs(globalvar.OUTPUT_NETWORK_DIRECTORY_FOR_PAJEK)
        print('New directory made: ' + str(globalvar.OUTPUT_NETWORK_DIRECTORY_FOR_PAJEK))
    
    globalvar.OUTPUT_NETWORK_DIRECTORY_FOR_COMPONENTS = str(os.path.realpath(globalvar.OUTPUT_PARENT_DIRECTORY_PATH + '/nwa-' + str(globalvar.FIELD) + '/' + 'runs/' + str(globalvar.RUN) + '/output/networks/' + str(globalvar.TYPE) +str(globalvar.START_YEAR) + '-' + str(globalvar.END_YEAR) + '_' + str(globalvar.SIZE) +'years' + '/generic'))
    if not os.path.exists(globalvar.OUTPUT_NETWORK_DIRECTORY_FOR_COMPONENTS):
        os.makedirs(globalvar.OUTPUT_NETWORK_DIRECTORY_FOR_COMPONENTS)
        print('New directory made: ' + str(globalvar.OUTPUT_NETWORK_DIRECTORY_FOR_COMPONENTS))
        
    globalvar.OUTPUT_STATISTICS_DIRECTORY = str(os.path.realpath(globalvar.OUTPUT_PARENT_DIRECTORY_PATH + '/nwa-' + str(globalvar.FIELD) + '/' + 'runs/' + str(globalvar.RUN) + '/output/statistics/' + str(globalvar.TYPE) + str(globalvar.START_YEAR) + '-' + str(globalvar.END_YEAR) + '_' + str(globalvar.SIZE) +'years' + '/generic'))
    if not os.path.exists(globalvar.OUTPUT_STATISTICS_DIRECTORY):
        os.makedirs(globalvar.OUTPUT_STATISTICS_DIRECTORY)
        print('New directory made: ' + str(globalvar.OUTPUT_STATISTICS_DIRECTORY))
    
    globalvar.OUTPUT_STATISTICS_DIRECTORY_FOR_COMPONENTS = str(os.path.realpath(globalvar.OUTPUT_PARENT_DIRECTORY_PATH + '/nwa-' + str(globalvar.FIELD) + '/' + 'runs/' + str(globalvar.RUN) + '/output/statistics/' + str(globalvar.TYPE) + str(globalvar.START_YEAR) + '-' + str(globalvar.END_YEAR) + '_' + str(globalvar.SIZE) +'years' + '/generic'))
    if not os.path.exists(globalvar.OUTPUT_STATISTICS_DIRECTORY_FOR_COMPONENTS):
        os.makedirs(globalvar.OUTPUT_STATISTICS_DIRECTORY_FOR_COMPONENTS)
        print('New directory made: ' + str(globalvar.OUTPUT_STATISTICS_DIRECTORY_FOR_COMPONENTS))
        
 

if __name__ == "__main__":
	communities_directory = os.path.realpath(os.getcwd() + '/../../..')
	
	for i in range(1,10):
		setFilePaths2(communities_directory, i)
		#makeComponents2(i)
	
	
	gm = open('largestgraph.r', 'w')
	gm.write('library(ggplot2)\n')
	gm.write('library(scales)\n')
	gm.write('\n\n\n\n')
	
# 	for i in range(1,10):
# 		setFilePaths2(communities_directory, i)
# 		fsd = globalvar.OUTPUT_NETWORK_DIRECTORY_FOR_COMPONENTS
# 		largest = fsd + '/' + str(globalvar.FIELD) + str(globalvar.RUN) + '_' + str(globalvar.TYPE) + str(globalvar.START_YEAR) + '-' + str(globalvar.END_YEAR) + '_' + str(i) + 'years_LargestGrowth.csv'
# 		gm.write("AB"  + str(i) + "<- read.table('" + largest + "', header = TRUE, sep =';')\n" )
# 	gm.write("\n\np<-ggplot(AB1)\n")
# 	s = str(globalvar.FIELD) + str(globalvar.RUN) + '_' + str(globalvar.TYPE) + str(globalvar.START_YEAR) + '-' + str(globalvar.END_YEAR) + '_' + str(i) + 'years_LargestGraph.pdf'
# 	gm.write("pdffile <-c('" +s +"')\n")
# 	gm.write("pdf(pdffile)\n")
# 	gm.write("p + xlab('Year') + ylab('Percent')")
# 	for i in range(1,10):
# 		gm.write(" + geom_point(aes(AB" + str(i) + "$End_Year,AB" + str(i) + "$Percent, color = '" + str(i)+ "')) + geom_line(aes(AB" + str(i) + "$End_Year,AB" + str(i) + "$Percent, color = '" + str(i)+ "')) + opts(legend.title=theme_blank()) + scale_y_continuous(limits = c(0, 100))")
# 	gm.write("\nggsave(pdffile)\n\n")
# 	gm.close()
	
	for i in range(1,10):
		setFilePaths2(communities_directory, i)
		fsd = globalvar.OUTPUT_NETWORK_DIRECTORY_FOR_COMPONENTS
		largest = fsd + '/' + str(globalvar.FIELD) + str(globalvar.RUN) + '_' + str(globalvar.TYPE) + str(globalvar.START_YEAR) + '-' + str(globalvar.END_YEAR) + '_' + str(i) + 'years_LargestGrowth.csv'
		gm.write("AB"  + str(i) + "<- read.table('" + largest + "', header = TRUE, sep =';')\n" )
	
	
	for i in range(1,10):
		gm.write("\n\np" + str(i) + "<-ggplot(AB" + str(i) + ")\n")
		setFilePaths2(communities_directory, i)
		s = globalvar.OUTPUT_STATISTICS_DIRECTORY_FOR_COMPONENTS + '/' + 'allyears/components/images'
		if not os.path.exists(s):
			os.makedirs(s)
		s = s + '/' + str(globalvar.FIELD) + str(globalvar.RUN) + '_' + str(globalvar.TYPE) + str(globalvar.START_YEAR) + '-' + str(globalvar.END_YEAR) + '_' + str(i) + 'years_LargestGraph' + '.pdf'
		gm.write("pdffile <-c('" +s +"')\n")
		gm.write("pdf(pdffile)\n")
		gm.write("p" + str(i) + " + xlab('Year') + ylab('Percent')")
		gm.write(" + geom_point(aes(AB" + str(i) + "$End_Year,AB" + str(i) + "$Percent, color = '" + str(i)+ "')) + geom_line(aes(AB" + str(i) + "$End_Year,AB" + str(i) + "$Percent, color = '" + str(i)+ "')) + opts(legend.title=theme_blank()) + scale_y_continuous(limits = c(0, 100))")
		gm.write("\nggsave(pdffile)\n\n")
	gm.close()