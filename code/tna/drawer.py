import os
import sys
import operator
import numpy
import scipy.stats
from operator import itemgetter
import pdb
import networkx as nx
import globalvar
import globalfuncs

class Net:
    def __init__(self):
        self.index = -1
        self.field = ''
        self.run = ''
        self.start_year = ''
        self.end_year = ''
        self.type= ''
        self.size = ''
        self.outpath = ''
        self.GeneralInfoFile = ''
        self.AbbasiTable2File = ''
        self.AbbasiTable3File = ''
        self.DegreeCentralityFile = ''
        self.ClosenessCentralityFile = ''
        self.BetweennessCentralityFile = ''
        self.DegreeCentralityhubFile = ''
        self.ClosenessCentralityhubFile = ''
        self.BetweennessCentralityhubFile = ''
        self.CollaborationDistributionFile = ''
        self.CollaborationDistributionhubFile = ''
        self.LargestComponentFile = ''
        self.graphpathforcomponents = ''
        self.graphpath = ''
        
        
    def setPath(self):
        self.GeneralInfoFile = self.outpath  + '/nwa-' + str(self.field) + '/' + 'runs/' + str(self.run) + '/output/statistics/' + str(self.type)  + str(self.start_year) + '-' + str(self.end_year) + '_' + str(self.size) +'years' + '/generic/allyears/whole_net/tables/' + str(self.field) + str(self.run) + '_' + str(self.type)  + str(self.start_year) + '-' + str(self.end_year) + '_' + str(self.size) + 'years_wholenet_GeneralInfo.csv'
        self.AbbasiTable2File = self.outpath  + '/nwa-' + str(self.field) + '/' + 'runs/' + str(self.run) + '/output/statistics/' + str(self.type)  + str(self.start_year) + '-' + str(self.end_year) + '_' + str(self.size) +'years' + '/generic/allyears/whole_net/tables/' + str(self.field) + str(self.run) + '_' + str(self.type)  + str(self.start_year) + '-' + str(self.end_year) + '_' + str(self.size) + 'years_wholenet_AbbasiTable2.csv'
        self.AbbasiTable3File = self.outpath  + '/nwa-' + str(self.field) + '/' + 'runs/' + str(self.run) + '/output/statistics/' + str(self.type)  + str(self.start_year) + '-' + str(self.end_year) + '_' + str(self.size) +'years' + '/generic/allyears/whole_net/tables/' + str(self.field) + str(self.run) + '_' + str(self.type)  + str(self.start_year) + '-' + str(self.end_year) + '_' + str(self.size) + 'years_wholenet_AbbasiTable3.csv'
        self.DegreeCentralityFile = self.outpath  + '/nwa-' + str(self.field) + '/' + 'runs/' + str(self.run) + '/output/statistics/' + str(self.type)  + str(self.start_year) + '-' + str(self.end_year) + '_' + str(self.size) +'years' + '/generic/allyears/whole_net/tables/' + str(self.field) + str(self.run) + '_' + str(self.type)  + str(self.start_year) + '-' + str(self.end_year) + '_' + str(self.size) + 'years_wholenet_DegreeCentrality.csv'
        self.ClosenessCentralityFile = self.outpath  + '/nwa-' + str(self.field) + '/' + 'runs/' + str(self.run) + '/output/statistics/' + str(self.type)  + str(self.start_year) + '-' + str(self.end_year) + '_' + str(self.size) +'years' + '/generic/allyears/whole_net/tables/' + str(self.field) + str(self.run) + '_' + str(self.type)  + str(self.start_year) + '-' + str(self.end_year) + '_' + str(self.size) + 'years_wholenet_ClosenessCentrality.csv'
        self.BetweennessCentralityFile = self.outpath  + '/nwa-' + str(self.field) + '/' + 'runs/' + str(self.run) + '/output/statistics/' + str(self.type)  + str(self.start_year) + '-' + str(self.end_year) + '_' + str(self.size) +'years' + '/generic/allyears/whole_net/tables/' + str(self.field) + str(self.run) + '_' + str(self.type)  + str(self.start_year) + '-' + str(self.end_year) + '_' + str(self.size) + 'years_wholenet_BetweennessCentrality.csv'
        
        self.DegreeCentralityhubFile = self.outpath  + '/nwa-' + str(self.field) + '/' + 'runs/' + str(self.run) + '/output/statistics/' + str(self.type)  + str(self.start_year) + '-' + str(self.end_year) + '_' + str(self.size) +'years' + '/generic/allyears/whole_net/tables/' + str(self.field) + str(self.run) + '_' + str(self.type)  + str(self.start_year) + '-' + str(self.end_year) + '_' + str(self.size) + 'years_wholenet_DegreeCentrality_hub.csv'
        self.ClosenessCentralityhubFile = self.outpath  + '/nwa-' + str(self.field) + '/' + 'runs/' + str(self.run) + '/output/statistics/' + str(self.type)  + str(self.start_year) + '-' + str(self.end_year) + '_' + str(self.size) +'years' + '/generic/allyears/whole_net/tables/' + str(self.field) + str(self.run) + '_' + str(self.type)  + str(self.start_year) + '-' + str(self.end_year) + '_' + str(self.size) + 'years_wholenet_ClosenessCentrality_hub.csv'
        self.BetweennessCentralityhubFile = self.outpath  + '/nwa-' + str(self.field) + '/' + 'runs/' + str(self.run) + '/output/statistics/' + str(self.type)  + str(self.start_year) + '-' + str(self.end_year) + '_' + str(self.size) +'years' + '/generic/allyears/whole_net/tables/' + str(self.field) + str(self.run) + '_' + str(self.type)  + str(self.start_year) + '-' + str(self.end_year) + '_' + str(self.size) + 'years_wholenet_BetweennessCentrality_hub.csv'
        
        self.CollaborationDistributionFile = self.outpath  + '/nwa-' + str(self.field) + '/' + 'runs/' + str(self.run) + '/output/statistics/' + str(self.type)  + str(self.start_year) + '-' + str(self.end_year) + '_' + str(self.size) +'years' + '/generic/allyears/whole_net/tables/' + str(self.field) + str(self.run) + '_' + str(self.type) + str(self.start_year) + '-' + str(self.end_year) + '_' + str(self.size) + 'years_wholenet_CollaborationDistribution.csv'
        self.CollaborationDistributionhubFile = self.outpath  + '/nwa-' + str(self.field) + '/' + 'runs/' + str(self.run) + '/output/statistics/' + str(self.type)  + str(self.start_year) + '-' + str(self.end_year) + '_' + str(self.size) +'years' + '/generic/allyears/whole_net/tables/' + str(self.field) + str(self.run) + '_' + str(self.type) + str(self.start_year) + '-' + str(self.end_year) + '_' + str(self.size) + 'years_wholenet_CollaborationDistribution_hub.csv'
        
        self.LargestComponentFile = self.outpath  + '/nwa-' + str(self.field) + '/' + 'runs/' + str(self.run) + '/output/statistics/' + str(self.type)  + str(self.start_year) + '-' + str(self.end_year) + '_' + str(self.size) +'years' + '/generic/allyears/components/tables/' +  str(self.field) + str(self.run) + '_' + str(self.type) + str(self.start_year) + '-' + str(self.end_year) + '_' + str(self.size) + 'years_Large-SecondLargeData.csv'
        
        self.Authordistributionfile = self.outpath  + '/nwa-' + str(self.field) + '/' + 'runs/' + str(self.run) + '/output/statistics/' + str(self.type)  + str(self.start_year) + '-' + str(self.end_year) + '_' + str(self.size) +'years' + '/generic/allyears/whole_net/tables/' + str(self.field) + str(self.run) + '_' + str(self.type)  + str(self.start_year) + '-' + str(self.end_year) + '_' + str(self.size) + 'years_wholenet_AuthorDistribution.csv'
        self.graphpath = self.outpath  + '/nwa-' + str(self.field) + '/' + 'runs/' + str(self.run) + '/output/statistics/' + str(self.type) + str(self.start_year) + '-' + str(self.end_year) + '_' + str(self.size) +'years' + '/generic/allyears/whole_net/images'
        self.graphpathforcomponents = self.outpath  + '/nwa-' + str(self.field) + '/' + 'runs/' + str(self.run) + '/output/statistics/' + str(self.type) + str(self.start_year) + '-' + str(self.end_year) + '_' + str(self.size) +'years' + '/generic/allyears/components/images'
        if not os.path.exists(os.path.realpath(self.graphpath)):
        	os.makedirs(os.path.realpath(self.graphpath))
