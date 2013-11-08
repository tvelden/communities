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
    # numberOfEdges: Number of total Links (if there are 3 links beteen 2 authors, that will contribute 3 to this total)
    # startYear
    # endYear
    # refList: the dictionary of the reference and the times of appearance
    # countRefList: the papers coupling

    # --Procedures--
    # readPapersFromFiles: read all the papers from the input file
    # makeBiblioCouplingNetworkFromFile: to build the network from file
    # makeBiblioCouplingNetworkFromPapers: to build the network from papers
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
        self.countRefList = []
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

    def makeBiblioCouplingNetworkFromFile(self, file):
        self.readPapersFromFile(file)
        #self.printReferenceList()
        self.makeWeightedBiblioCouplingNetworkFromPapers()
        #self.printFrequencyOfCouplingPapers()
        #self.makeGraph()

    def printReferenceList(self):   #print the sorted reference list
        fsref ='../../../results/reflist.txt'
        fsfreq= '../../../results/reffreq.txt'
        fsff= '../../../results/reff.txt'
        outReflist  = open (fsref, 'w')
        outReffreq = open (fsfreq, 'w')
        outReff = open (fsff, 'w')
        #sorted_refList = sorted(self.refList.iteritems(), key=operator.itemgetter(1))
        for pap in sorted(self.refList, key=self.refList.get, reverse = True):
            outReflist.write( pap + ' ')
            outReflist.write( str(self.refList[pap]) + '\n')
        tot = 0
        cur = 1
        for pap in sorted(self.refList, key=self.refList.get):
            outReffreq.write(str(self.refList[pap]) + '\n')
            if (self.refList[pap] == cur):
                tot = tot + 1
            else:
                outReff.write( str(cur) + ' ' + str(tot) + '\n')
                tot = 1
                cur = self.refList[pap]
        outReff.write( str(cur) + ' ' + str(tot) + '\n')
        outReff.close()
        outReflist.close()
        outReffreq.close()

    def makeBiblioCouplingNetworkFromPapers(self):
        self.nodes = []
        self.numberOfNodes = len(self.papers)
        self.degrees = []
        for i in range(self.numberOfNodes):
        	self.degrees.append(0)
        self.endYear = 2011
        self.startYear = 1990
        for i in range(len(self.papers)):
            self.nodes.append(self.papers[i].ID)
            for j in range(i+1, len(self.papers),1):
                p1 = self.papers[i]
                p2 = self.papers[j]
                sameRef = 0  # the number of same references
                for s1 in p1.RF:
                    for s2 in p2.RF:
                        if (s1==s2):
                            sameRef = sameRef + 1
                if ( sameRef == 0 ):
                    continue
                sim = sameRef / (math.sqrt(len(p1.RF)) * math.sqrt(len(p2.RF)))
                self.edges.append([i,j,sim])
                self.numberOfEdges = self.numberOfEdges + 1
                self.degrees[i] = self.degrees[i] + 1
                self.degrees[j] = self.degrees[j] + 1
        print "Building Complete"

    def makeWeightedBiblioCouplingNetworkFromPapers(self): #also write the points of scatterplot to evaluate if the tf-idf scheme works
        # fscatt='../../../results/scatterplotinput.txt'
        # outfilescatt=open(fscatt,'w')
        # fscatt2='../../../results/scatterplotinput2.txt'
        # outfilescatt2=open(fscatt2,'w')
        # fsOne='../../../results/FrequencyOfOneCouplingPaper.txt'
        # outfsOne=open(fsOne,'w')
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
            flag =0 # if the paper is related to other papers
            for j in range(i+1, len(self.papers),1):
                p1 = self.papers[i]
                p2 = self.papers[j]
                sumDe = 0 # denominater of similarity
                sumDeNoWeight=0
                sumNo1 = 0 # nominater of paper1
                sumNo2 = 0 # nominater of paper2
                for s1 in p1.RF:
                    for s2 in p2.RF:
                        if (s1==s2):
                            sumDeNoWeight = sumDeNoWeight + 1
                            record = s1
                            if (self.countRefList.count(s1)==0 ):
                                self.countRefList.append(s1)
                            sumDe = sumDe + 1 / ((math.log10(self.refList[s1]) + 1) * (math.log10(self.refList[s2]) + 1))
                for s1 in p1.RF:
                    sumNo1 = sumNo1 + 1 / ( (math.log10(self.refList[s1]) + 1) * (math.log10(self.refList[s1]) + 1) )
                for s2 in p2.RF:
                	sumNo2 = sumNo2 + 1 / ( (math.log10(self.refList[s2]) + 1) * (math.log10(self.refList[s2]) + 1) )
                if ( sumDe == 0 ):
                    continue
                flag = 1
                # if ( sumDeNoWeight == 1 ):
                #     #outfsOne.write(str(record) + ' ')
                #     outfsOne.write(str(self.refList[record]) + '\n')
                sim = sumDe / (math.sqrt(sumNo1) * math.sqrt(sumNo2))
                # outfilescatt.write(str(sim) + ' ' + str(sumDe) + '\n')
                # outfilescatt2.write(str(sim) + ' ' + str(sumDeNoWeight) + '\n')
                self.edges.append([i,j,sim])
                self.numberOfEdges = self.numberOfEdges + 1
                self.degrees[i] = self.degrees[i] + 1
                self.degrees[j] = self.degrees[j] + 1
            #if (flag == 0 ):
                #print self.papers[i].ID
        #outfsOne.close()
        #outfilescatt.close()
        #outfilescatt2.close()
        print "Building Complete"

    def printNetworkForPajek(self,File):
        fs = str(File)
        #fsd = "../../../results/SimilarityDistribution.txt" #print the similarity distribution
        outFile = open(fs, 'w')
        #outFileSimDis = open(fsd,'w')
        outFile.write('*Vertices ' + str(self.numberOfNodes) + '\n') 
        inde = 1
        for node in self.nodes:
            outFile.write(str(inde) + ' ' + '"'+ node + '"'+ '\n')
            inde = inde + 1
        #outFile.write('\n')
        outFile.write('*Edges' + '\n')
        for edge in self.edges:
            outFile.write(str(edge[0] + 1) + ' ' + str(edge[1] + 1) + ' ' + str(edge[2]) + '\n')
        #    outFileSimDis.write(str(edge[2]) + '\n')
        outFile.close()
        #outFileSimDis.close()
        print "Printing Complete"

    def printFrequencyOfCouplingPapers(self):
        print "Print Frequency of Coupling papers"
        fcp = '../../../results/FrequencyOfCouplingPapers.txt'
        outFileFcp = open(fcp,'w')
        for s in self.countRefList:
            outFileFcp.write(str(self.refList[s]) + '\n')
        outFileFcp.close()

if __name__ == "__main__":
    N= Network()
    default = '../../../nwa-ACMSIGMOD/data/re_output_mod.txt'
    N.makeBiblioCouplingNetworkFromFile(sys.argv[1])
    default2 = '../../../WeightedBiblioCouplingNetwork.net'
    N.printNetworkForPajek(sys.argv[2])

