#LinkExplanation
import os
import sys
import operator
import numpy
import scipy.stats
from operator import itemgetter
import pdb
import math
import networkx as nx

source2 = "/Users/shiyansiadmin/Dropbox/Files/NewField2Data2/in.txt"  #input file

ids = "/Users/shiyansiadmin/Dropbox/Files/NewField2Data2/DirectCitationNetworkGiantComponent.net" # Giantcomponent 
labels = "/Users/shiyansiadmin/Dropbox/Files/NewField2Data2/DirectCitationNetworkGiantComponent_Synthe2.clu" # partition file
top = 11 # top X area

sc = 1
tc = 6

soc = "/Users/shiyansiadmin/Dropbox/Files/NewField2Data2/" +"ExplanationOfLinkFromCluster" + str(sc) + "ToCluster" + str(tc) # output

sourcecluster = []
targetcluster = []
sourceclusterauthorlist = {} # match of author & its frequency in source cluster
targetclusterauthorlist = {} # match of author & its frequency in target cluster
targetclustermatch = {} # match of ID and paper
targetclusterIDTI = {} # match of ID and Title
targetclusterAUID = {} # match of authors and ID

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
        self.listOfAuthors = [] #list of authors in this cluster   (not instances)
        self.yearListOfPapers = {} #list of papers each year
        self.yearListOfAuthors = {} #List of authors each year (instances)
        self.yearListOfAuthorsDisjoin = {} # List of authors each year (not instances)

class clustersNetwork:
    def __init__(self):
        self.papers = [] #list of papers
        self.IDmatchLabel = {} # a match between IDs and Labels
        self.clusters = {} # the list of clusters
        self.numberOfClusters = 0 # the number of clusters

    def readIDmatchLabel(self,IDs,Labels): #map between IDs and Labels
    # change the label from here
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
                if (p.label == tc):
                    targetcluster.append(p)
                    targetclustermatch[p.ID] = p
                    if p.ID in targetclusterIDTI:
                        k =k
                    else:
                        targetclusterIDTI[p.ID] = p.TI
                    for author in p.AU:
                        if author in targetclusterauthorlist:
                            targetclusterauthorlist[author] += 1
                        else:
                            targetclusterauthorlist[author] = 1
                        if author in targetclusterAUID:
                            targetclusterAUID[author].append(p.ID)
                        else:
                            targetclusterAUID[author] = []
                            targetclusterAUID[author].append(p.ID)
                if (p.label == sc):
                    sourcecluster.append(p)
                    for author in p.AU:
                        if author in sourceclusterauthorlist:
                            sourceclusterauthorlist[author] +=1
                        else:
                            sourceclusterauthorlist[author] = 1

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

if __name__ == "__main__":
    k = 0
    C = clustersNetwork()
    C.readIDmatchLabel(ids,labels)
    C.readPapersFromFile(source2)
    outfile = open(soc + "AuthorBased","w")
    outfile.write("Explanation of the link from Cluster" + str(sc) + " to Cluster"+ str(tc) + "\n")
    outfile.write("The Results of SharedAuthor \n")
    outfile.write("Here are the papers that authors from the Cluster" + str(sc) + " write that are belong to Cluster" + str(tc) + "\n")
    idlist = []
    candidates = {} # candidate shared author names
    for p in sourcecluster:
        for author in p.AU:
            if (author in targetclusterauthorlist) and (author in sourceclusterauthorlist):
                if (targetclusterauthorlist[author]>=5) and (sourceclusterauthorlist[author]>=5):
                    if (author in candidates):
                        k = k
                    else:
                        candidates[author] = targetclusterauthorlist[author]
            if author in targetclusterAUID:
                for ids in targetclusterAUID[author]:
                    if ids in idlist:
                        k = k
                    else:
                        idlist.append(ids)
    aucount = {}
    tt = []
    for ids in idlist:
        p = targetclustermatch[ids]
        tt.append(p)
    for p in sorted(tt,key= lambda tt:tt.YR, reverse=False):
        if p.TI!="":
            strti = "TI " + p.TI + "\n"
            outfile.write(strti)
        if p.YR!=0:
            stryr = "YR " + str(p.YR) + "\n"
            outfile.write(stryr)
        if p.SO!="":
            strso = "SO " + str(p.SO) + "\n"
            outfile.write(strso)
        if len(p.AU)!=0:
            outfile.write("AU ")
            for au in p.AU:
            #     if au in aucount:
            #         aucount[au] += 1
            #     else:
            #         aucount[au] = 1
                outfile.write(au + " | ")
            outfile.write("\n")
        if len(p.CA)!=0:
            outfile.write("CA ")
            for ca in p.CA:
                outfile.write(ca + " | ")
            outfile.write("\n")
        outfile.write("\n")
    cc = 0
    # for au in sorted(aucount,key=aucount.get, reverse=True):
    #     cc += 1
    #     if (cc>10):
    #         break
    #     print au,aucount[au]
    for au in sorted(candidates,key=candidates.get,reverse=True):
        cc += 1
        if (cc>10):
            break
        print au,candidates[au]

    outfile.write("The Results of Citation")
    outfile.write("Here are the papers in Cluster" +str(tc) + " cited by papers in Cluster" + str(sc) + "\n")
    outfile.close()

    outfile = open(soc+"CitationBased","w")
    idlist = []
    for p in sourcecluster:
        for ref in p.RF:
            if ref in targetclusterIDTI:
                if ref in idlist:
                    k = k
                else:
                    idlist.append(ref)
    tt = []
    for ids in idlist:
        p = targetclustermatch[ids]
        tt.append(p)
    for p in sorted(tt,key= lambda tt:tt.YR, reverse=False):
        if p.TI!="":
            strti = "TI " + p.TI + "\n"
            outfile.write(strti)
        if p.YR!=0:
            stryr = "YR " + str(p.YR) + "\n"
            outfile.write(stryr)
        if p.SO!="":
            strso = "SO " + str(p.SO) + "\n"
            outfile.write(strso)
        if len(p.AU)!=0:
            outfile.write("AU ")
            for au in p.AU:
                outfile.write(au + " | ")
            outfile.write("\n")
        if len(p.CA)!=0:
            outfile.write("CA ")
            for ca in p.CA:
                outfile.write(ca + " | ")
            outfile.write("\n")
        outfile.write("\n")

    outfile.close()
