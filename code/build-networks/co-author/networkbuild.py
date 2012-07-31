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
#/Users/Kallol/communities/code/network-stats/analysis.py

#--Classes--
class Paper:
    #ID
    #CI
    #SO
    #TI
    #BI
    #AU []
    #AF []
    #CT []
    #CO []
    #RF []
    #CA []
    #YR
    def __init__(self):
        self.ID = ''
        self.CI = ''
        self.SO = ''
        self.TI = ''
        self.BI = ''
        self.AU = []
        self.AF = []
        self.CT = []
        self.CO = []
        self.RF = []
        self.CA = []
        self.YR = 0 #integer
class Network:
    #--Variables--
    #papers []: array of paper type objects
    #nodes []: array of author names
    #numberOfNodes: Number of authors
    #degrees {}: total degrees {author_name: degree} .. if an author has 3 papers with some coauthor it will add up to 3 to this count
    #edges:  array of Links (if there are 3 links beteen 2 authors, that will contribute thrice to this total) -> array of pairs
    #differentEdges {}: Dictionary of unique pairs of author names , number of occurences. {('x','y'):4} !!IMPORATNT!!: x is ALWAYS less than y (alphabetically
    #numberOfDifferentEdges: Number of Different Links
    #numberOfEdges: Number of total Links (if there are 3 links beteen 2 authors, that will contribute 3 to this total)
    #differentDegrees {}: Dectionary of author, their degrees and list of coauthors. {'x':[5,['a','b','c','d',e']]}
    #startYear
    #endYear
    
    #--Procedures--
    #def __init__(self)
    #def makeSubCoauthorshipNetworkFromSuperCoauthorshipNetwork(self, Super, start_Year, end_Year)
    #def makeCoauthorshipNetworkFromFile(self, file)
    #def makeCoauthorshipNetworkFromPapers(self)
    #def readPapersFromFile(self, File)
    
    def __init__(self):
        self.papers = [] 
        self.nodes = []
        self.differentEdges = {}
        self.degrees = {}
        self.differentDegrees = {}
        self.startYear = 0
        self.endYear = 0
        self.numberOfNodes = 0
        self.numberOfDifferentEdges = 0
        self.numberOfEdges = 0
        self.edges = []
        self.G = nx.Graph()
        #self.DegreeCentrality = {}
        #self.ClosenessCentrality = {}
        #self.BetweennessCentrality = {}
    
    def getGeneralInfo(self):
        col1 = self.startYear
        col2 = self.endYear
        col3 = len(self.papers)
        col4 = self.numberOfNodes
        col5 = self.numberOfEdges
        
        return (col1, col2, col3, col4, col5)
    
    def getCollaborationDistribution(self):
        max = 0
        for author in self.differentDegrees:
            if(self.differentDegrees[author][0] > max):
                max = self.differentDegrees[author][0]
        #print max
        X = {}
        for i in range(0,max+1):
            X[i] = 0
        for author in self.differentDegrees:
            X[self.differentDegrees[author][0]] = X[self.differentDegrees[author][0]] + 1
        
        for k in X.keys():
            if(X[k] == 0):
                del X[k]
        return X
        
    def makeCoauthorshipGraph(self):
        self.G.add_nodes_from(self.nodes)
        self.G.add_edges_from(self.edges)
        #print self.G
        
    def getDegreeCentrality(self):
        x = nx.degree_centrality(self.G)
        #self.DegreeCentrality = x
        return x
        
    def getClosenessCentrality(self):
        x = nx.closeness_centrality(self.G)
        #self.ClosenessCentrality = x
        return x
        
    def getBetweennessCentrality(self):
        x = nx.betweenness_centrality(self.G)
        #self.BetweennessCentrality = x
        return x
    
    def makeSubCoauthorshipNetworkFromSuperCoauthorshipNetwork(self, Super, start_Year, end_Year):
        self.startYear = start_Year
        self.endYear = end_Year
        self.nodes = []
        self.differentEdges = {}
        self.differentDegrees = {}
        self.papers = []
        for paper in Super.papers:
            if((paper.YR<self.startYear) or (paper.YR>self.endYear)):
                continue
            self.papers.append(paper)
            for author in paper.AU:
                if(author not in self.nodes):
                    self.nodes.append(author)
                    self.numberOfNodes = self.numberOfNodes + 1
                    self.degrees[author] = 0
                if(author not in self.differentDegrees):
                    list = []
                    list.append(0)
                    list.append([])
                    self.differentDegrees[author] = list
            for author in paper.AU:
                for anotherAuthor in paper.AU:
                    if((author<anotherAuthor)): 
                        self.numberOfEdges = self.numberOfEdges + 1
                        self.edges.append((author,anotherAuthor))
                        if((author,anotherAuthor) not in self.differentEdges):
                            self.differentEdges[(author,anotherAuthor)] = 1
                            self.numberOfDifferentEdges = self.numberOfDifferentEdges + 1
                        else:
                            self.differentEdges[(author,anotherAuthor)] = self.differentEdges[(author,anotherAuthor)] + 1
                        self.degrees[author] = self.degrees[author] + 1
                        self.degrees[anotherAuthor] = self.degrees[anotherAuthor] + 1
                        if(anotherAuthor not in self.differentDegrees[author][1]):
                            self.differentDegrees[author][0] = self.differentDegrees[author][0] + 1
                            self.differentDegrees[author][1].append(anotherAuthor)
                            self.differentDegrees[anotherAuthor][0] = self.differentDegrees[anotherAuthor][0] + 1
                            self.differentDegrees[anotherAuthor][1].append(author)  
    def makeCoauthorshipNetworkFromFile(self, file):
        self.readPapersFromFile(file)
        self.makeCoauthorshipNetworkFromPapers()
        #self.makeGraph()
    def makeCoauthorshipNetworkFromPapers(self):
        self.nodes = []
        self.differentEdges = {}
        self.differentDegrees = {}
        self.numberOfNodes = 0
        self.numberOfDifferentEdges = 0
        minYear = 2011
        maxYear = 1990
        for paper in self.papers:
            for author in paper.AU:
                if(author not in self.nodes):
                    self.nodes.append(author)
                    self.numberOfNodes = self.numberOfNodes + 1
                if(author not in self.differentDegrees):
                    list = []
                    list.append(0)
                    list.append([])
                    self.differentDegrees[author] = list
            for author in paper.AU:
                for anotherAuthor in paper.AU:
                    if((author<anotherAuthor)): 
                        self.numberOfEdges = self.numberOfEdges + 1
                        self.edges.append((author,anotherAuthor))
                        if((author,anotherAuthor) not in self.differentEdges):
                            self.differentEdges[(author,anotherAuthor)] = 1
                            self.numberOfDifferentEdges = self.numberOfDifferentEdges + 1
                        else:
                            self.differentEdges[(author,anotherAuthor)] = self.differentEdges[(author,anotherAuthor)] + 1
                            
                        if(anotherAuthor not in self.differentDegrees[author][1]):
                            self.differentDegrees[author][0] = self.differentDegrees[author][0] + 1
                            self.differentDegrees[author][1].append(anotherAuthor)
                            self.differentDegrees[anotherAuthor][0] = self.differentDegrees[anotherAuthor][0] + 1
                            self.differentDegrees[anotherAuthor][1].append(author)
            if(paper.YR>maxYear):
                maxYear = paper.YR
            if(paper.YR<minYear):
                minYear = paper.YR
        self.startYear = minYear
        self.endYear = maxYear                
    def readPapersFromFile(self, File):
        self.papers = []
        inFile = open(File, "r")
        InitialNumberOfPapers = 0
        PaperFlag = 0 # 1 = inside processing a paper, 0 = otherwise
        
        p = Paper()
        for lines in inFile:
            string = str(lines)
            #print string
            if(string =='\n' or string ==' \n'):
                PaperFlag = 0
                self.papers.append(p)
                InitialNumberOfPapers = InitialNumberOfPapers +1
                p = Paper()
                continue
            if(string[0] == 'I' and string[1]=='D'):
                PaperFlag = 1
                #processing ID
                l = len(string)
                p.ID = string[3:l-1]
            elif(string[0] == 'C' and string[1]=='I'):
                #processing CI
                l = len(string)
                p.CI = string[3:l-1]
            elif(string[0] == 'S' and string[1]=='O'):
                #processing SO
                l = len(string)
                p.SO = string[3:l-1]
            elif(string[0] == 'T' and string[1]=='I'):
                #processing TI
                l = len(string)
                p.TI = string[3:l-1]
            elif(string[0] == 'B' and string[1]=='I'):
                #processing BI and Year
                l = len(string)
                p.BI = string[3:l-1]
                temp = string[l-5:l-1]
                p.YR  = int(temp)
            elif(string[0] == 'A' and string[1]=='U'):
                #processing AU
                l = len(string)
                s = string[3:l-1]    
                p.AU.append(s)
            elif((string[0] == ' ') and (PaperFlag==1)):
                l = len(string)
                s = string[1:l-1]    
                p.AU.append(s)
            elif(string[0] == 'A' and string[1]=='F'):
                #processing AF
                l = len(string)
                s = string[3:l-1]
                p.AF.append(s)
            elif(string[0] == 'C' and string[1]=='T'):
                #processing CT
                l = len(string)
                s = string[3:l-1]
                p.CT.append(s)
            elif(string[0] == 'C' and string[1]=='O'):
                #processing CO
                l = len(string)
                s = string[3:l-1]
                p.CO.append(s)
            elif(string[0] == 'R' and string[1]=='F'):
                #processing RF
                l = len(string)
                s = string[3:l-1]
                p.RF.append(s)
            elif(string[0] == 'C' and string[1]=='A'):
                #processing CA
                l = len(string)
                s = string[3:l-1]
                p.CA.append(s)
                
        inFile.close()
    def printNetworkForPajek(self, field, run, type, size, directoryPath):
        if not os.path.exists(directoryPath):
            os.makedirs(directoryPath)
            print('New directory made: ' + str(dp1))
        dp1 = directoryPath + '/net_files/'
        if not os.path.exists(dp1):
            os.makedirs(dp1)
            print('New directory made: ' + str(dp1))
        dp1 = directoryPath + '/vec_files/'
        if not os.path.exists(dp1):
            os.makedirs(dp1)
            print('New directory made: ' + str(dp1))
        fs = directoryPath + '/net_files/' + str(type) + str(self.startYear) + '-' + str(self.endYear) + '_' + str(size) + 'years' + 'CoauthorshipNetwork.net'
        fsvec = directoryPath + '/vec_files/' + str(type) + str(self.startYear) + '-' + str(self.endYear) + '_' + str(size) + 'years' + 'CoauthorshipNetwork.vec'
        outFile = open(fs, 'w')
        outFilevec = open(fsvec,'w')
        
        nodeDic = {} #dictionary for indexing the authors
        index = 0
        for node in self.nodes:
            index = index + 1
            nodeDic[node] = index
        outFile.write('*Vertices ' + str(index) + '\n') 
        outFilevec.write('*Vertices ' + str(index) + '\n')
        sortedAuthorList = sorted(nodeDic.items(), key = itemgetter(1))
        for author in sortedAuthorList:
            outFile.write(str(author[1]) + ' "'  + str(author[0]) + '"' + '\n')
            outFilevec.write(str(self.degrees[author[0]]) + '\n')
        outFile.write('*Edges\n')
        sortedEdges = sorted(self.differentEdges.items(), key = itemgetter(1))
        for edge in sortedEdges:
            outFile.write(str(nodeDic[edge[0][0]]) + ' ' + str(nodeDic[edge[0][1]]) + ' ' + str(edge[1]) + '\n')
        outFile.close()

    
    def getMinDistance(): #Returns the minimum distance dictionary: {(author1_name,author2_name):dis} ... dis ==1 -> no path
        index = 0
        AuthorMap = {} #{'author_name':author index}
        ReverseMap = {}
        AuthorDis = {} #{('x,'y'):4} -> x,y: author_names and 4 is min distance between those two
        for author in self.nodes:
            if author not in AuthorMap:
                AuthorMap[author] = index
                ReverseMap[index] = author
                index = index + 1
        INF = self.numberOfNodes*100
        path = []
        row = []
        for i in range(0,self.numberOfNodes):
            for j in range(0,self.numberOfNodes):
                if(i==j):
                    row.append(0)
                    continue
                if(((ReverseMap[i], Reversemap[j]) in self.edges) or ((ReverseMap[j], Reversemap[i]) in self.edges)):
                    row.append(1)
                else:
                    row.append(INF)
            path.append(row)
        #Floyd-Warshall's Algorithm for finding the shortest path O(n^3)
        for k in range(0,self.numberOfNodes):
            for i in range(0,self.numberOfNodes):
                for j in range(0,self.numberOfNodes):
                    if(path[i][j] < (path[i][k] + path[k][j])):
                        path[i][j] = (path[i][k] + path[k][j])
        for i in range(0,self.numberOfNodes):
            for j in range(0,self.numberOfNodes):
                if(path[i][j] == INF):
                    path[i][j] == -1
                AuthorDis[(ReverseMap[i], ReverseMap[j])]  = path[i][j]
        return AuthorDis
       
