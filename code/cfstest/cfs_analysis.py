import os
import sys
import operator
import numpy
import scipy.stats
from operator import itemgetter
import pdb
import networkx as nx

#--Global Variables--

#SWITCHES: Change the values to "False" if you dont want them
I_WANT_ABBASI_TABLE_2_3 = True
I_WANT_DEGREE_CENTRALITY = True
I_WANT_CLOSENESS_CENTRALITY = True 
I_WANT_BETWEENNESS_CENTRALITY = True

#Others:
RELATIVE_INPUT_PARAMETER_FILE = 'parameters-global.txt'
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
        col6 = self.numberOfDifferentEdges
        
        return (col1, col2, col3, col4, col5, col6)
    
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
        fs = directoryPath + '/net_files/' + str(field) + str(run) + str(type) + str(self.startYear) + '-' + str(self.endYear) + '_' + str(size) + 'years' + 'CoauthorshipNetwork.net'
        fsvec = directoryPath + '/vec_files/' + str(field) + str(run) + str(type) + str(self.startYear) + '-' + str(self.endYear) + '_' + str(size) + 'years' + 'CoauthorshipNetwork.vec'
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
        
class Comparer:
    #--Variables--
    #previous : The previous Network, Network type object
    #current : The present Network, Network type object
    #numberOfNewNodes
    #numberOfNewEdges
    #numberOfCommonNodes
    #numberOfCommonEdges
    #newNodes: array of authors who are in current, but not in previous
    #newEdges: array of links who are in current, but not in previous
    #commonNodes: array of authors who contributed both in past and in present
    #commonEdges: array of links who are both in current and previous
    #dcVna: dictionary {author:}
    #dcVoa: dictionary {}
    #--Procedures--
    
    def __init__(self, Previous, Current):
        self.previous = Previous
        self.current = Current
        self.numberOfNewNodes = 0
        self.newNodes = []
        self.numberOfNewEdges = 0
        self.newEdges = []
        self.numberOfCommonNodes = 0
        self.commonNodes = []
        self.numberOfCommonEdges = 0
        self.commonEdges = []
        self.initializeNewNodes()
        self.initializeNewEdges()
        self.initializeCommonNodes()
        self.initializeCommonEdges()
        self.dcVna = {}
        self.dcVoa = {}
    def initializeNewNodes(self):
        self.numberOfNewNodes = 0
        self.newNodes = []
        for node in self.current.nodes:
            if node not in self.previous.nodes:
                self.numberOfNewNodes = self.numberOfNewNodes + 1
                self.newNodes.append(node)
    def initializeNewEdges(self):
        self.numberOfNewEdges = 0
        self.newEdges = []
        for edge in self.current.differentEdges:
            if edge not in self.previous.differentEdges:
                self.numberOfNewEdges = self.numberOfNewEdges + 1
                self.newEdges.append(edge)
    def initializeCommonNodes(self):
        self.numberOfCommonNodes = 0
        self.commonNodes = []
        for node in self.current.nodes:
            if node in self.previous.nodes:
                self.numberOfCommonNodes = self.numberOfCommonNodes + 1
                self.commonNodes.append(node) 
        #print self.commonNodes
    def initializeCommonEdges(self):
        self.numberOfCommonEdges = 0
        self.commonEdges = []
        for edge in self.current.differentEdges:
            if edge in self.previous.differentEdges:
                self.numberOfCommonEdges = self.numberOfCommonEdges + 1
                self.commonEdges.append(edge)    
    def cumulativeNumberOfAuthors(self):
        return self.previous.numberOfNodes + self.numberOfNewNodes
    def numberOfNewAuthors(self):
        return self.numberOfNewNodes
    def numberOfNewAuthorsAttachedToAtLeastANewAuthor(self):
        ans = 0
        for author in self.newNodes:
            for coauthor in self.current.differentDegrees[author][1]:
                if coauthor in self.newNodes:
                    ans = ans + 1
                    break
        return ans
    def numberOfNewAuthorsAttachedToAtLeastAnOldAuthor(self):
        ans = 0
        for author in self.newNodes:
            for coauthor in self.current.differentDegrees[author][1]:
                if coauthor in self.previous.nodes:
                    ans = ans + 1
                    break
        return ans
    def numberOfOldAuthorsAttachedToAtLeastANewAuthor(self):
        ans = 0
        for author in self.commonNodes:
            for coauthor in self.current.differentDegrees[author][1]:
                if coauthor in self.newNodes:
                    ans = ans + 1
                    break
        return ans
    def numberOfOldAuthorsAttachedToAtLeastAnOldAuthor(self):
        ans = 0
        for author in self.commonNodes:
            for coauthor in self.current.differentDegrees[author][1]:
                if coauthor in self.previous.nodes:
                    ans = ans + 1
                    break
        return ans
    def numberOfOldAuthorsAttachedToAtLeastAnAuthor(self):
        return self.numberOfCommonNodes
    def numberOfNewLinksAmongNewAuthors(self):
        ans = 0
        for edge in self.current.edges:
            if((edge[0] in self.newNodes) and (edge[1] in self.newNodes)):
                ans = ans + 1
        return ans
    def numberOfNewLinksBetweenNewAndOldAuthors(self):
        ans = 0
        for edge in self.current.edges:
            if(((edge[0] in self.newNodes) and (edge[1] in self.commonNodes)) or ((edge[1] in self.newNodes) and (edge[0] in self.commonNodes))):
                ans = ans + 1
        return ans
    def numberOfLinksBetweenOldAuthorsNotConnectedBefore(self):
        ans = 0
        for edge in self.current.edges:
            if((edge[0] in self.commonNodes) and (edge[1] in self.commonNodes) and (edge not in self.previous.edges)):
                ans = ans + 1
        return ans
    def numberOfLinksBetweenOldAuthorsConnectedBefore(self):
        ans = 0
        for edge in self.current.edges:
            if((edge[0] in self.commonNodes) and (edge[1] in self.commonNodes) and (edge in self.previous.edges)):
                ans = ans + 1
        return ans
    def contentForAbbasiTable2(self):
        column1 = self.current.startYear
        column2 = self.current.endYear
        column3 = self.cumulativeNumberOfAuthors()
        column4 = self.numberOfNewAuthors()
        
        column5 = self.numberOfNewAuthorsAttachedToAtLeastANewAuthor()
        if(column4 != 0):
            column6 = int((float(column5)/float(column4)) * 100.00)
        else:
            column6 = 0
            
        column7 = self.numberOfNewAuthorsAttachedToAtLeastAnOldAuthor()
        if(column4 != 0):
            column8 = int((float(column7)/float(column4)) * 100.00)
        else:
            column8 = 0    
        
        column9 = self.numberOfOldAuthorsAttachedToAtLeastANewAuthor()
        if(self.previous.numberOfNodes != 0):
            column10 = int((float(column9)/float(self.previous.numberOfNodes)) * 100.00)
        else:
            column10 = 0
            
        column11 = self.numberOfOldAuthorsAttachedToAtLeastAnOldAuthor()
        if(self.previous.numberOfNodes != 0):
            column12 = int((float(column11)/float(self.previous.numberOfNodes)) * 100.00)
        else:
            column12 = 0
            
        column13 = self.numberOfOldAuthorsAttachedToAtLeastAnAuthor()
        if(self.previous.numberOfNodes != 0):
            column14 = int((float(column13)/float(self.previous.numberOfNodes)) * 100.00)
        else:
            column14 = 0
        
        return (column1, column2, column3, column4, column5, column6, column7, column8, column9, column10, column11, column12, column13, column14 )
        
    def contentForAbbasiTable3(self):
        column1 = self.current.startYear
        column2 = self.current.endYear
        column3 = self.current.numberOfEdges + self.previous.numberOfEdges
        column4 = self.current.numberOfEdges
        x = self.current.numberOfEdges
        column5 = self.numberOfNewLinksAmongNewAuthors()
        column6 = int(((float(column5))/(float(x)))*100.00)
        column7 = self.numberOfNewLinksBetweenNewAndOldAuthors()
        column8 = int(((float(column7))/(float(x)))*100.00)
        column9 = self.numberOfLinksBetweenOldAuthorsNotConnectedBefore()
        column10 = int(((float(column9))/(float(x)))*100.00)
        column11 = self.numberOfLinksBetweenOldAuthorsConnectedBefore()
        column12 = int(((float(column11))/(float(x)))*100.00)
        
        return (column1, column2, column3, column4, column5, column6, column7, column8, column9, column10, column11, column12)
        
    def getNewAuthorLinks(self):
        dcVna = {}
        for author in self.commonNodes:
            count = 0
            for edge in self.current.edges:
                if((edge[0]==author and edge[1] in self.newNodes) or (edge[1]==author and edge[0] in self.newNodes)):
                    count = count + 1
            dcVna[author] = count
        return dcVna
    
    def getNewLinks(self):
        dcVnl = {}
        #print self.newNodes
        for author in self.commonNodes:
            dcVnl[author] = self.current.degrees[author]
        return dcVnl
    
    def getOldAuthorLinks(self):
        dcVoa = {}
        for author in self.commonNodes:
            count = 0
            for edge in self.current.edges:
                if((edge[0]==author and edge[1] in self.commonNodes) or (edge[1]==author and edge[0] in self.commonNodes)):
                    count = count + 1
            dcVoa[author] = count
        return dcVoa
    
    def getReadyForCentralityMeasures(self):
        self.previous.makeCoauthorshipGraph()
        self.dcVna = self.getNewAuthorLinks()
        self. dcVoa = self.getOldAuthorLinks()
        
    def getDataForDegreeCentralityVsLinkAssociations(self):
        x = self.previous.getDegreeCentrality()
        OUTPUT_DIR = OUTPUT_STATISTICS_DIRECTORY + '/DegreeCentrality/' 
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)
            print('New directory made: ' + str(OUTPUT_DIR))
        s = OUTPUT_DIR + '/DegreeCentrality_' + str(self.previous.startYear) + '-' + str(self.previous.endYear)+'.txt'
        out = open(s,'w')
        for e in x:
            out.write(str(e) + '; ' + str(x[e]) + '\n')
        out.close()
        #print x
        #pdb.set_trace()    
        if(len(x) > 0):
            X = []
            Y = []
            for author in self.commonNodes:
                X.append(x[author])
                Y.append(self.current.degrees[author])
            corrDVL = scipy.stats.spearmanr(X,Y)
            X = []
            Y = []
            for author in self.commonNodes:
                X.append(x[author])
                Y.append(self.dcVna[author])
            corrDVNL = scipy.stats.spearmanr(X,Y)
            X = []
            Y = []
            for author in self.commonNodes:
                X.append(x[author])
                Y.append(self.dcVoa[author])
            corrDVOL = scipy.stats.spearmanr(X,Y)
        else:
            corrDVL = [0.0,0.0]
            corrDVNL = [0.0,0.0]
            corrDVOL = [0.0,0.0]
            
        #pdb.set_trace()
        return (self.current.startYear, self.current.endYear, corrDVL[0],corrDVNL[0],corrDVOL[0])
        
    def getDataForClosenessCentralityVsLinkAssociations(self):
        x = self.previous.getClosenessCentrality()
        OUTPUT_DIR = OUTPUT_STATISTICS_DIRECTORY + '/ClosenessCentrality/' 
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)
            print('New directory made: ' + str(OUTPUT_DIR))
        s = OUTPUT_DIR + '/ClosenessCentrality_' + str(self.previous.startYear) + '-' + str(self.previous.endYear)+'.txt'
        out = open(s,'w')
        for e in x:
            out.write(str(e) + '; ' + str(x[e]) + '\n')
        out.close()    
        #pdb.set_trace()    
        if(len(x) > 0):
            X = []
            Y = []
            for author in self.commonNodes:
                X.append(x[author])
                Y.append(self.current.degrees[author])
            corrDVL = scipy.stats.spearmanr(X,Y)
            X = []
            Y = []
            for author in self.commonNodes:
                X.append(x[author])
                Y.append(self.dcVna[author])
            corrDVNL = scipy.stats.spearmanr(X,Y)
            X = []
            Y = []
            for author in self.commonNodes:
                X.append(x[author])
                Y.append(self.dcVoa[author])
            corrDVOL = scipy.stats.spearmanr(X,Y)
        else:
            corrDVL = [0.0,0.0]
            corrDVNL = [0.0,0.0]
            corrDVOL = [0.0,0.0]
            
        #pdb.set_trace()
        return (self.current.startYear, self.current.endYear, corrDVL[0],corrDVNL[0],corrDVOL[0])
    
    def getDataForBetweennessCentralityVsLinkAssociations(self):
        x = self.previous.getBetweennessCentrality()
        OUTPUT_DIR = OUTPUT_STATISTICS_DIRECTORY + '/BetweennessCentrality/' 
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)
            print('New directory made: ' + str(OUTPUT_DIR))
        s = OUTPUT_DIR + '/BetweennessCentrality_' + str(self.previous.startYear) + '-' + str(self.previous.endYear)+'.txt'
        out = open(s,'w')
        for e in x:
            out.write(str(e) + '; ' + str(x[e]) + '\n')
        out.close()    
        #pdb.set_trace()    
        if(len(x) > 0):
            X = []
            Y = []
            for author in self.commonNodes:
                X.append(x[author])
                Y.append(self.current.degrees[author])
            corrDVL = scipy.stats.spearmanr(X,Y)
            X = []
            Y = []
            for author in self.commonNodes:
                X.append(x[author])
                Y.append(self.dcVna[author])
            corrDVNL = scipy.stats.spearmanr(X,Y)
            X = []
            Y = []
            for author in self.commonNodes:
                X.append(x[author])
                Y.append(self.dcVoa[author])
            corrDVOL = scipy.stats.spearmanr(X,Y)
        else:
            corrDVL = [0.0,0.0]
            corrDVNL = [0.0,0.0]
            corrDVOL = [0.0,0.0]
            
        #pdb.set_trace()
        return (self.current.startYear, self.current.endYear, corrDVL[0],corrDVNL[0],corrDVOL[0])
    

    
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
    
    print 'Setting Input and output path ...'
    communities_directory = '../..' 
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
            OUTPUT_PARENT_DIRECTORY_PATH = '.'
            print OUTPUT_PARENT_DIRECTORY_PATH
        elif(line[0:10] == 'DATA_PATH='):
            INPUT_REDUCED_FILE_PATH = './reducedData.txt'
            print INPUT_REDUCED_FILE_PATH

    OUTPUT_NETWORK_DIRECTORY_FOR_PAJEK = OUTPUT_PARENT_DIRECTORY_PATH + '/nwa-' + str(FIELD) + '/' + 'runs/' + str(RUN) + '/output/networks/' + str(FIELD) + str(RUN) + str(TYPE) + str(START_YEAR) + '-' + str(END_YEAR) + '_' + str(SIZE) +'years-network_files'
    if not os.path.exists(OUTPUT_NETWORK_DIRECTORY_FOR_PAJEK):
        os.makedirs(OUTPUT_NETWORK_DIRECTORY_FOR_PAJEK)
        print('New directory made: ' + str(OUTPUT_NETWORK_DIRECTORY_FOR_PAJEK))
    
    OUTPUT_STATISTICS_DIRECTORY = OUTPUT_PARENT_DIRECTORY_PATH + '/nwa-' + str(FIELD) + '/' + 'runs/' + str(RUN) + '/output/statistics/' + str(FIELD) + str(RUN) + str(TYPE) + str(START_YEAR) + '-' + str(END_YEAR) + '_' + str(SIZE) + 'years-statistics_files'
    if not os.path.exists(OUTPUT_STATISTICS_DIRECTORY):
        os.makedirs(OUTPUT_STATISTICS_DIRECTORY)
        print('New directory made: ' + str(OUTPUT_STATISTICS_DIRECTORY))
    print 'path setting completed !!'
    
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
            
