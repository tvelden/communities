import os
import sys
import operator
import math
import numpy
import scipy.stats
from operator import itemgetter
import pdb
import networkx as nx
sys.path.append(os.path.realpath('../../tna'))
import globalvar
from globalfuncs import *
from analyzer import *

#--Global Variables--

#SWITCHES: Change the values to "False" if you dont want them
I_WANT_ABBASI_TABLE_2_3 = True
I_WANT_DEGREE_CENTRALITY = True
I_WANT_CLOSENESS_CENTRALITY = True 
I_WANT_BETWEENNESS_CENTRALITY = True
    
#--Global Functions--
              
def makeTemporalDataFilesForAbbasi():
    
    print 'Started gathering data for Abbasi ...'
    
    N = Network()
    N.makeCoauthorshipNetworkFromFile(globalvar.INPUT_REDUCED_FILE_PATH)
    
    directoryPath = globalvar.OUTPUT_STATISTICS_DIRECTORY + '/allyears/whole_net/tables' 
    if not os.path.exists(directoryPath):
            os.makedirs(directoryPath)
            print('New directory made: ' + str(directoryPath))
    Table4file = directoryPath + '/'+ str(globalvar.FIELD) + str(globalvar.RUN) + '_' + str(globalvar.TYPE) + str(globalvar.START_YEAR) + '-' + str(globalvar.END_YEAR) + '_' + str(globalvar.SIZE) + 'years_wholenet_DegreeCentrality_hub.csv'
    Table4 = open(Table4file, 'w')
    Table4.write('Start_Year; End_Year; Correlation_Betwwen_Prev_Degree_and_New_Degree; Correlation_Betwwen_Prev_Degree_and_New_Authors_Degree; Correlation_Betwwen_Prev_Degree_and_New_Old_Degree\n')
    Table5file = directoryPath + '/'+ str(globalvar.FIELD) + str(globalvar.RUN) + '_' + str(globalvar.TYPE)  + str(globalvar.START_YEAR) + '-' + str(globalvar.END_YEAR) + '_' + str(globalvar.SIZE) + 'years_wholenet_ClosenessCentrality_hub.csv'
    Table5 = open(Table5file, 'w')
    Table5.write('Start_Year; End_Year; Correlation_Betwwen_Prev_Closeness_and_New_Degree; Correlation_Betwwen_Prev_Closeness_and_New_Authors_Degree; Correlation_Betwwen_Prev_Closeness_and_New_Old_Degree\n')
    Table6file = directoryPath + '/'+ str(globalvar.FIELD) + str(globalvar.RUN) + '_' + str(globalvar.TYPE) + str(globalvar.START_YEAR) + '-' + str(globalvar.END_YEAR) + '_' + str(globalvar.SIZE) + 'years_wholenet_BetweennessCentrality_hub.csv'
    Table6 = open(Table6file, 'w')
    Table6.write('Start_Year; End_Year; Correlation_Betwwen_Prev_Betweenness_and_New_Degree; Correlation_Betwwen_Prev_Betweenness_and_New_Authors_Degree; Correlation_Betwwen_Prev_Betweenness_and_New_Old_Degree\n')
    
    #Degree Centrality Correlations
    print 'Started Computing Degree Centrality correlation ...'
    y1 = globalvar.START_YEAR
    y2 = y1 + globalvar.SIZE -1    
    while(y2<=globalvar.END_YEAR):
        if(I_WANT_DEGREE_CENTRALITY == True):
            old = Network()
            old.makeSubCoauthorshipNetworkFromSuperCoauthorshipNetwork(N, globalvar.START_YEAR, y1-1)
            new = Network()
            new.makeSubCoauthorshipNetworkFromSuperCoauthorshipNetwork(N, y1, y2)
            C = Comparer(old, new) 
            C.getReadyForCentralityMeasures()
            (column1, column2, column3, column4, column5) =  C.getDataForDegreeCentralityVsLinkAssociationsForHubs()
            print column1, column2, column3, column4, column5
            Table4.write(str(column1) +';'+str(column2) +';'+str(column3) +';'+str(column4) +';'+str(column5) + '\n')
        else:
            Table4.write('0; 0; 0; 0; 0\n')
        y1 = y2 + 1
        y2 = y1 + globalvar.SIZE -1
    Table4.close()
    print "Computation for Degree Centrality is completed"
    
    #Closeness Centrality Correlations
    print 'Started Computing Closeness Centrality correlation ...'
    y1 = globalvar.START_YEAR
    y2 = y1 + globalvar.SIZE -1    
    while(y2<=globalvar.END_YEAR):
        if(I_WANT_CLOSENESS_CENTRALITY == True):
            old = Network()
            old.makeSubCoauthorshipNetworkFromSuperCoauthorshipNetwork(N, globalvar.START_YEAR, y1-1)
            new = Network()
            new.makeSubCoauthorshipNetworkFromSuperCoauthorshipNetwork(N, y1, y2)
            C = Comparer(old, new) 
            C.getReadyForCentralityMeasures()
            (column1, column2, column3, column4, column5) =  C.getDataForClosenessCentralityVsLinkAssociationsForHubs()
            print column1, column2, column3, column4, column5
            Table5.write(str(column1) +';'+str(column2) +';'+str(column3) +';'+str(column4) +';'+str(column5) + '\n')
        else:
            Table5.write('0; 0; 0; 0; 0\n')
        y1 = y2 + 1
        y2 = y1 + globalvar.SIZE -1
    Table4.close()
    Table5.close()
    print "Computation for Closeness Centrality is completed"
    
    #Betweenness Centrality Correlations
    print 'Started Computing Betweenness Centrality correlation ...'
    y1 = globalvar.START_YEAR
    y2 = y1 + globalvar.SIZE -1
    while(y2<=globalvar.END_YEAR):
        if(I_WANT_BETWEENNESS_CENTRALITY == True):
            old = Network()
            old.makeSubCoauthorshipNetworkFromSuperCoauthorshipNetwork(N, globalvar.START_YEAR, y1-1)
            new = Network()
            new.makeSubCoauthorshipNetworkFromSuperCoauthorshipNetwork(N, y1, y2)
            C = Comparer(old, new)  
            C.getReadyForCentralityMeasures()
            (column1, column2, column3, column4, column5) =  C.getDataForBetweennessCentralityVsLinkAssociationsForHubs()
            print column1, column2, column3, column4, column5
            Table6.write(str(column1) +';'+str(column2) +';'+str(column3) +';'+str(column4) +';'+str(column5) + '\n')
        else:
            Table6.write('0; 0; 0; 0; 0\n')
        y1 = y2 + 1
        y2 = y1 + globalvar.SIZE -1
    Table6.close()
    print "Computation for Betweenness Centrality is completed"

