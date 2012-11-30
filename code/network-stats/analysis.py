import os
import sys
import operator
import math
import numpy
import scipy.stats
from operator import itemgetter
import pdb
import networkx as nx
sys.path.append(os.path.realpath('../tna'))
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
    Table2file = directoryPath + '/'+ str(globalvar.FIELD) + str(globalvar.RUN) + '_' + str(globalvar.TYPE) + str(globalvar.START_YEAR) + '-' + str(globalvar.END_YEAR) + '_' + str(globalvar.SIZE) + 'years_wholenet_AbbasiTable2.csv'
    Table2 = open(Table2file, 'w')
    Table2.write('Start_Year; End_Year; Cumulative_No_of_Authors; No_of_New_Authors; No_Of_New_Authors_Connected_to_atleast_one_new_author; Percent_Of_New_Authors_Connected_to_atleast_one_new_author; No_Of_New_Authors_Connected_to_atleast_one_old_author; Percent_Of_New_Authors_Connected_to_atleast_one_old_author; No_Of_Old_Authors_Connected_to_atleast_one_new_author; Percent_Of_Old_Authors_Connected_to_atleast_one_new_author; No_Of_Old_Authors_Connected_to_atleast_one_old_author; Percent_Of_Old_Authors_Connected_to_atleast_one_old_author; No_Of_Old_Authors_Connected_to_atleast_one_any_author; Percent_Of_Old_Authors_Connected_to_atleast_one_any_author\n')
    Table3file = directoryPath + '/'+ str(globalvar.FIELD) + str(globalvar.RUN) + '_' + str(globalvar.TYPE) + str(globalvar.START_YEAR) + '-' + str(globalvar.END_YEAR) + '_' + str(globalvar.SIZE) + 'years_wholenet_AbbasiTable3.csv'
    Table3 = open(Table3file, 'w')
    Table3.write('Start_Year; End_Year; Cumulative_Number_of_Links; Number_of_New_Links; Number_of_New_Links_Among_New_Authors; Percent_of_New_Links_Among_New_Authors; Number_Of_Links_Between_New_and_Old; Percent_Of_Links_Between_New_and_Old; Number_of_New_Links_Between_Two_Old_Authors_Not_Connected_Before; Percent_of_New_Links_Between_Two_Old_Authors_Not_Connected_Before; Number_of_Links_Among_Old_Authors_Connected_Before ; Percent_of_Links_Among_Old_Authors_Connected_Before\n')
    Table4file = directoryPath + '/'+ str(globalvar.FIELD) + str(globalvar.RUN) + '_' + str(globalvar.TYPE) + str(globalvar.START_YEAR) + '-' + str(globalvar.END_YEAR) + '_' + str(globalvar.SIZE) + 'years_wholenet_DegreeCentrality.csv'
    Table4 = open(Table4file, 'w')
    Table4.write('Start_Year; End_Year; Correlation_Between_Prev_Degree_and_New_Degree; pCDND; Correlation_Between_Prev_Degree_and_New_Authors_Degree; pCDNAD; Correlation_Between_Prev_Degree_and_New_Old_Degree; pCDNOD\n')
    Table5file = directoryPath + '/'+ str(globalvar.FIELD) + str(globalvar.RUN) + '_' + str(globalvar.TYPE)  + str(globalvar.START_YEAR) + '-' + str(globalvar.END_YEAR) + '_' + str(globalvar.SIZE) + 'years_wholenet_ClosenessCentrality.csv'
    Table5 = open(Table5file, 'w')
    Table5.write('Start_Year; End_Year; Correlation_Between_Prev_Closeness_and_New_Degree; pCDND; Correlation_Between_Prev_Closeness_and_New_Authors_Degree; pCDNAD; Correlation_Between_Prev_Closeness_and_New_Old_Degree; pCDNOD\n')
    Table6file = directoryPath + '/'+ str(globalvar.FIELD) + str(globalvar.RUN) + '_' + str(globalvar.TYPE) + str(globalvar.START_YEAR) + '-' + str(globalvar.END_YEAR) + '_' + str(globalvar.SIZE) + 'years_wholenet_BetweennessCentrality.csv'
    Table6 = open(Table6file, 'w')
    Table6.write('Start_Year; End_Year; Correlation_Between_Prev_Betweenness_and_New_Degree; pCDND; Correlation_Between_Prev_Betweenness_and_New_Authors_Degree; pCDNAD; Correlation_Between_Prev_Betweenness_and_New_Old_Degree; pCDNOD\n')
    
    print 'Making Table2 and Table3 ...'
    y1 = globalvar.START_YEAR
    y2 = y1 + globalvar.SIZE -1
    while(y2<=globalvar.END_YEAR):
        if(I_WANT_ABBASI_TABLE_2_3 == True):
            old = Network()
            old.makeSubCoauthorshipNetworkFromSuperCoauthorshipNetwork(N, globalvar.START_YEAR, y1-1)
            new = Network()
            new.makeSubCoauthorshipNetworkFromSuperCoauthorshipNetwork(N, y1, y2)
            C = Comparer(old, new)
            (column1, column2, column3, column4, column5, column6, column7, column8, column9, column10, column11, column12, column13, column14 ) =  C.contentForAbbasiTable2()
            print column1, column2, column3, column4, column5, column6, column7, column8, column9, column10, column11, column12, column13, column14 
            Table2.write(str(column1) +';'+str(column2) +';'+str(column3) +';'+str(column4) +';'+str(column5) +';'+str(column6) +';'+str(column7) +';'+str(column8) +';'+str(column9) +';'+str(column10) +';'+str(column11) +';'+str(column12) +';'+str(column13) +';'+str(column14) +'\n')
            (column1, column2, column3, column4, column5, column6, column7, column8, column9, column10, column11, column12) = C.contentForAbbasiTable3()
            print column1, column2, column3, column4, column5, column6, column7, column8, column9, column10, column11, column12
            Table3.write(str(column1) +';'+str(column2) +';'+str(column3) +';'+str(column4) +';'+str(column5) +';'+str(column6) +';'+str(column7) +';'+str(column8) +';'+str(column9) +';'+str(column10) +';'+str(column11) +';'+str(column12) +'\n')
        else:
            Table2.write('0; 0; 0; 0; 0; 0; 0; 0; 0; 0; 0; 0; 0; 0\n')
            Table3.write('0; 0; 0; 0; 0; 0; 0; 0; 0; 0; 0; 0\n')
        if(globalvar.TYPE =='discrete'):
        	y1 = y2+1
        	y2 = y2 + globalvar.SIZE
        elif(globalvar.TYPE == 'accumulative'):
        	y1 = y2 +1
        	y2 = y2 + globalvar.SIZE
        elif(globalvar.TYPE == 'sliding'):
        	y1 = y1 + 1
        	y2 = y2 + 1
    Table2.close()
    Table3.close()
    print 'Finished making Table2 and Table 3!!'
    
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
            (X, column1, column2, column3, p3, column4, p4, column5, p5) =  C.getDataForDegreeCentralityVsLinkAssociations()
            print column1, column2, column3, p3, column4, p4, column5, p5
            Table4.write(str(column1) +';'+str(column2) +';'+str(column3) +';'+str(p3) +';'+str(column4) +';'+str(p4)+ ';' + str(column5)+';'+str(p5) + '\n')
            fos = directoryPath + '/extra/'
            if not os.path.exists(fos):
            	os.makedirs(fos)
            	print('New directory made: ' + str(fos))
            fos = fos + str(globalvar.FIELD) + str(globalvar.RUN) + '_' + str(globalvar.TYPE) + str(globalvar.START_YEAR) + '-' + str(y1-1) + '_' + str(globalvar.SIZE) + 'years_Degree_centrality_list.csv'
            fo = open(fos, 'w')
            fo.write('AuthorName; Centrality\n')
            for e in X:
            	fo.write(str(e) + ';' + str(X[e]) + '\n')
            fo.close()
        else:
            Table4.write('0; 0; 0; 0; 0; 0; 0; 0\n')
        if(globalvar.TYPE =='discrete'):
        	y1 = y2+1
        	y2 = y2 + globalvar.SIZE
        elif(globalvar.TYPE == 'accumulative'):
        	y1 = y2 + 1
        	y2 = y2 + globalvar.SIZE
        elif(globalvar.TYPE == 'sliding'):
        	y1 = y1 + 1
        	y2 = y2 + 1
        
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
            (X, column1, column2, column3, p3, column4, p4, column5, p5) =  C.getDataForClosenessCentralityVsLinkAssociations()
            print column1, column2, column3, p3, column4, p4, column5, p5
            Table5.write(str(column1) +';'+str(column2) +';'+str(column3) +';'+str(p3) +';'+str(column4) +';'+str(p4)+ ';' + str(column5)+';'+str(p5) + '\n')
            fos = directoryPath + '/extra/'
            if not os.path.exists(fos):
            	os.makedirs(fos)
            	print('New directory made: ' + str(fos))
            fos = fos + str(globalvar.FIELD) + str(globalvar.RUN) + '_' + str(globalvar.TYPE) + str(globalvar.START_YEAR) + '-' + str(y1-1) + '_' + str(globalvar.SIZE) + 'years_Closeness_centrality_list.csv'
            fo = open(fos, 'w')
            fo.write('AuthorName; Centrality\n')
            for e in X:
            	fo.write(str(e) + ';' + str(X[e]) + '\n')
            fo.close()
        else:
            Table5.write('0; 0; 0; 0; 0; 0; 0; 0\n')
        if(globalvar.TYPE =='discrete'):
        	y1 = y2+1
        	y2 = y2 + globalvar.SIZE
        elif(globalvar.TYPE == 'accumulative'):
        	y1 = y2 + 1
        	y2 = y2 + globalvar.SIZE
        elif(globalvar.TYPE == 'sliding'):
        	y1 = y1 + 1
        	y2 = y2 + 1
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
            (X, column1, column2, column3, p3, column4, p4, column5, p5) =  C.getDataForBetweennessCentralityVsLinkAssociations()
            print column1, column2, column3, p3, column4, p4, column5, p5
            Table6.write(str(column1) +';'+str(column2) +';'+str(column3) +';'+str(p3) +';'+str(column4) +';'+str(p4)+ ';' + str(column5)+';'+str(p5) + '\n')
            fos = directoryPath + '/extra/'
            if not os.path.exists(fos):
            	os.makedirs(fos)
            	print('New directory made: ' + str(fos))
            fos = fos + str(globalvar.FIELD) + str(globalvar.RUN) + '_' + str(globalvar.TYPE) + str(globalvar.START_YEAR) + '-' + str(y1-1) + '_' + str(globalvar.SIZE) + 'years_Betweenness_centrality_list.csv'
            fo = open(fos, 'w')
            fo.write('AuthorName; Centrality\n')
            for e in X:
            	fo.write(str(e) + ';' + str(X[e]) + '\n')
            fo.close()
        else:
            Table6.write('0; 0; 0; 0; 0; 0; 0; 0\n')
        if(globalvar.TYPE =='discrete'):
        	y1 = y2+1
        	y2 = y2 + globalvar.SIZE
        elif(globalvar.TYPE == 'accumulative'):
        	y2 = y2 + globalvar.SIZE
        elif(globalvar.TYPE == 'sliding'):
        	y1 = y1 + 1
        	y2 = y2 + 1
    Table6.close()
    print "Computation for Betweenness Centrality is completed"
    
