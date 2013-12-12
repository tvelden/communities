#Construct the topic affinity network based on both citation and authors for a sliding steps with a certain window
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
        self.label= 0 #label of clusters (after two rounds of clustering)

class cluster:
    def __init__(self):
        self.label = 0 #label of this cluster
        self.numberOfPapers = 0 #number of papers in this cluster
        self.listOfPapers = [] #list of papers in this cluster
        self.journalFre = {} #the frequency of names of journals in this cluster
        self.numOfAuthors = 0 #number of authors in this cluster
        self.listOfAuthors = [] #list of authors in this cluster
        self.yearListOfPapers = {} #list of papers each year
        self.yearListOfAuthors = {} #List of authors each year

class clustersNetwork:
    def __init__(self):
        self.papers = [] #list of papers
        self.IDmatchLabel = {} # a match between IDs and Labels
        self.clusters = {} # the list of clusters
        self.numberOfClusters = 0 # the number of clusters

    def readIDmatchLabel(self,IDs,Labels): #map between IDs and Labels
        LabelInput = open(str(Labels) , 'r')
        i = 0
        LabelMap = {}
        for lines in LabelInput:
            i = i + 1
            if (i == 1): continue
            LabelMap[i-1] = int(lines)
        LabelInput.close()            
        idInput = open(str(IDs), 'r')
        i = 0
        for lines in idInput:
            k = lines.split('"')
            if (len(k) <= 1):
                continue
            else:
                i = i + 1
                self.IDmatchLabel[k[1]] = LabelMap[i]
        print 'Match Complete'

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
                if p.ID in self.IDmatchLabel:
                    p.label = self.IDmatchLabel[p.ID]
                if p.label>self.numberOfClusters:
                    self.numberOfClusters = p.label
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
        print 'Read Complete'

    def buildClusters(self):
        for i in range(self.numberOfClusters):
            cc = cluster()
            cc.label = i + 1
            self.clusters[i+1] = cc
        for paper in self.papers:
            if (paper.label == 0): continue
            self.clusters[paper.label].listOfPapers.append(paper)
            self.clusters[paper.label].numberOfPapers += 1
            if (paper.SO != ''):
                if paper.SO in self.clusters[paper.label].journalFre:
                    self.clusters[paper.label].journalFre[paper.SO] +=1
                else:
                    self.clusters[paper.label].journalFre[paper.SO] = 1

            for author in paper.AU:
                if author in self.clusters[paper.label].listOfAuthors:
                    continue
                else:
                    self.clusters[paper.label].listOfAuthors.append(author)
            if paper.YR in self.clusters[paper.label].yearListOfPapers:
                if paper in self.clusters[paper.label].yearListOfPapers[paper.YR]:
                    continue
                self.clusters[paper.label].yearListOfPapers[paper.YR].append(paper)
            else:
            	self.clusters[paper.label].yearListOfPapers[paper.YR] = []
            	self.clusters[paper.label].yearListOfPapers[paper.YR].append(paper)
            if paper.YR in self.clusters[paper.label].yearListOfAuthors:
            	for au in paper.AU:
                    if au in self.clusters[paper.label].yearListOfAuthors[paper.YR]:
                        continue
                    self.clusters[paper.label].yearListOfAuthors[paper.YR].append(au)
            else:
            	self.clusters[paper.label].yearListOfAuthors[paper.YR] = []
            	for au in paper.AU:
                    self.clusters[paper.label].yearListOfAuthors[paper.YR].append(au)
        self.numberOfClusters = len(self.clusters)
        for i in range(self.numberOfClusters):
            i += 1
            self.clusters[i].numberOfPapers = len(self.clusters[i].listOfPapers)
            self.clusters[i].numOfAuthors = len(self.clusters[i].listOfAuthors)
            self.clusters[i].label = i
        print 'Build Complete'

    def AffinityBuild(self):
    	soc="../../../../../Dropbox/Files/Affinity/"
        for startyear in range(1991,1992):
            endyear = startyear + 19
            outFile1 = open( soc + "Citation " + str(startyear) + "-" + str(endyear)+".net",'w')
            outFile2 = open( soc + "Authors " + str(startyear) + "-" + str(endyear)+".net",'w')
            outFile3 = open( soc + "NumberOfPapers" + str(startyear) + "-" +str(endyear),'w')
            outFile4 = open( soc + "NumberOfAuthors" + str(startyear) + "-" +str(endyear),'w')
            outFile5 = open( soc + "NumberOfSharedAuthors" + str(startyear) + "-" +str(endyear),'w')
            outFile6 = open( soc + "NumberOfCitatoin" + str(startyear) + "-" +str(endyear),'w')
            outFile1.write("*Vertices 12\n")
            for i in range(1,13):
                outFile1.write(str(i) + " "+ '"Area' + str(i) + '"\n')
            outFile1.write("*Arcs\n")
            outFile2.write("*Vertices 12\n")
            for i in range(1,13):
                outFile2.write(str(i) + " "+ '"Area' + str(i) + '"\n')
            outFile2.write("*Arcs\n")
            paperList = {} # the paper list of every cluster in this five years
            paperListID = {} # paperListID list
            authorList = {} # the author list of every cluster in the five years
            totalNumberOfPapers = 0
            totalNumberOfAuthors = 0
            for i in range(1,self.numberOfClusters+1):   #top 12 areas
                clu = self.clusters[i]
                paperList[i] = []
                authorList[i] = []
                paperListID[i] = []
                for year in range(startyear,endyear+1):
                    if (year in clu.yearListOfPapers):
                        paperList[i] = list(set(paperList[i]) | set(clu.yearListOfPapers[year]))
                        for paper in clu.yearListOfPapers[year]:
                            paperListID[i].append(paper.ID)
                    if (year in clu.yearListOfAuthors):
                        authorList[i] = list(set(authorList[i]) | set(clu.yearListOfAuthors[year]))
                outFile3.write(str(len(paperList[i]))+"\n")
                outFile4.write(str(len(authorList[i]))+"\n")
                totalNumberOfPapers += len(paperList[i])
                totalNumberOfAuthors += len(authorList[i])
                print i,len(paperList[i]),len(authorList[i])
            print totalNumberOfPapers,totalNumberOfAuthors
            CitationMatrix = [[0 for x in xrange(30)] for x in xrange(30)] 
            AuthorMatrix = [[0 for x in xrange(30)] for x in xrange(30)] 
            print startyear

            for i in range(1,self.numberOfClusters+1):
                for paper in paperList[i]:
                    for ref in paper.RF:
                    	for j in range(1,self.numberOfClusters+1):
                    		if (i==j): continue
                    		if (ref in paperListID[j]):
                    			CitationMatrix[i][j] +=1
                for j in range(1,self.numberOfClusters+1):
                    if (i==j): continue
                    AuthorMatrix[i][j] = len(list(set(authorList[i]) & set(authorList[j])))
            for i in range(1,self.numberOfClusters+1):
                totCitation = 0
                totSharedAuthors = 0
                if (i<=13) and (i!=1):
                    outFile6.write("\n")
                    outFile5.write("\n")
                for j in range(1,self.numberOfClusters+1):
                    if (i==j): continue
                    totCitation += CitationMatrix[i][j]
                    totSharedAuthors += AuthorMatrix[i][j]
                for j in range(1,self.numberOfClusters+1):
                    if (i>12): continue
                    if (j>12): continue
                    if (i==j):
                        outFile6.write("0	") 
                        outFile5.write("0	")
                        continue
                    # Citation Based
                    ExpectedRate = float(len(paperList[j])) / float(totalNumberOfPapers-len(paperList[i]))
                    ActualRate = float(CitationMatrix[i][j]) / float(totCitation)
                    Residual = (ActualRate - ExpectedRate) / ExpectedRate
                    if (j!=12):
                        outFile6.write(str(CitationMatrix[i][j])+"	")
                    else:
                        outFile6.write(str(CitationMatrix[i][j]))
                    if (Residual>0):
                        outFile1.write(str(i) + ' ' + str(j) + ' ' + str(Residual) + '\n')
                    # Author Based
                    ExpectedRate2 = float(len(authorList[j])) / float(totalNumberOfAuthors-len(authorList[i]))
                    ActualRate2 = float(AuthorMatrix[i][j]) / float(totSharedAuthors)
                    Residual2 = (ActualRate2 - ExpectedRate2) / ExpectedRate2
                    if (j!=12):
                        outFile5.write(str(AuthorMatrix[i][j])+"	")
                    else:
                        outFile5.write(str(AuthorMatrix[i][j]))
                    if (Residual2>0):
                        outFile2.write(str(i) + ' ' + str(j) + ' ' + str(Residual2) + '\n')
            outFile1.close()
            outFile2.close()
            outFile3.close()
            outFile4.close()
            outFile5.close()
            outFile6.close()


if __name__ == "__main__":
    C = clustersNetwork()
    ids ='../../../../../Dropbox/Files/Synthe/DirectCitationNetwork_Modified_GC.net' 
    labels ='../../../../../Dropbox/Files/Synthe/Synthe.clu'
    C.readIDmatchLabel(ids,labels)
    source = '../../../../../Dropbox/Network Build/in-norm-dis-hfree-red.txt'
    C.readPapersFromFile(source)
    C.buildClusters()
    C.AffinityBuild()