#--Global Functions--

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

def makeCoauthorshipNetworkFilesForPajek():
    global TYPE
    global START_YEAR
    global SIZE
    global OUTPUT_NETWORK_DIRECTORY_FOR_PAJEK
    global FIELD
    global RUN
    global END_YEAR
    
    #output_directory = OUTPUT_NETWORK_DIRECTORY_FOR_PAJEK + '/' + 
    N = Network()
    N.makeCoauthorshipNetworkFromFile(INPUT_REDUCED_FILE_PATH)
    if(TYPE == 'discrete'):
        start = START_YEAR
        end = start + SIZE -1
        while(end<=END_YEAR):
            Partition = Network()
            Partition.makeSubCoauthorshipNetworkFromSuperCoauthorshipNetwork(N, start, end)
            Partition.printNetworkForPajek(FIELD, RUN, TYPE, SIZE, OUTPUT_NETWORK_DIRECTORY_FOR_PAJEK)
            start = end + 1
            end = end + SIZE
    elif(TYPE == 'accumulative'):
        start = START_YEAR
        end = start + SIZE -1
        while(end<=END_YEAR):
            Partition = Network()
            Partition.makeSubCoauthorshipNetworkFromSuperCoauthorshipNetwork(N, start, end)
            Partition.printNetworkForPajek(FIELD, RUN, TYPE, SIZE, OUTPUT_NETWORK_DIRECTORY_FOR_PAJEK)
            end = end + SIZE
    elif(TYPE == 'sliding'):
        start = START_YEAR
        end = start + SIZE -1
        while(end<=END_YEAR):
            Partition = Network()
            Partition.makeSubCoauthorshipNetworkFromSuperCoauthorshipNetwork(N, start, end)
            Partition.printNetworkForPajek(FIELD, RUN, TYPE, SIZE, OUTPUT_NETWORK_DIRECTORY_FOR_PAJEK)
            start = start + 1
            end = end + 1
if __name__ == "__main__":
    setFilePaths()
    makeCoauthorshipNetworkFilesForPajek()