class GraphDrawer:
    def __init__(self, cd):
        self.GList = []
        self.index = -1
        self.communities_directory = os.path.realpath(cd)
        
    def getData(self, file):
        #communities_directory = os.path.realpath('../..')
        f = open(file, 'r')
        G = Net()
        for line in f:
            l = len(line)
            if(line[0:6] == 'FIELD='):
                self.index = self.index + 1
                G = Net()
                G.index = self.index
                G.field = line[6:(l-1)]
            elif(line[0:4] == 'RUN='):
                G.run = line[4:(l-1)]
            elif(line[0:11] == 'START_YEAR='):
                G.start_year = line[11:(l-1)]
            elif(line[0:9] == 'END_YEAR='):
                G.end_year = line[9:(l-1)]
            elif(line[0:5] == 'TYPE='):
                G.type = line[5:(l-1)]
            elif(line[0:5] == 'SIZE='):
                G.size = line[5:(l-1)]
            elif(line[0:9] == 'NET_PATH='):
                G.outpath = os.path.realpath(self.communities_directory + '/' + line[9:(len(line)-1)])
                G.setPath()
                self.GList.append(G)
                
    def printLib(self, fs):
        f = open(fs, 'a')
        f.write('library(ggplot2)\n')
        f.write('library(scales)\n')
        f.write('\n\n\n\n')
    
    def addGeneralInfo(self, g, fs):
        fi = open(fs, 'a')
        fi.write("GI <- read.table('" + g.GeneralInfoFile + "', header = TRUE, sep =';')\n" )
        fi.write("\n\n#General Info\n")
        #number of papers
        fi.write("p<-ggplot(GI)\n")
        s = g.graphpath + '/' + str(g.field) + str(g.run) + '_' + str(g.type)  + str(g.start_year) + '-' + str(g.end_year) + '_' + str(g.size) + 'years_NumberOfPapers.pdf'
        fi.write("pdffile <-c('" +s +"')\n")
        fi.write("pdf(pdffile)\n")
        fi.write("p + xlab('Year') + ylab('Number of Papers Published') + geom_point(aes(GI$End_Year,GI$Number_Of_Papers,  shape = 'Papers')) + geom_line(aes(GI$End_Year,GI$Number_Of_Papers,  shape = 'Papers')) +  opts(legend.title=theme_blank())+ opts(title = '" + g.field +"')\n")
        fi.write("ggsave(pdffile)\n\n")
        
        #number of authors
        fi.write("p<-ggplot(GI)\n")
        s = g.graphpath + '/' + str(g.field) + str(g.run)+ '_' + str(g.type)  + str(g.start_year) + '-' + str(g.end_year) + '_' + str(g.size) + 'years_NumberOfAuthors.pdf'
        fi.write("pdffile <-c('" +s +"')\n")
        fi.write("pdf(pdffile)\n")
        fi.write("p + xlab('Year') + ylab('Number of Authors') + geom_point(aes(GI$End_Year,GI$Number_Of_Authors, shape = 'Authors')) + geom_line(aes(GI$End_Year,GI$Number_Of_Authors, shape = 'Authors')) +  opts(legend.title=theme_blank())+ opts(title = '" + g.field +"')\n")
        fi.write("ggsave(pdffile)\n\n")
        
        #number of edges
        fi.write("p<-ggplot(GI)\n")
        s = g.graphpath + '/' + str(g.field) + str(g.run) + '_' + str(g.type) + str(g.start_year) + '-' + str(g.end_year) + '_' + str(g.size) + 'years_NumberOfLinks.pdf'
        fi.write("pdffile <-c('" +s +"')\n")
        fi.write("pdf(pdffile)\n")
        fi.write("p + xlab('Year') + ylab('Number of Links') + geom_point(aes(GI$End_Year,GI$Number_Of_Unweighted_Edges, shape = 'Links')) + geom_line(aes(GI$End_Year,GI$Number_Of_Unweighted_Edges, shape = 'Links')) +  opts(legend.title=theme_blank())+ opts(title = '" + g.field +"')\n")
        fi.write("ggsave(pdffile)\n\n")
        
        #number of Links
        fi.write("p<-ggplot(GI)\n")
        s = g.graphpath + '/' + str(g.field) + str(g.run) + '_' + str(g.type) + str(g.start_year) + '-' + str(g.end_year) + '_' + str(g.size) + 'years_NumberOfEdges.pdf'
        fi.write("pdffile <-c('" +s +"')\n")
        fi.write("pdf(pdffile)\n")
        fi.write("p + xlab('Year') + ylab('Number of Edges') + geom_point(aes(GI$End_Year,GI$Number_Of_Edges, shape = 'Edges')) + geom_line(aes(GI$End_Year,GI$Number_Of_Edges, shape = 'Edges')) +  opts(legend.title=theme_blank())+ opts(title = '" + g.field +"')\n")
        fi.write("ggsave(pdffile)\n\n")
        
        #summary
        fi.write("p<-ggplot(GI)\n")
        s = g.graphpath + '/' + str(g.field) + str(g.run) + '_' + str(g.type) + str(g.start_year) + '-' + str(g.end_year) + '_' + str(g.size) + 'years_Summary.pdf'
        fi.write("pdffile <-c('" +s +"')\n")
        fi.write("pdf(pdffile)\n")
        fi.write("p + xlab('Year') + ylab('Number') + geom_point(aes(GI$End_Year,GI$Number_Of_Papers, shape = 'Papers')) + geom_line(aes(GI$End_Year,GI$Number_Of_Papers, shape = 'Papers')) +  opts(legend.title=theme_blank())+ opts(title = '" + g.field +"')")
        fi.write("+ geom_point(aes(GI$End_Year,GI$Number_Of_Authors, shape = 'Authors')) + geom_line(aes(GI$End_Year,GI$Number_Of_Authors, shape = 'Authors')) +  opts(legend.title=theme_blank())+ opts(title = '" + g.field +"')")
        fi.write("+ geom_point(aes(GI$End_Year,GI$Number_Of_Unweighted_Edges, shape = 'Links')) + geom_line(aes(GI$End_Year,GI$Number_Of_Unweighted_Edges, shape = 'Links')) +  opts(legend.title=theme_blank())+ opts(title = '" + g.field +"')")
        fi.write("+ geom_point(aes(GI$End_Year,GI$Number_Of_Edges, shape = 'Edges')) + geom_line(aes(GI$End_Year,GI$Number_Of_Edges, shape = 'Edges'))  + scale_shape_manual(values=c(2,4,16,7,15,5)) + opts(legend.title=theme_blank())+ opts(title = '" + g.field +"')\n")
        fi.write("ggsave(pdffile)\n\n")
        
        fi.write("#General Info ends\n\n\n")
        fi.close()
        
    def addAbbasi2(self, g, fs):
        fi = open(fs, 'a')
        fi.write("\n\n#Abbasi Table 2 starts\n")
        fi.write("AB1<- read.table('" + g.AbbasiTable2File + "', header = TRUE, sep =';')\n" )
        
        fi.write("\n\np<-ggplot(AB1)\n")
        s = g.graphpath + '/' + str(g.field) + str(g.run) + '_' + str(g.type) + str(g.start_year) + '-' + str(g.end_year) + '_' + str(g.size) + 'years_NewAuthorAttachmentDistribution.pdf'
        fi.write("pdffile <-c('" +s +"')\n")
        fi.write("pdf(pdffile)\n")
        fi.write("p + xlab('Year') + ylab('Percent of New Authors') + geom_point(aes(AB1$End_Year,AB1$Percent_Of_New_Authors_Connected_to_atleast_one_new_author, shape = 'With New')) + geom_point(aes(AB1$End_Year,AB1$Percent_Of_New_Authors_Connected_to_atleast_one_old_author, shape = 'With Old')) + geom_line(aes(AB1$End_Year,AB1$Percent_Of_New_Authors_Connected_to_atleast_one_new_author, shape = 'With New')) + geom_line(aes(AB1$End_Year,AB1$Percent_Of_New_Authors_Connected_to_atleast_one_old_author, shape = 'With Old'))+ scale_shape_manual(values=c(2,4,16,7,15,5)) + opts(legend.title=theme_blank()) + scale_y_continuous(limits = c(0, 100))\n")
        fi.write("ggsave(pdffile)\n\n")
        
        fi.write("p<-ggplot(AB1)\n")
        s = g.graphpath + '/' + str(g.field) + str(g.run) + '_' + str(g.type) + str(g.start_year) + '-' + str(g.end_year) + '_' + str(g.size) + 'years_OldAuthorAttachmentDistribution.pdf'
        fi.write("pdffile <-c('" +s +"')\n")
        fi.write("pdf(pdffile)\n")
        fi.write("p + xlab('Year') + ylab('Percent of old Authors') + geom_point(aes(AB1$End_Year,AB1$Percent_Of_Old_Authors_Connected_to_atleast_one_new_author, shape = 'With New')) + geom_point(aes(AB1$End_Year,AB1$Percent_Of_Old_Authors_Connected_to_atleast_one_old_author, shape = 'With Old')) + geom_point(aes(AB1$End_Year,AB1$Percent_Of_Old_Authors_Connected_to_atleast_one_any_author, shape = 'With Any')) + geom_line(aes(AB1$End_Year,AB1$Percent_Of_Old_Authors_Connected_to_atleast_one_new_author, shape = 'With New')) + geom_line(aes(AB1$End_Year,AB1$Percent_Of_Old_Authors_Connected_to_atleast_one_old_author, shape = 'With Old')) + geom_line(aes(AB1$End_Year,AB1$Percent_Of_Old_Authors_Connected_to_atleast_one_any_author, shape = 'With Any'))+ scale_shape_manual(values=c(2,4,16,7,15,5)) + opts(legend.title=theme_blank()) + scale_y_continuous(limits = c(0, 100))\n")
        fi.write("ggsave(pdffile)\n\n")
        
        
        fi.write("#Abbasi Table 2 ends\n\n\n")
        fi.close()
        
    def addAbbasi3(self, g, fs):
        fi = open(fs, 'a')
        fi.write("\n\n#Abbasi Table 3 starts\n")
        fi.write("ABT1<- read.table('" + g.AbbasiTable3File + "', header = TRUE, sep =';')\n" )
        
        fi.write("\n\np<-ggplot(ABT1)\n")
        s = g.graphpath + '/' + str(g.field) + str(g.run) + '_' + str(g.type) + str(g.start_year) + '-' + str(g.end_year) + '_' + str(g.size) + 'years_NewLinkDistribution.pdf'
        fi.write("pdffile <-c('" +s +"')\n")
        fi.write("pdf(pdffile)\n")
        fi.write("p + xlab('Year') + ylab('Percent New Links') + geom_point(aes(ABT1$End_Year,ABT1$Percent_of_New_Links_Among_New_Authors, shape = 'New-New')) + geom_point(aes(ABT1$End_Year,ABT1$Percent_Of_Links_Between_New_and_Old, shape = 'New-Old')) + geom_point(aes(ABT1$End_Year,ABT1$Percent_of_New_Links_Between_Two_Old_Authors_Not_Connected_Before, shape = 'Old-Old-1st')) + geom_point(aes(ABT1$End_Year,ABT1$Percent_of_Links_Among_Old_Authors_Connected_Before, shape = 'Old-Old-Again')) + geom_line(aes(ABT1$End_Year,ABT1$Percent_of_New_Links_Among_New_Authors, shape = 'New-New')) + geom_line(aes(ABT1$End_Year,ABT1$Percent_Of_Links_Between_New_and_Old, shape = 'New-Old')) + geom_line(aes(ABT1$End_Year,ABT1$Percent_of_New_Links_Between_Two_Old_Authors_Not_Connected_Before, shape = 'Old-Old-1st')) + geom_line(aes(ABT1$End_Year,ABT1$Percent_of_Links_Among_Old_Authors_Connected_Before, shape = 'Old-Old-Again'))+ scale_shape_manual(values=c(2,4,16,7,15,5)) + opts(legend.title=theme_blank()) + scale_y_continuous(limits = c(0, 100))\n")
        fi.write("ggsave(pdffile)\n\n")
          
        fi.write("#Abbasi Table 3 ends\n\n\n")
        fi.close()
        
    def addCentrality(self, g, fs):
        fi = open(fs, 'a')
        fi.write("\n\n#Preferrential Attachment starts\n")
        fi.write("DC1<- read.table('" + g.DegreeCentralityFile + "', header = TRUE, sep =';')\n" )
        fi.write("CC1<- read.table('" + g.ClosenessCentralityFile + "', header = TRUE, sep =';')\n" )
        fi.write("BC1<- read.table('" + g.BetweennessCentralityFile + "', header = TRUE, sep =';')\n" )
        
        fi.write("\n\np<-ggplot(DC1)\n")
        s = g.graphpath + '/' + str(g.field) + str(g.run) + '_' + str(g.type) + str(g.start_year) + '-' + str(g.end_year) + '_' + str(g.size) + 'years_CentralityVnewLinks.pdf'
        fi.write("pdffile <-c('" +s +"')\n")
        fi.write("pdf(pdffile)\n")
        fi.write("p + xlab('Year') + ylab('Spearman Correlation with Number of New Links (Any Type)') + geom_point(aes(DC1$End_Year,DC1$Correlation_Between_Prev_Degree_and_New_Degree, shape = 'Degree Centrality')) + geom_point(aes(CC1$End_Year,CC1$Correlation_Between_Prev_Closeness_and_New_Degree, shape = 'Closeness Centrality')) + geom_point(aes(BC1$End_Year,BC1$Correlation_Between_Prev_Betweenness_and_New_Degree, shape = 'Betweenness Centrality')) + geom_line(aes(DC1$End_Year,DC1$Correlation_Between_Prev_Degree_and_New_Degree, shape = 'Degree Centrality')) + geom_line(aes(CC1$End_Year,CC1$Correlation_Between_Prev_Closeness_and_New_Degree, shape = 'Closeness Centrality')) + geom_line(aes(BC1$End_Year,BC1$Correlation_Between_Prev_Betweenness_and_New_Degree, shape = 'Betweenness Centrality'))+ scale_shape_manual(values=c(2,4,16,7,15,5)) + opts(legend.title=theme_blank()) + coord_cartesian(ylim=c(-0.5, 1.0))\n")
        fi.write("ggsave(pdffile)\n\n")
        
        fi.write("p<-ggplot(DC1)\n")
        s = g.graphpath + '/' + str(g.field) + str(g.run) + '_' + str(g.type) + str(g.start_year) + '-' + str(g.end_year) + '_' + str(g.size) + 'years_CentralityVnewLinkswithNewAuthors.pdf'
        fi.write("pdffile <-c('" +s +"')\n")
        fi.write("pdf(pdffile)\n")
        fi.write("p + xlab('Year') + ylab('Spearman correlation (Collaborations with New Authors)') + geom_point(aes(DC1$End_Year,DC1$Correlation_Between_Prev_Degree_and_New_Authors_Degree, shape = 'Degree Centrality')) + geom_point(aes(CC1$End_Year,CC1$Correlation_Between_Prev_Closeness_and_New_Authors_Degree, shape = 'Closeness Centrality')) + geom_point(aes(BC1$End_Year,BC1$Correlation_Between_Prev_Betweenness_and_New_Authors_Degree, shape = 'Betweenness Centrality')) + geom_line(aes(DC1$End_Year,DC1$Correlation_Between_Prev_Degree_and_New_Authors_Degree, shape = 'Degree Centrality')) + geom_line(aes(CC1$End_Year,CC1$Correlation_Between_Prev_Closeness_and_New_Authors_Degree, shape = 'Closeness Centrality')) + geom_line(aes(BC1$End_Year,BC1$Correlation_Between_Prev_Betweenness_and_New_Authors_Degree, shape = 'Betweenness Centrality'))+ scale_shape_manual(values=c(2,4,16,7,15,5)) + opts(legend.title=theme_blank()) + coord_cartesian(ylim=c(-0.5, 1.0))\n")
        fi.write("ggsave(pdffile)\n\n")
        
        fi.write("p<-ggplot(DC1)\n")
        s = g.graphpath + '/' + str(g.field) + str(g.run) + '_' + str(g.type) + str(g.start_year) + '-' + str(g.end_year) + '_' + str(g.size) + 'years_CentralityVnewLinkswithOldAuthors.pdf'
        fi.write("pdffile <-c('" +s +"')\n")
        fi.write("pdf(pdffile)\n")
        fi.write("p + xlab('Year') + ylab('Spearman correlation (New Collaborations between Existing Authors)') + geom_point(aes(DC1$End_Year,DC1$Correlation_Between_Prev_Degree_and_New_Old_Degree, shape = 'Degree Centrality')) + geom_point(aes(CC1$End_Year,CC1$Correlation_Between_Prev_Closeness_and_New_Old_Degree, shape = 'Closeness Centrality')) + geom_point(aes(BC1$End_Year,BC1$Correlation_Between_Prev_Betweenness_and_New_Old_Degree, shape = 'Betweenness Centrality')) + geom_line(aes(DC1$End_Year,DC1$Correlation_Between_Prev_Degree_and_New_Old_Degree, shape = 'Degree Centrality')) + geom_line(aes(CC1$End_Year,CC1$Correlation_Between_Prev_Closeness_and_New_Old_Degree, shape = 'Closeness Centrality')) + geom_line(aes(BC1$End_Year,BC1$Correlation_Between_Prev_Betweenness_and_New_Old_Degree, shape = 'Betweenness Centrality'))+ scale_shape_manual(values=c(2,4,16,7,15,5)) + opts(legend.title=theme_blank()) + coord_cartesian(ylim=c(-0.5, 1.0))\n")
        fi.write("ggsave(pdffile)\n\n")
        
        fi.write("#Preferrential Attachment ends\n\n\n")
        fi.close()
        
    def addCentralityhub(self, g, fs):
        fi = open(fs, 'a')
        fi.write("\n\n#Preferrential Attachment starts\n")
        fi.write("DC1<- read.table('" + g.DegreeCentralityhubFile + "', header = TRUE, sep =';')\n" )
        fi.write("CC1<- read.table('" + g.ClosenessCentralityhubFile + "', header = TRUE, sep =';')\n" )
        fi.write("BC1<- read.table('" + g.BetweennessCentralityhubFile + "', header = TRUE, sep =';')\n" )
        
        fi.write("\n\np<-ggplot(DC1)\n")
        s = g.graphpath + '/' + str(g.field) + str(g.run) + '_' + str(g.type) + str(g.start_year) + '-' + str(g.end_year) + '_' + str(g.size) + 'years_CentralityVnewLinks_hub.pdf'
        fi.write("pdffile <-c('" +s +"')\n")
        fi.write("pdf(pdffile)\n")
        fi.write("p + xlab('Year') + ylab('Spearman Correlation with Number of New Links (Any Type)') + geom_point(aes(DC1$End_Year,DC1$Correlation_Between_Prev_Degree_and_New_Degree, shape = 'Degree Centrality')) + geom_point(aes(CC1$End_Year,CC1$Correlation_Between_Prev_Closeness_and_New_Degree, shape = 'Closeness Centrality')) + geom_point(aes(BC1$End_Year,BC1$Correlation_Between_Prev_Betweenness_and_New_Degree, shape = 'Betweenness Centrality')) + geom_line(aes(DC1$End_Year,DC1$Correlation_Between_Prev_Degree_and_New_Degree, shape = 'Degree Centrality')) + geom_line(aes(CC1$End_Year,CC1$Correlation_Between_Prev_Closeness_and_New_Degree, shape = 'Closeness Centrality')) + geom_line(aes(BC1$End_Year,BC1$Correlation_Between_Prev_Betweenness_and_New_Degree, shape = 'Betweenness Centrality'))+ scale_shape_manual(values=c(2,4,16,7,15,5)) + opts(legend.title=theme_blank()) + coord_cartesian(ylim=c(-0.5, 1.0))\n")
        fi.write("ggsave(pdffile)\n\n")
        
        fi.write("p<-ggplot(DC1)\n")
        s = g.graphpath + '/' + str(g.field) + str(g.run) + '_' + str(g.type) + str(g.start_year) + '-' + str(g.end_year) + '_' + str(g.size) + 'years_CentralityVnewLinkswithNewAuthors_hub.pdf'
        fi.write("pdffile <-c('" +s +"')\n")
        fi.write("pdf(pdffile)\n")
        fi.write("p + xlab('Year') + ylab('Spearman correlation (Collaborations with New Authors)') + geom_point(aes(DC1$End_Year,DC1$Correlation_Between_Prev_Degree_and_New_Authors_Degree, shape = 'Degree Centrality')) + geom_point(aes(CC1$End_Year,CC1$Correlation_Between_Prev_Closeness_and_New_Authors_Degree, shape = 'Closeness Centrality')) + geom_point(aes(BC1$End_Year,BC1$Correlation_Between_Prev_Betweenness_and_New_Authors_Degree, shape = 'Betweenness Centrality')) + geom_line(aes(DC1$End_Year,DC1$Correlation_Between_Prev_Degree_and_New_Authors_Degree, shape = 'Degree Centrality')) + geom_line(aes(CC1$End_Year,CC1$Correlation_Between_Prev_Closeness_and_New_Authors_Degree, shape = 'Closeness Centrality')) + geom_line(aes(BC1$End_Year,BC1$Correlation_Between_Prev_Betweenness_and_New_Authors_Degree, shape = 'Betweenness Centrality'))+ scale_shape_manual(values=c(2,4,16,7,15,5)) + opts(legend.title=theme_blank()) + coord_cartesian(ylim=c(-0.5, 1.0))\n")
        fi.write("ggsave(pdffile)\n\n")
        
        fi.write("p<-ggplot(DC1)\n")
        s = g.graphpath + '/' + str(g.field) + str(g.run) + '_' + str(g.type) + str(g.start_year) + '-' + str(g.end_year) + '_' + str(g.size) + 'years_CentralityVnewLinkswithOldAuthors_hub.pdf'
        fi.write("pdffile <-c('" +s +"')\n")
        fi.write("pdf(pdffile)\n")
        fi.write("p + xlab('Year') + ylab('Spearman correlation (New Collaborations between Existing Authors)') + geom_point(aes(DC1$End_Year,DC1$Correlation_Between_Prev_Degree_and_New_Old_Degree, shape = 'Degree Centrality')) + geom_point(aes(CC1$End_Year,CC1$Correlation_Between_Prev_Closeness_and_New_Old_Degree, shape = 'Closeness Centrality')) + geom_point(aes(BC1$End_Year,BC1$Correlation_Between_Prev_Betweenness_and_New_Old_Degree, shape = 'Betweenness Centrality')) + geom_line(aes(DC1$End_Year,DC1$Correlation_Between_Prev_Degree_and_New_Old_Degree, shape = 'Degree Centrality')) + geom_line(aes(CC1$End_Year,CC1$Correlation_Between_Prev_Closeness_and_New_Old_Degree, shape = 'Closeness Centrality')) + geom_line(aes(BC1$End_Year,BC1$Correlation_Between_Prev_Betweenness_and_New_Old_Degree, shape = 'Betweenness Centrality'))+ scale_shape_manual(values=c(2,4,16,7,15,5)) + opts(legend.title=theme_blank()) + coord_cartesian(ylim=c(-0.5, 1.0))\n")
        fi.write("ggsave(pdffile)\n\n")
        
        fi.write("#Preferrential Attachment ends\n\n\n")
        fi.close()

    def addpValuesCentrality(self, g, fs):
        fi = open(fs, 'a')
        fi.write("\n\n#p-Values for Preferrential Attachment starts\n")
        fi.write("DC1<- read.table('" + g.DegreeCentralityFile + "', header = TRUE, sep =';')\n" )
        fi.write("CC1<- read.table('" + g.ClosenessCentralityFile + "', header = TRUE, sep =';')\n" )
        fi.write("BC1<- read.table('" + g.BetweennessCentralityFile + "', header = TRUE, sep =';')\n" )
        
        fi.write("\n\np<-ggplot(DC1)\n")
        s = g.graphpath + '/' + str(g.field) + str(g.run) + '_' + str(g.type) + str(g.start_year) + '-' + str(g.end_year) + '_' + str(g.size) + 'years_pCentralityVnewLinks.pdf'
        fi.write("pdffile <-c('" +s +"')\n")
        fi.write("pdf(pdffile)\n")
        fi.write("p + xlab('Year') + ylab('p-Values of the Spearman Correlation with Number of New Links (Any Type)') + geom_point(aes(DC1$End_Year,DC1$pCDND, shape = 'Degree Centrality')) + geom_point(aes(CC1$End_Year,CC1$pCDND, shape = 'Closeness Centrality')) + geom_point(aes(BC1$End_Year,BC1$pCDND, shape = 'Betweenness Centrality')) + geom_line(aes(DC1$End_Year,DC1$pCDND, shape = 'Degree Centrality')) + geom_line(aes(CC1$End_Year,CC1$pCDND, shape = 'Closeness Centrality')) + geom_line(aes(BC1$End_Year,BC1$pCDND, shape = 'Betweenness Centrality'))+ scale_shape_manual(values=c(2,4,16,7,15,5)) + opts(legend.title=theme_blank())\n")
        fi.write("ggsave(pdffile)\n\n")
        
        fi.write("p<-ggplot(DC1)\n")
        s = g.graphpath + '/' + str(g.field) + str(g.run) + '_' + str(g.type) + str(g.start_year) + '-' + str(g.end_year) + '_' + str(g.size) + 'years_pCentralityVnewLinkswithNewAuthors.pdf'
        fi.write("pdffile <-c('" +s +"')\n")
        fi.write("pdf(pdffile)\n")
        fi.write("p + xlab('Year') + ylab('p-Values of the Spearman correlation (Collaborations with New Authors)') + geom_point(aes(DC1$End_Year,DC1$pCDNAD, shape = 'Degree Centrality')) + geom_point(aes(CC1$End_Year,CC1$pCDNAD, shape = 'Closeness Centrality')) + geom_point(aes(BC1$End_Year,BC1$pCDNAD, shape = 'Betweenness Centrality')) + geom_line(aes(DC1$End_Year,DC1$pCDNAD, shape = 'Degree Centrality')) + geom_line(aes(CC1$End_Year,CC1$pCDNAD, shape = 'Closeness Centrality')) + geom_line(aes(BC1$End_Year,BC1$pCDNAD, shape = 'Betweenness Centrality'))+ scale_shape_manual(values=c(2,4,16,7,15,5)) + opts(legend.title=theme_blank())\n")
        fi.write("ggsave(pdffile)\n\n")
        
        fi.write("p<-ggplot(DC1)\n")
        s = g.graphpath + '/' + str(g.field) + str(g.run) + '_' + str(g.type) + str(g.start_year) + '-' + str(g.end_year) + '_' + str(g.size) + 'years_pCentralityVnewLinkswithOldAuthors.pdf'
        fi.write("pdffile <-c('" +s +"')\n")
        fi.write("pdf(pdffile)\n")
        fi.write("p + xlab('Year') + ylab('p-Values of the Spearman correlation (New Collaborations between Existing Authors)') + geom_point(aes(DC1$End_Year,DC1$pCDNOD, shape = 'Degree Centrality')) + geom_point(aes(CC1$End_Year,CC1$pCDNOD, shape = 'Closeness Centrality')) + geom_point(aes(BC1$End_Year,BC1$pCDNOD, shape = 'Betweenness Centrality')) + geom_line(aes(DC1$End_Year,DC1$pCDNOD, shape = 'Degree Centrality')) + geom_line(aes(CC1$End_Year,CC1$pCDNOD, shape = 'Closeness Centrality')) + geom_line(aes(BC1$End_Year,BC1$pCDNOD, shape = 'Betweenness Centrality'))+ scale_shape_manual(values=c(2,4,16,7,15,5)) + opts(legend.title=theme_blank())\n")
        fi.write("ggsave(pdffile)\n\n")
        
        fi.write("#p-Values of Preferrential Attachment ends\n\n\n")
        fi.close()
        
    

    def addpValuesCentralityhub(self, g, fs):

        fi = open(fs, 'a')
        fi.write("\n\n#p-Values for Preferrential Attachment starts\n")
        fi.write("DC1<- read.table('" + g.DegreeCentralityhubFile + "', header = TRUE, sep =';')\n" )
        fi.write("CC1<- read.table('" + g.ClosenessCentralityhubFile + "', header = TRUE, sep =';')\n" )
        fi.write("BC1<- read.table('" + g.BetweennessCentralityhubFile + "', header = TRUE, sep =';')\n" )
        
        fi.write("\n\np<-ggplot(DC1)\n")
        s = g.graphpath + '/' + str(g.field) + str(g.run) + '_' + str(g.type) + str(g.start_year) + '-' + str(g.end_year) + '_' + str(g.size) + 'years_pCentralityVnewLinks_hub.pdf'
        fi.write("pdffile <-c('" +s +"')\n")
        fi.write("pdf(pdffile)\n")
        fi.write("p + xlab('Year') + ylab('p-Values of the Spearman Correlation with Number of New Links (Any Type)') + geom_point(aes(DC1$End_Year,DC1$pCDND, shape = 'Degree Centrality')) + geom_point(aes(CC1$End_Year,CC1$pCDND, shape = 'Closeness Centrality')) + geom_point(aes(BC1$End_Year,BC1$pCDND, shape = 'Betweenness Centrality')) + geom_line(aes(DC1$End_Year,DC1$pCDND, shape = 'Degree Centrality')) + geom_line(aes(CC1$End_Year,CC1$pCDND, shape = 'Closeness Centrality')) + geom_line(aes(BC1$End_Year,BC1$pCDND, shape = 'Betweenness Centrality'))+ scale_shape_manual(values=c(2,4,16,7,15,5)) + opts(legend.title=theme_blank())\n")
        fi.write("ggsave(pdffile)\n\n")
        
        fi.write("p<-ggplot(DC1)\n")
        s = g.graphpath + '/' + str(g.field) + str(g.run) + '_' + str(g.type) + str(g.start_year) + '-' + str(g.end_year) + '_' + str(g.size) + 'years_pCentralityVnewLinkswithNewAuthors_hub.pdf'
        fi.write("pdffile <-c('" +s +"')\n")
        fi.write("pdf(pdffile)\n")
        fi.write("p + xlab('Year') + ylab('p-Values of the Spearman correlation (Collaborations with New Authors)') + geom_point(aes(DC1$End_Year,DC1$pCDNAD, shape = 'Degree Centrality')) + geom_point(aes(CC1$End_Year,CC1$pCDNAD, shape = 'Closeness Centrality')) + geom_point(aes(BC1$End_Year,BC1$pCDNAD, shape = 'Betweenness Centrality')) + geom_line(aes(DC1$End_Year,DC1$pCDNAD, shape = 'Degree Centrality')) + geom_line(aes(CC1$End_Year,CC1$pCDNAD, shape = 'Closeness Centrality')) + geom_line(aes(BC1$End_Year,BC1$pCDNAD, shape = 'Betweenness Centrality'))+ scale_shape_manual(values=c(2,4,16,7,15,5)) + opts(legend.title=theme_blank())\n")
        fi.write("ggsave(pdffile)\n\n")
        
        fi.write("p<-ggplot(DC1)\n")
        s = g.graphpath + '/' + str(g.field) + str(g.run) + '_' + str(g.type) + str(g.start_year) + '-' + str(g.end_year) + '_' + str(g.size) + 'years_pCentralityVnewLinkswithOldAuthors_hub.pdf'
        fi.write("pdffile <-c('" +s +"')\n")
        fi.write("pdf(pdffile)\n")
        fi.write("p + xlab('Year') + ylab('p-Values of the Spearman correlation (New Collaborations between Existing Authors)')+ geom_point(aes(DC1$End_Year,DC1$pCDNOD, shape = 'Degree Centrality')) + geom_point(aes(CC1$End_Year,CC1$pCDNOD, shape = 'Closeness Centrality')) + geom_point(aes(BC1$End_Year,BC1$pCDNOD, shape = 'Betweenness Centrality')) + geom_line(aes(DC1$End_Year,DC1$pCDNOD, shape = 'Degree Centrality')) + geom_line(aes(CC1$End_Year,CC1$pCDNOD, shape = 'Closeness Centrality')) + geom_line(aes(BC1$End_Year,BC1$pCDNOD, shape = 'Betweenness Centrality'))+ scale_shape_manual(values=c(2,4,16,7,15,5)) + opts(legend.title=theme_blank())\n")
        fi.write("ggsave(pdffile)\n\n")
        
        fi.write("#p-Values of Preferrential Attachment ends\n\n\n")
        fi.close()

        
    def addDegreeDistribution(self, g, fs):
        fi = open(fs, 'a')
        fi.write("\n\n#Degree Distribution starts\n")
        fi.write("M<- read.table('" + g.CollaborationDistributionFile + "', header = TRUE, sep =';')\n" )
        
        fi.write("p<-ggplot(M)\n")
        s = g.graphpath + '/' + str(g.field) + str(g.run) + '_' + str(g.type) + str(g.start_year) + '-' + str(g.end_year) + '_' + str(g.size) + 'years_CollaborationDistribution.pdf'
        fi.write("pdffile <-c('" +s +"')\n")
        fi.write("pdf(pdffile)\n")
        fi.write("N<-c()\n")
        fi.write("for (i in 0:10) { N[i+1]<-10^i}\n")
        fi.write("p + xlab('Number of Authors') + ylab('Number of Collaborators (per author)') + geom_point(aes(M$Collaborators, M$Frequency)) + geom_line(aes(M$Collaborators, M$Frequency)) + coord_trans('log10','log10') + scale_x_continuous(breaks=N) + scale_y_continuous(breaks=N)\n")
        fi.write("ggsave(pdffile)\n\n")

        fi.write("#Degree Distribution ends\n\n\n")
        fi.close()
        
    def addDegreeDistributionhub(self, g, fs):
        fi = open(fs, 'a')
        fi.write("\n\n#Degree Distribution starts\n")
        fi.write("M<- read.table('" + g.CollaborationDistributionhubFile + "', header = TRUE, sep =';')\n" )
        
        fi.write("p<-ggplot(M)\n")
        s = g.graphpath + '/' + str(g.field) + str(g.run) + '_' + str(g.type) + str(g.start_year) + '-' + str(g.end_year) + '_' + str(g.size) + 'years_CollaborationDistribution_hub.pdf'
        fi.write("pdffile <-c('" +s +"')\n")
        fi.write("pdf(pdffile)\n")
        fi.write("N<-c()\n")
        fi.write("for (i in 0:10) { N[i+1]<-10^i}\n")
        fi.write("p + xlab('Number of Authors') + ylab('Number of Collaborators (per author)') + geom_point(aes(M$Collaborators, M$Frequency)) + geom_line(aes(M$Collaborators, M$Frequency)) + coord_trans('log10','log10') + scale_x_continuous(breaks=N) + scale_y_continuous(breaks=N)\n")
        fi.write("ggsave(pdffile)\n\n")

        fi.write("#Degree Distribution ends\n\n\n")
        fi.close()
    def addAuthorDistribution(self, g, fs):
        fi = open(fs, 'a')
        fi.write("\n\n#Author Distribution starts\n")
        fi.write("M<- read.table('" + g.Authordistributionfile + "', header = TRUE, sep =';')\n" )
        
        fi.write("p<-ggplot(M)\n")
        s = g.graphpath + '/' + str(g.field) + str(g.run) + '_' + str(g.type) + str(g.start_year) + '-' + str(g.end_year) + '_' + str(g.size) + 'years_AuthorDistribution.pdf'
        fi.write("pdffile <-c('" +s +"')\n")
        fi.write("pdf(pdffile)\n")
        fi.write("p + xlab('No. of Authors') + ylab('Number of Papers') + geom_point(aes(M$No_of_Authors, M$Frequency_of_Papers)) + geom_line(aes(M$No_of_Authors, M$Frequency_of_Papers)) \n")
        fi.write("ggsave(pdffile)\n\n")

        fi.write("#Author Distribution ends\n\n\n")
        fi.close()
        

        
    def densification(self, g, fs):
        fi = open(fs, 'a')
        fi.write("\n\n#Densification starts\n")
        fi.write("M<- read.table('" + g.GeneralInfoFile + "', header = TRUE, sep =';')\n" )
        
        fi.write("p<-ggplot(M)\n")
        s = g.graphpath + '/' + str(g.field) + str(g.run) + '_' + str(g.type) + str(g.start_year) + '-' + str(g.end_year) + '_' + str(g.size) + 'years_Densification.pdf'
        fi.write("pdffile <-c('" +s +"')\n")
        fi.write("pdf(pdffile)\n")
        fi.write('res=lm(log10(M$Number_Of_Unweighted_Edges)~log10(M$Number_Of_Authors))\n')
        fi.write("p + xlab('Log10(Number of Authors)') + ylab('Log10(Number of Connections)') + geom_point(aes(M$Number_Of_Authors, M$Number_Of_Unweighted_Edges)) + geom_line(aes(M$Number_Of_Authors, M$Number_Of_Unweighted_Edges)) + coord_trans('log10','log10') + opts(title=res)\n")
        fi.write("ggsave(pdffile)\n\n")

        fi.write("#Densification ends\n\n\n")
        fi.close()    
        
    def makeIndividualGraphs(self, fs):
        for g in self.GList:
            self.addGeneralInfo(g,fs)
            self.addAbbasi2(g,fs)
            self.addAbbasi3(g,fs)
            self.addCentrality(g,fs)
            self.addpValuesCentrality(g, fs)
            self.addDegreeDistribution(g,fs)
            self.addAuthorDistribution(g,fs)
            self.densification(g,fs)
    
    def makeIndividualhubGraphs(self, fs):
        for g in self.GList:
            self.addCentralityhub(g,fs)
            self.addDegreeDistributionhub(g,fs)
            self.addpValuesCentralityhub(g, fs)
            
    
    def addLargestComponentGraph(self, g, fs):
    	fi = open(fs, 'a')
        fi.write("\n\n#Largest Component starts\n")
        fi.write("M<- read.table('" + g.LargestComponentFile + "', header = TRUE, sep =';')\n" )
        
        fi.write("p<-ggplot(M)\n")
        s = g.graphpathforcomponents + '/' + str(g.field) + str(g.run) + '_' + str(g.type) + str(g.start_year) + '-' + str(g.end_year) + '_' + str(g.size) + 'years_LargestComponent.pdf'
        fi.write("pdffile <-c('" +s +"')\n")
        fi.write("pdf(pdffile)\n")
        fi.write("p + xlab('Year') + ylab('% of authors newly joining largest component') + geom_point(aes(M$End_year, M$Ever_Second_Percent, shape = 'Second Ever')) + geom_line(aes(M$End_year, M$Ever_Second_Percent, shape = 'Second Ever')) + geom_point(aes(M$End_year, M$Just_Previous_Percent, shape = 'Previous Second')) + geom_line(aes(M$End_year, M$Just_Previous_Percent, shape = 'Previous Second'))+ geom_point(aes(M$End_year, M$Percent_from_others, shape = 'From Other Components')) + geom_line(aes(M$End_year, M$Percent_from_others, shape = 'From Other Components')) + geom_point(aes(M$End_year, M$Percent_Previous_Largest,  shape = 'From Previous Largest')) + geom_line(aes(M$End_year, M$Percent_Previous_Largest,  shape = 'From Previous Largest')) + geom_point(aes(M$End_year, M$Percent_New,   shape = 'From New')) + geom_line(aes(M$End_year, M$Percent_New,  shape = 'From New'))+ scale_shape_manual(values=c(2,4,16,7,15,5)) \n")
        fi.write("ggsave(pdffile)\n\n")

        fi.write("#Largest Component ends\n\n\n")
        
        fi.write("\n\n#Largest Component 2 starts\n")
        fi.write("p<-ggplot(M)\n")
        s = g.graphpathforcomponents + '/' + str(g.field) + str(g.run) + '_' + str(g.type) + str(g.start_year) + '-' + str(g.end_year) + '_' + str(g.size) + 'years_LargestComponent2.pdf'
        fi.write("pdffile <-c('" +s +"')\n")
        fi.write("pdf(pdffile)\n")
        fi.write("p + xlab('Year') + ylab('% of authors newly joining largest component') + geom_point(aes(M$End_year, (M$Number_from_Just_Previous_Second/(M$Number_from_Just_Previous_Second + M$Number_from_Others + M$New))*100.00,  shape = '2nd component'))+ geom_line(aes(M$End_year, (M$Number_from_Just_Previous_Second/(M$Number_from_Just_Previous_Second + M$Number_from_Others + M$New))*100.00))+ geom_point(aes(M$End_year, (M$Number_from_Others/(M$Number_from_Just_Previous_Second + M$Number_from_Others + M$New))*100.00,  shape = 'other component')) + geom_line(aes(M$End_year, (M$Number_from_Others/(M$Number_from_Just_Previous_Second + M$Number_from_Others + M$New))*100.00)) + geom_point(aes(M$End_year, (M$New/(M$Number_from_Just_Previous_Second + M$Number_from_Others + M$New))*100.00,  shape = 'new author')) + geom_line(aes(M$End_year, (M$New/(M$Number_from_Just_Previous_Second + M$Number_from_Others + M$New))*100.00)) + scale_shape_manual(nam = 'Source', values=c(2,4,16,7,15,5)) + coord_cartesian(ylim=c(0, 100)) + \n")
        fi.write("ggsave(pdffile)\n\n")

        fi.write("#Largest Component 2 ends\n\n\n")
        
        
        fi.close() 
    
    def makeIndividualComponentGraphs(self, fs):
    	for g in self.GList:
    		self.addLargestComponentGraph(g,fs)
            
    def makeComparisonGraphs(self, fs):
        print 'No comparison graph'
        
    def makeR(self):
        fs = os.path.realpath(self.communities_directory +'/code/network-stats/makegraphs.r')
        f = open(fs,'w')
        f.close()
        self.printLib(fs)
        self.makeIndividualGraphs(fs)
        self.makeComparisonGraphs(fs)
    
    def makeRhub(self):
        fs = os.path.realpath(self.communities_directory + '/code/hub-analysis/co-author/makegraphs.r')
        f = open(fs,'w')
        f.close()
        self.printLib(fs)
        self.makeIndividualhubGraphs(fs)
        
    def makeRcomponent(self):
        fs = os.path.realpath(self.communities_directory + '/code/component-analysis/co-author/makegraphs.r')
        f = open(fs,'w')
        f.close()
        self.printLib(fs)
        self.makeIndividualComponentGraphs(fs)
        
if __name__ == "__main__":
	communities_directory = os.path.realpath(os.getcwd() + '/../..')
	G = GraphDrawer(communities_directory)
	G.getData('/Users/macbookadministrator/Academic/Research/Network/communities/parameters/parameters-global.txt')
	G.makeRhub()
    