def makeTemporalDataFilesForAbbasi():
    global TYPE
    global START_YEAR
    global SIZE
    global OUTPUT_NETWORK_DIRECTORY_FOR_PAJEK
    global OUTPUT_STATISTICS_DIRECTORY
    global FIELD
    global RUN
    global END_YEAR
    
    print 'Started gathering data for Abbasi ...'
    
    N = Network()
    N.makeCoauthorshipNetworkFromFile(INPUT_REDUCED_FILE_PATH)
    
    Table2file = OUTPUT_STATISTICS_DIRECTORY + '/'+ str(FIELD) + str(RUN) + str(TYPE) + str(START_YEAR) + '-' + str(END_YEAR) + '_' + str(SIZE) +'years-AbbasiTable2.csv'
    Table2 = open(Table2file, 'w')
    Table2.write('Start_Year; End_Year; Cumulative_No_of_Authors; No_of_New_Authors; No_Of_New_Authors_Connected_to_atleast_one_new_author; Percent_Of_New_Authors_Connected_to_atleast_one_new_author; No_Of_New_Authors_Connected_to_atleast_one_old_author; Percent_Of_New_Authors_Connected_to_atleast_one_old_author; No_Of_Old_Authors_Connected_to_atleast_one_new_author; Percent_Of_Old_Authors_Connected_to_atleast_one_new_author; No_Of_Old_Authors_Connected_to_atleast_one_old_author; Percent_Of_Old_Authors_Connected_to_atleast_one_old_author; No_Of_Old_Authors_Connected_to_atleast_one_any_author; Percent_Of_Old_Authors_Connected_to_atleast_one_any_author\n')
    Table3file = OUTPUT_STATISTICS_DIRECTORY + '/'+ str(FIELD) + str(RUN) + str(TYPE) + str(START_YEAR) + '-' + str(END_YEAR) + '_' + str(SIZE) +'years-AbbasiTable3.csv'
    Table3 = open(Table3file, 'w')
    Table3.write('Start_Year; End_Year; Cumulative_Number_of_Links; Number_of_New_Links; Number_of_New_Links_Among_New_Authors; Percent_of_New_Links_Among_New_Authors; Number_of_New_Links_Between_Two_Old_Authors_Not_Connected_Before; Percent_of_New_Links_Between_Two_Old_Authors_Not_Connected_Before; Number_of_Links_Among_Old_Authors_Connected_Before\n')
    Table4file = OUTPUT_STATISTICS_DIRECTORY + '/'+ str(FIELD) + str(RUN) + str(TYPE) + str(START_YEAR) + '-' + str(END_YEAR) + '_' + str(SIZE) +'years-DegreeCentrality.csv'
    Table4 = open(Table4file, 'w')
    Table4.write('Start_Year; End_Year; Correlation_Betwwen_Prev_Degree_and_New_Degree; Correlation_Betwwen_Prev_Degree_and_New_Authors_Degree; Correlation_Betwwen_Prev_Degree_and_New_Old_Degree\n')
    Table5file = OUTPUT_STATISTICS_DIRECTORY + '/'+ str(FIELD) + str(RUN) + str(TYPE) + str(START_YEAR) + '-' + str(END_YEAR) + '_' + str(SIZE) +'years-ClosenessCentrality.csv'
    Table5 = open(Table5file, 'w')
    Table5.write('Start_Year; End_Year; Correlation_Betwwen_Prev_Closeness_and_New_Degree; Correlation_Betwwen_Prev_Closeness_and_New_Authors_Degree; Correlation_Betwwen_Prev_Closeness_and_New_Old_Degree\n')
    Table6file = OUTPUT_STATISTICS_DIRECTORY + '/'+ str(FIELD) + str(RUN) + str(TYPE) + str(START_YEAR) + '-' + str(END_YEAR) + '_' + str(SIZE) +'years-BetweennessCentrality.csv'
    Table6 = open(Table6file, 'w')
    Table6.write('Start_Year; End_Year; Correlation_Betwwen_Prev_Betweenness_and_New_Degree; Correlation_Betwwen_Prev_Betweenness_and_New_Authors_Degree; Correlation_Betwwen_Prev_Betweenness_and_New_Old_Degree\n')
    
    print 'Making Table2 and Table3 ...'
    y1 = START_YEAR
    y2 = y1 + SIZE -1
    while(y2<=END_YEAR):
        if(I_WANT_ABBASI_TABLE_2_3 == True):
            old = Network()
            old.makeSubCoauthorshipNetworkFromSuperCoauthorshipNetwork(N, START_YEAR, y1-1)
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
        y1 = y2 + 1
        y2 = y1 + SIZE -1
    Table2.close()
    Table3.close()
    print 'Finished making Table2 and Table 3!!'
    
    #Degree Centrality Correlations
    print 'Started Computing Degree Centrality correlation ...'
    y1 = START_YEAR
    y2 = y1 + SIZE -1    
    while(y2<=END_YEAR):
        if(I_WANT_DEGREE_CENTRALITY == True):
            old = Network()
            old.makeSubCoauthorshipNetworkFromSuperCoauthorshipNetwork(N, START_YEAR, y1-1)
            new = Network()
            new.makeSubCoauthorshipNetworkFromSuperCoauthorshipNetwork(N, y1, y2)
            C = Comparer(old, new) 
            C.getReadyForCentralityMeasures()
            (column1, column2, column3, column4, column5) =  C.getDataForDegreeCentralityVsLinkAssociations()
            print column1, column2, column3, column4, column5
            Table4.write(str(column1) +';'+str(column2) +';'+str(column3) +';'+str(column4) +';'+str(column5) + '\n')
        else:
            Table4.write('0; 0; 0; 0; 0\n')
        y1 = y2 + 1
        y2 = y1 + SIZE -1
    Table4.close()
    print "Computation for Degree Centrality is completed"
    
    #Closeness Centrality Correlations
    print 'Started Computing Closeness Centrality correlation ...'
    y1 = START_YEAR
    y2 = y1 + SIZE -1    
    while(y2<=END_YEAR):
        if(I_WANT_CLOSENESS_CENTRALITY == True):
            old = Network()
            old.makeSubCoauthorshipNetworkFromSuperCoauthorshipNetwork(N, START_YEAR, y1-1)
            new = Network()
            new.makeSubCoauthorshipNetworkFromSuperCoauthorshipNetwork(N, y1, y2)
            C = Comparer(old, new) 
            C.getReadyForCentralityMeasures()
            (column1, column2, column3, column4, column5) =  C.getDataForClosenessCentralityVsLinkAssociations()
            print column1, column2, column3, column4, column5
            Table5.write(str(column1) +';'+str(column2) +';'+str(column3) +';'+str(column4) +';'+str(column5) + '\n')
        else:
            Table5.write('0; 0; 0; 0; 0\n')
        y1 = y2 + 1
        y2 = y1 + SIZE -1
    Table4.close()
    Table5.close()
    print "Computation for Closeness Centrality is completed"
    
    #Betweenness Centrality Correlations
    print 'Started Computing Betweenness Centrality correlation ...'
    y1 = START_YEAR
    y2 = y1 + SIZE -1
    while(y2<=END_YEAR):
        if(I_WANT_BETWEENNESS_CENTRALITY == True):
            old = Network()
            old.makeSubCoauthorshipNetworkFromSuperCoauthorshipNetwork(N, START_YEAR, y1-1)
            new = Network()
            new.makeSubCoauthorshipNetworkFromSuperCoauthorshipNetwork(N, y1, y2)
            C = Comparer(old, new)  
            C.getReadyForCentralityMeasures()
            (column1, column2, column3, column4, column5) =  C.getDataForBetweennessCentralityVsLinkAssociations()
            print column1, column2, column3, column4, column5
            Table6.write(str(column1) +';'+str(column2) +';'+str(column3) +';'+str(column4) +';'+str(column5) + '\n')
        else:
            Table6.write('0; 0; 0; 0; 0\n')
        y1 = y2 + 1
        y2 = y1 + SIZE -1
    Table6.close()
    print "Computation for Betweenness Centrality is completed"
    
