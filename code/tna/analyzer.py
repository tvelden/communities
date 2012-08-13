import os
import sys
import operator
import numpy
import scipy.stats
from operator import itemgetter
import pdb
import networkx as nx


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
    
    def printNetworkComponents(self, field, run, type, size, directoryPath):
        
        color = {}
        component = {}
        for node in self.nodes:
            color[node] = 0
            component[node] = 0
            
        alist = {}
        for node in self.nodes:
            alist[node] = []
        for edge in self.differentEdges:
            alist[edge[0]].append(edge[1])
            alist[edge[1]].append(edge[0])
         
        index = 0
        stack = []
        for node in self.nodes:
            if(color[node] == 0):
                color[node] = 1
                index = index + 1
                component[node] = index
                stack.append(node)
                while(len(stack)>0):
                    x = stack.pop()
                    for e in alist[x]:
                        if(color[e] == 0):
                            color[e] = 1
                            component[e] = index
                            stack.append(e)
        #for node in self.nodes:
            #print node, component[node]
        C = {}
        for i in range(1,index + 1):
            C[i] = []
            C[i].append(0)
            C[i].append([])
        for node in self.nodes:
            C[component[node]][0] = C[component[node]][0] + 1
            C[component[node]][1].append(node)
            
        sortedComponentList = sorted(C.items(), key = itemgetter(1), reverse = True)
        SL = []
        for e in sortedComponentList:
            #print e[1][0]
            SL.append(e)
        #print SL[0][1][0]
        
        #making the component file
        fsd = directoryPath + '/' + str(type) + str(self.startYear) + '-' + str(self.endYear) + '_' + str(size) + 'years/components/pajek'
        if not os.path.exists(fsd):
            os.makedirs(fsd)
        fs = fsd + '/' + str(field) + str(run) + str(type) + '_' + str(self.startYear) + '-' + str(self.endYear) + '_' + str(size) + 'years_components.net'
        out = open(fs, 'w')
        out.write('Number of Vertices:' + str(self.numberOfNodes) + '\n')
        out.write('Number of Components:' +str(index) + '\n')
        out.write('Size of the Largest Compnent:' +str(SL[0][1][0]) + '\n')
        out.write('Size of the Second Largest Compnent:' +str(SL[1][1][0]) + '\n')
        out.write('Components:\n\n')
        i = 0
        for e in SL:
            i = i + 1
            out.write('*Component ' + str(i) + '\n')
            out.write('Size' + str(SL[i-1][1][0]) + '\n')
            for x in SL[i-1][1][1]:
                out.write(str(x) + '\n')
            out.write('\n')
        out.close()
    
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
            print('New directory made: ' + str(directoryPath))

        fsd = directoryPath + '/' + str(type) + str(self.startYear) + '-' + str(self.endYear) + '_' + str(size) + 'years/whole_net/pajek' 
        if not os.path.exists(fsd):
            os.makedirs(fsd)
        fs = fsd + '/' + str(field) + str(run) + str(type) + '_' + str(self.startYear) + '-' + str(self.endYear) + '_' + str(size) + 'years_wholenet.net'
        fsvec = fsd + '/' + str(field) + str(run) + str(type) + '_' + str(self.startYear) + '-' + str(self.endYear) + '_' + str(size) + 'years_wholenet.vec'
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
        outFilevec.close()
        
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
    
    