def makeCollaborationDistributionFile():
    print 'Gathering data for collaboration distribution among the authors entire network  ...'
    directoryPath = globalvar.OUTPUT_STATISTICS_DIRECTORY + '/allyears/whole_net/tables' 
    if not os.path.exists(directoryPath):
            os.makedirs(directoryPath)
            print('New directory made: ' + str(directoryPath))
    Mfile = directoryPath + '/'+ str(globalvar.FIELD) + str(globalvar.RUN) + '_' + str(globalvar.TYPE) + str(globalvar.START_YEAR) + '-' + str(globalvar.END_YEAR) + '_' + str(globalvar.SIZE) + 'years_wholenet_CollaborationDistribution_hub.csv'
    MF = open(Mfile, 'w')
    MF.write('Collaborators; Frequency\n')
    N = Network()
    N.makeCoauthorshipNetworkFromFile(globalvar.INPUT_REDUCED_FILE_PATH)
    X = N.getCollaborationDistributionForHubs()
    for k in X:
        if(k ==0):
            continue
        MF.write(str(k) + ';' + str(X[k]) + '\n')
    MF.close()
    print 'Finished gathering data for collaboration distribution!!'
    

if __name__ == "__main__":
    communities_directory = os.path.realpath(os.getcwd() + '/../../..')
    setFilePaths(communities_directory)
    #makeTemporalDataFilesForAbbasi()
    makeCollaborationDistributionFile()
    