def makeCollaborationDistributionFile():
    print 'Gathering data for collaboration distribution among the authors entire network  ...'
    directoryPath = globalvar.OUTPUT_STATISTICS_DIRECTORY + '/allyears/whole_net/tables' 
    if not os.path.exists(directoryPath):
            os.makedirs(directoryPath)
            print('New directory made: ' + str(directoryPath))
    Mfile = directoryPath + '/'+ str(globalvar.FIELD) + str(globalvar.RUN) + '_' + str(globalvar.TYPE) + str(globalvar.START_YEAR) + '-' + str(globalvar.END_YEAR) + '_' + str(globalvar.SIZE) + 'years_wholenet_CollaborationDistribution.csv'
    MF = open(Mfile, 'w')
    MF.write('Collaborators; Frequency\n')
    N = Network()
    N.makeCoauthorshipNetworkFromFile(globalvar.INPUT_REDUCED_FILE_PATH)
    X = N.getCollaborationDistribution()
    for k in X:
        if(k ==0):
            continue
        MF.write(str(k) + ';' + str(X[k]) + '\n')
    MF.close()
    print 'Finished gathering data for collaboration distribution!!'

def makeGeneralNetworkDataFile():
    
    print 'Gathering the general information of the total network ...'
    
    directoryPath = globalvar.OUTPUT_STATISTICS_DIRECTORY + '/allyears/whole_net/tables' 
    if not os.path.exists(directoryPath):
            os.makedirs(directoryPath)
            print('New directory made: ' + str(directoryPath))
    Mfile = directoryPath + '/'+ str(globalvar.FIELD) + str(globalvar.RUN) + '_' + str(globalvar.TYPE) + str(globalvar.START_YEAR) + '-' + str(globalvar.END_YEAR) + '_' + str(globalvar.SIZE) + 'years_wholenet_GeneralInfo.csv'
    MF = open(Mfile, 'w')
    MF.write('Start_Year; End_Year; Number_Of_Papers; Number_Of_Authors; Number_Of_Edges; Number_Of_Unweighted_Edges\n')
    N = Network()
    N.makeCoauthorshipNetworkFromFile(globalvar.INPUT_REDUCED_FILE_PATH)
    if(globalvar.TYPE == 'discrete'):
        start = globalvar.START_YEAR
        end = start + globalvar.SIZE -1
        while(end<=globalvar.END_YEAR):
            Partition = Network()
            Partition.makeSubCoauthorshipNetworkFromSuperCoauthorshipNetwork(N, start, end)
            (col1, col2, col3, col4, col5, col6) = Partition.getGeneralInfo()
            MF.write(str(col1) + ';' + str(col2) + ';' + str(col3) + ';' + str(col4) + ';' + str(col5) + ';' + str(col6) + '\n' )
            start = end + 1
            end = end + globalvar.SIZE
    elif(globalvar.TYPE == 'accumulative'):
        start = globalvar.START_YEAR
        end = start + globalvar.SIZE -1
        while(end<=globalvar.END_YEAR):
            Partition = Network()
            Partition.makeSubCoauthorshipNetworkFromSuperCoauthorshipNetwork(N, start, end)
            (col1, col2, col3, col4, col5, col6) = Partition.getGeneralInfo()
            MF.write(str(col1) + ';' + str(col2) + ';' + str(col3) + ';' + str(col4) + ';' + str(col5) + ';' + str(col6) + '\n' )
            end = end + globalvar.SIZE
    elif(globalvar.TYPE == 'sliding'):
        start = globalvar.START_YEAR
        end = start + globalvar.SIZE -1
        while(end<=globalvar.END_YEAR):
            Partition = Network()
            Partition.makeSubCoauthorshipNetworkFromSuperCoauthorshipNetwork(N, start, end)
            (col1, col2, col3, col4, col5, col6) = Partition.getGeneralInfo()
            MF.write(str(col1) + ';' + str(col2) + ';' + str(col3) + ';' + str(col4) + ';' + str(col5) + ';' + str(col6) + '\n' )
            start = start + 1
            end = end + 1
    MF.close()
    print 'Finished gathering the general information !!'
    
