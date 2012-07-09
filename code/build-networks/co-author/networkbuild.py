import os
import sys
import operator
from operator import itemgetter

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
    #edges {}: Dictionary of pairs of author names , number of occurences. {('x','y'):4} !!IMPORATNT!!: x is ALWAYS less than y (alphabetically
    #numberOfEdges: Number of Links
    #degrees {}: Dectionary of author, their degrees and list of coauthors. {'x':[5,['a','b','c','d',e']]}
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
        self.edges = {}
        self.degrees = {}
        self.startYear = 0
        self.endYear = 0
        self.numberOfNodes = 0
        self.numberOfEdges = 0
    def makeSubCoauthorshipNetworkFromSuperCoauthorshipNetwork(self, Super, start_Year, end_Year):
        self.startYear = start_Year
        self.endYear = end_Year
        self.nodes = []
        self.edges = {}
        self.degrees = {}
        for paper in Super.papers:
            if((paper.YR<self.startYear) or (paper.YR>self.endYear)):
                continue
            for author in paper.AU:
                if(author not in self.nodes):
                    self.nodes.append(author)
                    self.numberOfNodes = self.numberOfNodes + 1
                if(author not in self.degrees):
                    list = []
                    list.append(0)
                    list.append([])
                    self.degrees[author] = list
            for author in paper.AU:
                for anotherAuthor in paper.AU:
                    if((author<anotherAuthor)): 
                        if((author,anotherAuthor) not in self.edges):
                            self.edges[(author,anotherAuthor)] = 1
                            self.numberOfEdges = self.numberOfEdges + 1
                        else:
                            self.edges[(author,anotherAuthor)] = self.edges[(author,anotherAuthor)] + 1
                        if(anotherAuthor not in self.degrees[author][1]):
                            self.degrees[author][0] = self.degrees[author][0] + 1
                            self.degrees[author][1].append(anotherAuthor)
                            self.degrees[anotherAuthor][0] = self.degrees[anotherAuthor][0] + 1
                            self.degrees[anotherAuthor][1].append(author)  
    def makeCoauthorshipNetworkFromFile(self, file):
        self.readPapersFromFile(file)
        self.makeCoauthorshipNetworkFromPapers()
    def makeCoauthorshipNetworkFromPapers(self):
        self.nodes = []
        self.edges = {}
        self.degrees = {}
        self.numberOfNodes = 0
        self.numberOfEdges = 0
        minYear = 2011
        maxYear = 1990
        for paper in self.papers:
            for author in paper.AU:
                if(author not in self.nodes):
                    self.nodes.append(author)
                    self.numberOfNodes = self.numberOfNodes + 1
                if(author not in self.degrees):
                    list = []
                    list.append(0)
                    list.append([])
                    self.degrees[author] = list
            for author in paper.AU:
                for anotherAuthor in paper.AU:
                    if((author<anotherAuthor)): 
                        if((author,anotherAuthor) not in self.edges):
                            self.edges[(author,anotherAuthor)] = 1
                            self.numberOfEdges = self.numberOfEdges + 1
                        else:
                            self.edges[(author,anotherAuthor)] = self.edges[(author,anotherAuthor)] + 1
                            
                        if(anotherAuthor not in self.degrees[author][1]):
                            self.degrees[author][0] = self.degrees[author][0] + 1
                            self.degrees[author][1].append(anotherAuthor)
                            self.degrees[anotherAuthor][0] = self.degrees[anotherAuthor][0] + 1
                            self.degrees[anotherAuthor][1].append(author)
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
            if(len(string) == 1):
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
            os.makedirs(fs)
            print('New directory made: ' + str(path2))
        fs = directoryPath + '/' + str(field) + str(run) + str(type) + str(self.startYear) + '-' + str(self.endYear) + '_' + str(size) + 'years' + 'CoauthorshipNetwork.net'
        outFile = open(fs, 'w')
        
        outFile.write('%START\n')
        outFile.write('%' + str(self.startYear) + '\n')
        outFile.write('%END\n')
        outFile.write('%' + str(self.endYear) + '\n')
        
        nodeDic = {} #dictionary for indexing the authors
        index = 0
        for node in self.nodes:
            index = index + 1
            nodeDic[node] = index
        outFile.write('*Vertices ' + str(index) + '\n')        
        sortedAuthorList = sorted(nodeDic.items(), key = itemgetter(1))
        for author in sortedAuthorList:
            outFile.write(str(author[1]) + ' "'  + str(author[0]) + '"' + '\n')
        outFile.write('*Edges\n')
        sortedEdges = sorted(self.edges.items(), key = itemgetter(1))
        for edge in sortedEdges:
            outFile.write(str(nodeDic[edge[0][0]]) + ' ' + str(nodeDic[edge[0][1]]) + ' ' + str(edge[1]) + '\n')
        outFile.close()
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
    
    #--Procedures--
    
    def __init__(self, Previous, Current):
        self.previous = Previous
        self.current = Current
        self.initializeNewNodes()
        self.initializeNewEdges()
        self.initializeCommonNodes()
        self.initializeCommonEdges()
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
        for edge in self.current.edges:
            if edge not in self.previous.edges:
                self.numberOfNewEdges = self.numberOfNewEdges + 1
                self.newEdges.append(edge)
    def initializeCommonNodes(self):
        numberOfCommonNodes = 0
        for node in self.current.nodes:
            if node in self.previous.nodes:
                self.numberOfCommonNodes = self.numberOfCommonNodes + 1
                self.commonNodes.append(node)       
    def initializeCommonEdges(self):
        self.numberOfCommonEdges = 0
        self.commonEdges = []
        for edge in self.current.edges:
            if edge in self.previous.edges:
                self.numberOfCommonEdges = self.numberOfCommonEdges + 1
                self.commonEdges.append(edge)    
    def cumulativeNumberOfAuthors(self):
        return self.previous.numberOfNodes + self.current.numberOfNodes
    def numberOfNewAuthors(self):
        return self.numberOfNewNodes
    def numberOfNewAuthorsAttachedToAtLeastANewAuthor(self):
        ans = 0
        for author in self.newNodes:
            for coauthor in self.current.degrees[author][1]:
                if coauthor in self.newNodes:
                    ans = ans + 1
                    break
        return ans
    def numberOfNewAuthorsAttachedToAtLeastAnOldAuthor(self):
        ans = 0
        for author in self.newNodes:
            for coauthor in self.current.degrees[author][1]:
                if coauthor in self.previous.nodes:
                    ans = ans + 1
                    break
        return ans
    def numberOfOldAuthorsAttachedToAtLeastANewAuthor(self):
        ans = 0
        for author in self.commonNodes:
            for coauthor in self.current.degrees[author][1]:
                if coauthor in self.newNodes:
                    ans = ans + 1
                    break
        return ans
    def numberOfOldAuthorsAttachedToAtLeastAnOldAuthor(self):
        ans = 0
        for author in self.commonNodes:
            for coauthor in self.current.degrees[author][1]:
                if coauthor in self.previous.nodes:
                    ans = ans + 1
                    break
        return ans
    def numberOfOldAuthorsAttachedToAtLeastAnAuthor(self):
        return numberOfCommonNodes
    def numberOfNewLinksAmongNewAuthors(self):
        ans = 0
        for edge in self.newEdges():
            if((edge[0] in self.newNodes) and (edge[1] in self.newNodes)):
                ans = ans + 1
        return ans
    def numberOfNewLinksBetweenNewAndOldAuthors(self):
        ans = 0
        for edge in self.newEdges():
            if(((edge[0] in self.newNodes) and (edge[1] in self.commonNodes)) or ((edge[1] in self.newNodes) and (edge[0] in self.commonNodes))):
                ans = ans + 1
        return ans
    def numberOfLinksBetweenOldAuthorsNotConnectedBefore(self):
        ans = 0
        for edge in self.newEdges:
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
        column6 = int((float(column5)/float(self.numberOfnewAuthors)) * 100.00)
        column7 = self.numberOfNewAuthorsAttachedToAtLeastAnOldAuthor()
        column8 = int((float(column7)/float(self.numberOfnewAuthors)) * 100.00)
        column9 = self.numberOfOldAuthorsAttachedToAtLeastANewAuthor()
        column10 = int((float(column9)/float(self.previous.numberOfNodes)) * 100.00)
        column11 = self.numberOfOldAuthorsAttachedToAtLeastAnOldAuthor()
        column12 = int((float(column11)/float(self.previous.numberOfNodes)) * 100.00)
        column13 = self.numberOfNewAuthorsAttachedToAtLeastAnAuthor()
        column14 = int((float(column13)/float(self.previous.numberOfNodes)) * 100.00)
        
        return (column1, column2, column3, column4, column5, column6, column7, column8, column9, column10, column11, column12, column13, column14 )
    def contentForAbbasiTable3(self):
        column1 = self.current.startYear
        column2 = self.current.endYear
        column3 = self.numberOfNewEdges + self.previous.numberOfEdges
        column4 = self.numberOfNewEdges
        column5 = self.numberOfNewLinksAmongNewAuthors()
        column6 = int(((float(column4))/(float(column4)))*100.00)
        column7 = self.numberOfNewLinksBetweenNewAndOldAuthors()
        column8 = int(((float(column6))/(float(column4)))*100.00)
        column9 = self.numberOfLinksBetweenOldAuthorsNotConnectedBefore()
        column10 = int(((float(column8))/(float(column4)))*100.00)
        column11 = self.numberOfLinksBetweenOldAuthorsConnectedBefore()
        column12 = int(((float(column10))/(float(column4)))*100.00)
        
        return (column1, column2, column3, column4, column5, column6, column7, column8, column9, column10, column11, column12)
        
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

    OUTPUT_NETWORK_DIRECTORY_FOR_PAJEK = OUTPUT_PARENT_DIRECTORY_PATH + '/nwa-' + str(FIELD) + '/' + 'runs/' + str(RUN) + '/output/networks/' + str(TYPE) + str(START_YEAR) + '-' + str(END_YEAR) + '_' + str(SIZE) +'years-network_files'
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