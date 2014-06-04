#To count the frequent journal names in each cluster
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
        self.journalResidual = {} #the residual of journals
        self.journalScore = {} #the score of the journals in this cluster
        self.numOfAuthors = 0 #number of authors in this cluster
        self.listOfAuthors = [] #list of authors in this cluster
        self.yearListOfPapers = {} #list of papers each year
        self.yearListOfAuthors = {} #List of authors each year

class clustersNetwork:
    def __init__(self):
        self.papers = [] #list of papers
        self.IDmatchLabel = {} # a match between IDs and Labels
        self.clusters = {} # the list of clusters
        self.journalFre = {} #journal frequency in all the clusters
        self.numberOfClusters = 0 # the number of clusters
        self.numberOfPapers = 0 # number of papers in the clusters

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
            self.numberOfPapers +=1
            if (paper.SO != ''):
                if paper.SO in self.clusters[paper.label].journalFre:
                    self.clusters[paper.label].journalFre[paper.SO] +=1
                else:
                    self.clusters[paper.label].journalFre[paper.SO] = 1
                if paper.SO in self.journalFre:
                    self.journalFre[paper.SO] +=1
                else:
                    self.journalFre[paper.SO] = 1
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

    def printFrequency(self,outfile):
        outFile = open(str(outfile), 'w')
        min = 0
        flag = 0
        for i in range(self.numberOfClusters):
            clu = self.clusters[i+1]
            for jour in clu.journalFre:
                expected = float(self.journalFre[jour] * clu.numberOfPapers)/ float(self.numberOfPapers)
                # if (flag<5):
                #     flag+=1
                #     print self.journalFre[jour],clu.numberOfPapers,self.numberOfPapers
                self.clusters[i+1].journalResidual[jour] = float(clu.journalFre[jour]-expected) / float(expected)
                if (self.clusters[i+1].journalResidual[jour]<min): min = self.clusters[i+1].journalResidual[jour]
        for i in range(self.numberOfClusters):
            clu = self.clusters[i+1]
            for jour in clu.journalFre:
                score = math.log(clu.journalFre[jour]) * (clu.journalResidual[jour]-min)
                self.clusters[i+1].journalScore[jour] = score

        for i in range(self.numberOfClusters):
            clu = self.clusters[i+1]
            outFile.write(str(i+1) + '	' + str(clu.numberOfPapers) + '\n')
            t = 0
            for jour in , re(clu.journalScore, key = clu.journalScore.get, reverse=True):
                t +=1
                outFile.write(jour + '	' + str(clu.journalFre[jour]) +' '+str(clu.journalResidual[jour])+'  '+ str(clu.journalScore[jour])+ '\n')
                if (t>10):
                    break
        outFile.close()
        print 'Print Complete'

    def AuthorPortionYear(self,fromcluster,tocluster): #generate the author portion number of each year
        print 'Author Portion Print Begin'
        source = '../../../../../Dropbox/Files/Results/Annual/Inherit/'
        # outFile1 = open (source + 'AuthorPortionYear From Cluster' + str(fromcluster) + ' To Cluster' +str(tocluster), 'w' )
        # outFile2 = open (source + 'AuthorNumber in Cluster' + str(fromcluster), 'w')
        # for year in range(1991,2011):
        #     if year in self.clusters[fromcluster].yearListOfAuthors :
        #         yearListFrom = self.clusters[fromcluster].yearListOfAuthors[year]
        #     else:
        #         yearListFrom = []
        #     if year in self.clusters[tocluster].yearListOfAuthors :
        #         yearListTo = self.clusters[tocluster].yearListOfAuthors[year]
        #     else:
        #         yearListTo = []
        #     # if (year == 1991):
        #     # 	print yearListFrom
        #     # 	print yearListTo
        #     NOA= len(yearListFrom)
        #     tot = 0
        #     intersect = list(set(yearListFrom) & set(yearListTo))
        #     tot = len(intersect)
        #     # print intersect
        #     # for au in yearListFrom:
        #     #     if au in yearListTo:
        #     #         tot +=1
        #     if (NOA>0):
        #         port = float(tot) / float(NOA)
        #     else:
        #         port = 0
        #     outFile1.write(str(port) + '\n')
        #     outFile2.write(str(year) + '	' + str(NOA) + '\n')
        # outFile1.close()
        # outFile2.close()
        outFile3 = open (source + 'AuthorPortionYear3 From Cluster' + str(fromcluster) + ' To Cluster' +str(tocluster), 'w' )
        for year in range(1992,2010):
            if year in self.clusters[fromcluster].yearListOfAuthors :
                yearListFrom = list(set(self.clusters[fromcluster].yearListOfAuthors[year-1]) | set(self.clusters[fromcluster].yearListOfAuthors[year]) | set(self.clusters[fromcluster].yearListOfAuthors[year+1]))
            else:
                yearListFrom = []
            if year in self.clusters[tocluster].yearListOfAuthors :
                yearListTo = list(set(self.clusters[tocluster].yearListOfAuthors[year-1]) | set(self.clusters[tocluster].yearListOfAuthors[year]) | set(self.clusters[tocluster].yearListOfAuthors[year+1]))
            else:
                yearListTo = []
            # if (year == 1991):
            #   print yearListFrom
            #   print yearListTo
            NOA= len(yearListFrom)
            NOA2 = len(yearListTo)
            tot = 0
            intersect = list(set(yearListFrom) & set(yearListTo))
            outFileKP.write(str(year)+"	"+str(len(intersect))+"	"+"clu"+str(fromcluster)+"--clu"+str(tocluster)+"\n")
            tot = len(intersect)
            # print intersect
            # for au in yearListFrom:
            #     if au in yearListTo:
            #         tot +=1
            if ((NOA>0) and (NOA2>0)):
                port = float(tot) / math.sqrt(float(NOA)*float(NOA2))
            else:
                port = 0
            outFile3.write(str(port) + '\n')
        outFile3.close()
        print 'Author Portion Print Complete'

    def CitationPortionYear(self,fromcluster,tocluster): #generate the citation portion number of each year
        print 'Citation Portion Print Begin'
        source = '../../../../../Dropbox/Files/Results/Annual/'
        outFile1 = open (source + 'Citation Portion From Cluster' + str(fromcluster) + ' To Cluster' +str(tocluster), 'w' )
        outFile2 = open (source + 'Citation Number in Cluster' + str(fromcluster), 'w')
        outFile3 = open (source + 'Paper Number in Cluster' + str(fromcluster), 'w')
        sourceList = []
        for year in range(1991,2011):
            if year in self.clusters[fromcluster].yearListOfPapers:
                yearListFrom = self.clusters[fromcluster].yearListOfPapers[year]
            else:
                yearListFrom = []
            if year in self.clusters[tocluster].yearListOfPapers:
                yearListTo = self.clusters[fromcluster].yearListOfPapers[year]
            else:
                yearListTo = []
            for paper in yearListTo:
                sourceList.append(paper.ID)
            totavg = 0
            NOP = len(yearListFrom) #number of papers
            totcitation = 0 #number of citation
            for paper in yearListFrom:
                amount = len(paper.RF)
                totcitation += amount
                tot = 0
                for ref in paper.RF:
                    if ref in sourceList:
                        tot += 1
                port = float(tot) / float(amount)
                totavg += port
            avg = totavg / float(NOP)
            outFile1.write(str(avg) + '\n')
            outFile2.write(str(year) + '	' + str(totcitation) + '\n')
            outFile3.write(str(year) + '	' + str(NOP) + '\n')
        outFile1.close()
        outFile2.close()
        outFile3.close()
        print 'Citatoin Portion Print Finish'