def makeAuthorDistributionAmongPapersFile():
    print 'Gathering data for Author distribution among the papers in entire network ...'
    directoryPath = globalvar.OUTPUT_STATISTICS_DIRECTORY + '/allyears/whole_net/tables' 
    if not os.path.exists(directoryPath):
        os.makedirs(directoryPath)
        print('New directory made: ' + str(directoryPath))
    print directoryPath
    Mfile = directoryPath + '/'+ str(globalvar.FIELD) + str(globalvar.RUN) + '_' + str(globalvar.TYPE) + str(globalvar.START_YEAR) + '-' + str(globalvar.END_YEAR) + '_' + str(globalvar.SIZE) + 'years_wholenet_AuthorDistribution.csv'
    MWfile = directoryPath + '/'+ str(globalvar.FIELD) + str(globalvar.RUN) + '_' + str(globalvar.TYPE) + str(globalvar.START_YEAR) + '-' + str(globalvar.END_YEAR) + '_' + str(globalvar.SIZE) + 'years_wholenet_AuthorDistributionWithList.csv'
    MF = open(Mfile, 'w')
    MW = open(MWfile, 'w')
    MF.write('No_of_Authors; Frequency_of_Papers\n')
    MW.write('No_of_Authors; Frequency_of_Papers\n')
    N = Network()
    N.makeCoauthorshipNetworkFromFile(globalvar.INPUT_REDUCED_FILE_PATH)
    X = N.getAuthorDistributionAmongPapers()
    for e in X:
    	MF.write(str(e) + '; ' + str(X[e][0]) + '\n')
    	print e, X[e][0]
    	MW.write(str(e) + '; ' + str(X[e][0]) + ': ')
    	for el in X[e][1]:
    		MW.write('; ' + str(el))
    	MW.write('\n')
    MF.close()
    MW.close()


if __name__ == "__main__":
    communities_directory = os.path.realpath(os.getcwd() + '/../..')
    setFilePaths(communities_directory)
    makeGeneralNetworkDataFile()
    makeCollaborationDistributionFile()
    makeTemporalDataFilesForAbbasi()
    makeAuthorDistributionAmongPapersFile()
    