def makeCollaborationDistributionFile():
    global TYPE
    global START_YEAR
    global SIZE
    global OUTPUT_NETWORK_DIRECTORY_FOR_PAJEK
    global FIELD
    global RUN
    global END_YEAR
    global OUTPUT_STATISTICS_DIRECTORY
    
    print 'Gathering data for collaboration distribution over the time ...'
    
    Mfile = OUTPUT_STATISTICS_DIRECTORY + '/'+ str(FIELD) + str(RUN) + str(TYPE) + str(START_YEAR) + '-' + str(END_YEAR) + '_' + str(SIZE) +'CollaborationDistribution.csv'
    MF = open(Mfile, 'w')
    MF.write('Collaborators; Frequency\n')
    N = Network()
    N.makeCoauthorshipNetworkFromFile(INPUT_REDUCED_FILE_PATH)
    X = N.getCollaborationDistribution()
    for k in X:
        MF.write(str(k) + ';' + str(X[k]) + '\n')
    MF.close()
    print 'Finished gathering data for collaboration distribution!!'
    
def makeGeneralNetworkDataFile():
    global TYPE
    global START_YEAR
    global SIZE
    global OUTPUT_NETWORK_DIRECTORY_FOR_PAJEK
    global FIELD
    global RUN
    global END_YEAR
    
    print 'Gathering the general information of the total network ...'
    
    Mfile = OUTPUT_STATISTICS_DIRECTORY + '/'+ str(FIELD) + str(RUN) + str(TYPE) + str(START_YEAR) + '-' + str(END_YEAR) + '_' + str(SIZE) +'GeneralInfo.csv'
    MF = open(Mfile, 'w')
    MF.write('Start_Year; End_Year; Number_Of_Papers; Number_Of_Authors; Number_Of_Edges; Number_of_Unweighted_Edges\n')
    N = Network()
    N.makeCoauthorshipNetworkFromFile(INPUT_REDUCED_FILE_PATH)
    if(TYPE == 'discrete'):
        start = START_YEAR
        end = start + SIZE -1
        while(end<=END_YEAR):
            Partition = Network()
            Partition.makeSubCoauthorshipNetworkFromSuperCoauthorshipNetwork(N, start, end)
            (col1, col2, col3, col4, col5, col6) = Partition.getGeneralInfo()
            MF.write(str(col1) + ';' + str(col2) + ';' + str(col3) + ';' + str(col4) + ';' + str(col5) + ';' + str(col6) + '\n' )
            start = end + 1
            end = end + SIZE
    elif(TYPE == 'accumulative'):
        start = START_YEAR
        end = start + SIZE -1
        while(end<=END_YEAR):
            Partition = Network()
            Partition.makeSubCoauthorshipNetworkFromSuperCoauthorshipNetwork(N, start, end)
            (col1, col2, col3, col4, col5, col6) = Partition.getGeneralInfo()
            MF.write(str(col1) + ';' + str(col2) + ';' + str(col3) + ';' + str(col4) + ';' + str(col5) + ';' + str(col6) + '\n' )
            end = end + SIZE
    elif(TYPE == 'sliding'):
        start = START_YEAR
        end = start + SIZE -1
        while(end<=END_YEAR):
            Partition = Network()
            Partition.makeSubCoauthorshipNetworkFromSuperCoauthorshipNetwork(N, start, end)
            (col1, col2, col3, col4, col5, col6) = Partition.getGeneralInfo()
            MF.write(str(col1) + ';' + str(col2) + ';' + str(col3) + ';' + str(col4) + ';' + str(col5) + ';' + str(col6) + '\n' )
            start = start + 1
            end = end + 1
    MF.close()
    print 'Finished gathering the general information !!'
    
if __name__ == "__main__":
    setFilePaths()
    makeGeneralNetworkDataFile()
    #makeCoauthorshipNetworkFilesForPajek()
    #makeCollaborationDistributionFile()
    makeTemporalDataFilesForAbbasi()
    