if __name__ == "__main__":
    C = clustersNetwork()
    ids ='../../../../../Dropbox/Files/Synthe/DirectCitationNetwork_Modified_GC.net' 
    labels ='../../../../../Dropbox/Files/Synthe/Synthe.clu'
    C.readIDmatchLabel(ids,labels)
    source = '../../../../../Dropbox/Network Build/in-norm-dis-hfree-red.txt'
    C.readPapersFromFile(source)
    C.buildClusters()
    outfile = '../../../../../Dropbox/Files/Results/JournalWeighted2.txt'    
    # for i in range(1,13):
    #     outFileKP= open("../../../../../Dropbox/Files/Results/Annual/InstancesOfCluster"+str(i),"w")
    #     outFileKP.write("Year"+"    "+"NoOfAuthors"+"   "+"Label\n")
    #     for j in range(1,13):
    #         if (i==j): continue
    #         C.AuthorPortionYear(i,j)
    #     #C.CitationPortionYear(i,1)
    #     outFileKP.close()
    # max =0 
    # for i in range(1,13):
    #     outFileNA=open("../../../../../Dropbox/Files/Results/Annual/NumberOfAuthorsOfCluster"+str(i),"w")
    #     outFileNA.write("Year"+"	NoOfAuthors"+"\n")
    #     for year in range(1991,2011):
    #         #print i,year
    #         num= len(C.clusters[i].yearListOfAuthors[year])
    #         #print num
    #         if (num>max): max = num
    #         outFileNA.write(str(year)+"	"+str(num)+"\n")
    #     outFileNA.close()
    # print max

    C.printFrequency(outfile)
    




