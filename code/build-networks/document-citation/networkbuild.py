# this is for the networld-building of the bibliographic-network (the document level)
import os
import sys
import operator
import numpy
import scipy.stats
from operator import itemgetter
import pdb
import math
import networkx as nx

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
    # --Variables--
    # papers: array of papers
    # nodes: array of nodes in the network , title of documents
    # numberOfNodes: Number of documents
    # degrees: number of degrees of each nodes
    # edges:  array of Links -> array of triples
    # numberOfEdges: Number of total Links
    # startYear
    # endYear
    # refList: the dictionary of the reference and the times of appearance

    # --Procedures--
    # readPapersFromFiles: read all the papers from the input file
    # makeDirectCitationNetworkFromfile: to build the network from file
    # printNetworkForPajek: to print the Network in the pajek format

    def __init__(self):
        self.papers = [] 
        self.nodes = []
        self.degrees = []
        self.startYear = 0
        self.endYear = 0
        self.numberOfNodes = 0
        self.numberOfEdges = 0
        self.edges = []
        self.refList = {}
        self.G = nx.Graph()

    def readPapersFromFile(self, File):
        self.papers = []
        inFile = open(str(File), "r")
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
                if s in self.refList:
                	self.refList[s] = self.refList[s] + 1
                else:
                	self.refList[s] = 1
            elif(string[0] == 'C' and string[1]=='A'):
                #processing CA
                l = len(string)
                s = string[3:l-1]
                p.CA.append(s)
                
        inFile.close()

    def makeDirectCitationNetworkFromfile(self, file):
        self.readPapersFromFile(file)
        self.makeDirectCitationNetworkFromPapers()
        #self.makeGraph()

    def makeDirectCitationNetworkFromPapers(self): 
        self.nodes = []
        self.numberOfNodes = len(self.papers)
        self.degrees = []
        for i in range(self.numberOfNodes):
        	self.degrees.append(0)
        self.endYear = 2011
        self.startYear = 1990
        for i in range(len(self.papers)):
            self.nodes.append(self.papers[i].ID)
            if (i % 100 == 0):
                print 'node-' + str(i) + ' Complete'
            for j in range(len(self.papers)):  #direct citation network so there may be conditions that node i do not link to node but not vice versa
                flag = 0  # if paper1 related to paper2
                p1 = self.papers[i]
                p2 = self.papers[j]
                for s1 in p1.RF:
                    if (s1==p2.ID):
                        flag = 1
                        break
                if (flag == 0):
                    continue
                self.edges.append([i,j,1])
                self.numberOfEdges = self.numberOfEdges + 1
                self.degrees[i] = self.degrees[i] + 1
                #print self.numberOfEdges
        print "Building Complete"

    def printNetworkForPajek(self,File):
        outFile = open(str(File), 'w')
        
        outFile.write('*Vertices ' + str(self.numberOfNodes) + '\n') 
        inde = 1
        for node in self.nodes:
            outFile.write(str(inde) + ' ' + '"'+ node + '"'+ '\n')
            inde = inde + 1
        #outFile.write('\n')
        outFile.write('*Arcs' + '\n')
        for edge in self.edges:
            outFile.write(str(edge[0] + 1) + ' ' + str(edge[1] + 1) + ' ' + str(edge[2]) + '\n')
        outFile.close()
        print "Printing Complete"

if __name__ == "__main__":
    N= Network()
    default = '../../../nwa-ACMSIGMOD/data/re_output_mod.txt'
    N.makeDirectCitationNetworkFromfile(sys.argv[1])
    default2 = '../../../results/DirectCitationNetwork_Modified.net'
    N.printNetworkForPajek(default2)

