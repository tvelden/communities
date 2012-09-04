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
        self.CollaborationDistributionFile = ''
        self.graphpath = ''
    def setPath(self):
        self.GeneralInfoFile = self.outpath  + '/nwa-' + str(self.field) + '/' + 'runs/' + str(self.run) + '/output/statistics/' + str(self.type)  + str(self.start_year) + '-' + str(self.end_year) + '_' + str(self.size) +'years' + '/generic/allyears/whole_net/tables/' + str(self.field) + str(self.run) + '_' + str(self.type)  + str(self.start_year) + '-' + str(self.end_year) + '_' + str(self.size) + 'years_wholenet_GeneralInfo.csv'
        self.AbbasiTable2File = self.outpath  + '/nwa-' + str(self.field) + '/' + 'runs/' + str(self.run) + '/output/statistics/' + str(self.type)  + str(self.start_year) + '-' + str(self.end_year) + '_' + str(self.size) +'years' + '/generic/allyears/whole_net/tables/' + str(self.field) + str(self.run) + '_' + str(self.type)  + str(self.start_year) + '-' + str(self.end_year) + '_' + str(self.size) + 'years_wholenet_AbbasiTable2.csv'
        self.AbbasiTable3File = self.outpath  + '/nwa-' + str(self.field) + '/' + 'runs/' + str(self.run) + '/output/statistics/' + str(self.type)  + str(self.start_year) + '-' + str(self.end_year) + '_' + str(self.size) +'years' + '/generic/allyears/whole_net/tables/' + str(self.field) + str(self.run) + '_' + str(self.type)  + str(self.start_year) + '-' + str(self.end_year) + '_' + str(self.size) + 'years_wholenet_AbbasiTable3.csv'
        self.DegreeCentralityFile = self.outpath  + '/nwa-' + str(self.field) + '/' + 'runs/' + str(self.run) + '/output/statistics/' + str(self.type)  + str(self.start_year) + '-' + str(self.end_year) + '_' + str(self.size) +'years' + '/generic/allyears/whole_net/tables/' + str(self.field) + str(self.run) + '_' + str(self.type)  + str(self.start_year) + '-' + str(self.end_year) + '_' + str(self.size) + 'years_wholenet_DegreeCentrality.csv'
        self.ClosenessCentralityFile = self.outpath  + '/nwa-' + str(self.field) + '/' + 'runs/' + str(self.run) + '/output/statistics/' + str(self.type)  + str(self.start_year) + '-' + str(self.end_year) + '_' + str(self.size) +'years' + '/generic/allyears/whole_net/tables/' + str(self.field) + str(self.run) + '_' + str(self.type)  + str(self.start_year) + '-' + str(self.end_year) + '_' + str(self.size) + 'years_wholenet_ClosenessCentrality.csv'
        self.BetweennessCentralityFile = self.outpath  + '/nwa-' + str(self.field) + '/' + 'runs/' + str(self.run) + '/output/statistics/' + str(self.type)  + str(self.start_year) + '-' + str(self.end_year) + '_' + str(self.size) +'years' + '/generic/allyears/whole_net/tables/' + str(self.field) + str(self.run) + '_' + str(self.type)  + str(self.start_year) + '-' + str(self.end_year) + '_' + str(self.size) + 'years_wholenet_BetweennessCentrality.csv'
        self.CollaborationDistributionFile = self.outpath  + '/nwa-' + str(self.field) + '/' + 'runs/' + str(self.run) + '/output/statistics/' + str(self.type)  + str(self.start_year) + '-' + str(self.end_year) + '_' + str(self.size) +'years' + '/generic/allyears/whole_net/tables/' + str(self.field) + str(self.run) + '_' + str(self.type) + str(self.start_year) + '-' + str(self.end_year) + '_' + str(self.size) + 'years_wholenet_CollaborationDistribution.csv'
        self.Authordistributionfile = self.outpath  + '/nwa-' + str(self.field) + '/' + 'runs/' + str(self.run) + '/output/statistics/' + str(self.type)  + str(self.start_year) + '-' + str(self.end_year) + '_' + str(self.size) +'years' + '/generic/allyears/whole_net/tables/' + str(self.field) + str(self.run) + '_' + str(self.type)  + str(self.start_year) + '-' + str(self.end_year) + '_' + str(self.size) + 'years_wholenet_AuthorDistribution.csv'
        self.graphpath = self.outpath  + '/nwa-' + str(self.field) + '/' + 'runs/' + str(self.run) + '/output/statistics/' + str(self.type) + str(self.start_year) + '-' + str(self.end_year) + '_' + str(self.size) +'years' + '/generic/allyears/whole_net/images'
        if not os.path.exists(os.path.realpath(self.graphpath)):
        	os.makedirs(os.path.realpath(self.graphpath))
class GraphDrawer:
    def __init__(self):
        self.GList = []
        self.index = -1
    def getData(self, file):
        communities_directory = os.path.realpath('../..')
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
                G.outpath = os.path.realpath(communities_directory + '/' + line[9:(len(line)-1)])
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
        fi.write("p + xlab('Year') + ylab('Number of Papers Published') + geom_point(aes(GI$End_Year,GI$Number_Of_Papers, color = 'Papers')) + geom_line(aes(GI$End_Year,GI$Number_Of_Papers, color = 'Papers')) +  opts(legend.title=theme_blank())+ opts(title = '" + g.field +"')\n")
        fi.write("ggsave(pdffile)\n\n")
        
        #number of authors
        fi.write("p<-ggplot(GI)\n")
        s = g.graphpath + '/' + str(g.field) + str(g.run)+ '_' + str(g.type)  + str(g.start_year) + '-' + str(g.end_year) + '_' + str(g.size) + 'years_NumberOfAuthors.pdf'
        fi.write("pdffile <-c('" +s +"')\n")
        fi.write("pdf(pdffile)\n")
        fi.write("p + xlab('Year') + ylab('Number of Authors') + geom_point(aes(GI$End_Year,GI$Number_Of_Authors, color = 'Authors')) + geom_line(aes(GI$End_Year,GI$Number_Of_Authors, color = 'Authors')) +  opts(legend.title=theme_blank())+ opts(title = '" + g.field +"')\n")
        fi.write("ggsave(pdffile)\n\n")
        
        #number of edges
        fi.write("p<-ggplot(GI)\n")
        s = g.graphpath + '/' + str(g.field) + str(g.run) + '_' + str(g.type) + str(g.start_year) + '-' + str(g.end_year) + '_' + str(g.size) + 'years_NumberOfLinks.pdf'
        fi.write("pdffile <-c('" +s +"')\n")
        fi.write("pdf(pdffile)\n")
        fi.write("p + xlab('Year') + ylab('Number of Links') + geom_point(aes(GI$End_Year,GI$Number_Of_Unweighted_Edges, color = 'Links')) + geom_line(aes(GI$End_Year,GI$Number_Of_Unweighted_Edges, color = 'Links')) +  opts(legend.title=theme_blank())+ opts(title = '" + g.field +"')\n")
        fi.write("ggsave(pdffile)\n\n")
        
        #number of Links
        fi.write("p<-ggplot(GI)\n")
        s = g.graphpath + '/' + str(g.field) + str(g.run) + '_' + str(g.type) + str(g.start_year) + '-' + str(g.end_year) + '_' + str(g.size) + 'years_NumberOfEdges.pdf'
        fi.write("pdffile <-c('" +s +"')\n")
        fi.write("pdf(pdffile)\n")
        fi.write("p + xlab('Year') + ylab('Number of Edges') + geom_point(aes(GI$End_Year,GI$Number_Of_Edges, color = 'Edges')) + geom_line(aes(GI$End_Year,GI$Number_Of_Edges, color = 'Edges')) +  opts(legend.title=theme_blank())+ opts(title = '" + g.field +"')\n")
        fi.write("ggsave(pdffile)\n\n")
        
        #summary
        fi.write("p<-ggplot(GI)\n")
        s = g.graphpath + '/' + str(g.field) + str(g.run) + '_' + str(g.type) + str(g.start_year) + '-' + str(g.end_year) + '_' + str(g.size) + 'years_Summary.pdf'
        fi.write("pdffile <-c('" +s +"')\n")
        fi.write("pdf(pdffile)\n")
        fi.write("p + xlab('Year') + ylab('Number') + geom_point(aes(GI$End_Year,GI$Number_Of_Papers, color = 'Papers')) + geom_line(aes(GI$End_Year,GI$Number_Of_Papers, color = 'Papers')) +  opts(legend.title=theme_blank())+ opts(title = '" + g.field +"')")
        fi.write("+ geom_point(aes(GI$End_Year,GI$Number_Of_Authors, color = 'Authors')) + geom_line(aes(GI$End_Year,GI$Number_Of_Authors, color = 'Authors')) +  opts(legend.title=theme_blank())+ opts(title = '" + g.field +"')")
        fi.write("+ geom_point(aes(GI$End_Year,GI$Number_Of_Unweighted_Edges, color = 'Links')) + geom_line(aes(GI$End_Year,GI$Number_Of_Unweighted_Edges, color = 'Links')) +  opts(legend.title=theme_blank())+ opts(title = '" + g.field +"')")
        fi.write("+ geom_point(aes(GI$End_Year,GI$Number_Of_Edges, color = 'Edges')) + geom_line(aes(GI$End_Year,GI$Number_Of_Edges, color = 'Edges')) +  opts(legend.title=theme_blank())+ opts(title = '" + g.field +"')\n")
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
        fi.write("p + xlab('Year') + ylab('Percent of New Authors') + geom_point(aes(AB1$Start_Year,AB1$Percent_Of_New_Authors_Connected_to_atleast_one_new_author, color = 'With New')) + geom_point(aes(AB1$Start_Year,AB1$Percent_Of_New_Authors_Connected_to_atleast_one_old_author, color = 'With Old')) + geom_line(aes(AB1$Start_Year,AB1$Percent_Of_New_Authors_Connected_to_atleast_one_new_author, color = 'With New')) + geom_line(aes(AB1$Start_Year,AB1$Percent_Of_New_Authors_Connected_to_atleast_one_old_author, color = 'With Old')) + opts(legend.title=theme_blank()) + scale_y_continuous(limits = c(0, 100))\n")
        fi.write("ggsave(pdffile)\n\n")
        
        fi.write("p<-ggplot(AB1)\n")
        s = g.graphpath + '/' + str(g.field) + str(g.run) + '_' + str(g.type) + str(g.start_year) + '-' + str(g.end_year) + '_' + str(g.size) + 'years_OldAuthorAttachmentDistribution.pdf'
        fi.write("pdffile <-c('" +s +"')\n")
        fi.write("pdf(pdffile)\n")
        fi.write("p + xlab('Year') + ylab('Percent of old Authors') + geom_point(aes(AB1$Start_Year,AB1$Percent_Of_Old_Authors_Connected_to_atleast_one_new_author, color = 'With New')) + geom_point(aes(AB1$Start_Year,AB1$Percent_Of_Old_Authors_Connected_to_atleast_one_old_author, color = 'With Old')) + geom_point(aes(AB1$Start_Year,AB1$Percent_Of_Old_Authors_Connected_to_atleast_one_any_author, color = 'With Any')) + geom_line(aes(AB1$Start_Year,AB1$Percent_Of_Old_Authors_Connected_to_atleast_one_new_author, color = 'With New')) + geom_line(aes(AB1$Start_Year,AB1$Percent_Of_Old_Authors_Connected_to_atleast_one_old_author, color = 'With Old')) + geom_line(aes(AB1$Start_Year,AB1$Percent_Of_Old_Authors_Connected_to_atleast_one_any_author, color = 'With Any')) + opts(legend.title=theme_blank()) + scale_y_continuous(limits = c(0, 100))\n")
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
        fi.write("p + xlab('Year') + ylab('Percent New Links') + geom_point(aes(ABT1$Start_Year,ABT1$Percent_of_New_Links_Among_New_Authors, color = 'New-New')) + geom_point(aes(ABT1$Start_Year,ABT1$Percent_Of_Links_Between_New_and_Old, color = 'New-Old')) + geom_point(aes(ABT1$Start_Year,ABT1$Percent_of_New_Links_Between_Two_Old_Authors_Not_Connected_Before, color = 'Old-Old-1st')) + geom_point(aes(ABT1$Start_Year,ABT1$Percent_of_Links_Among_Old_Authors_Connected_Before, color = 'Old-Old-Again')) + geom_line(aes(ABT1$Start_Year,ABT1$Percent_of_New_Links_Among_New_Authors, color = 'New-New')) + geom_line(aes(ABT1$Start_Year,ABT1$Percent_Of_Links_Between_New_and_Old, color = 'New-Old')) + geom_line(aes(ABT1$Start_Year,ABT1$Percent_of_New_Links_Between_Two_Old_Authors_Not_Connected_Before, color = 'Old-Old-1st')) + geom_line(aes(ABT1$Start_Year,ABT1$Percent_of_Links_Among_Old_Authors_Connected_Before, color = 'Old-Old-Again')) + opts(legend.title=theme_blank()) + scale_y_continuous(limits = c(0, 100))\n")
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
        fi.write("p + xlab('Year') + ylab('Correlation with Number of New Links (Any Type)') + geom_point(aes(DC1$Start_Year,DC1$Correlation_Betwwen_Prev_Degree_and_New_Degree, color = 'Degree Centrality')) + geom_point(aes(CC1$Start_Year,CC1$Correlation_Betwwen_Prev_Closeness_and_New_Degree, color = 'Closeness Centrality')) + geom_point(aes(BC1$Start_Year,BC1$Correlation_Betwwen_Prev_Betweenness_and_New_Degree, color = 'Betweenness Centrality')) + geom_line(aes(DC1$Start_Year,DC1$Correlation_Betwwen_Prev_Degree_and_New_Degree, color = 'Degree Centrality')) + geom_line(aes(CC1$Start_Year,CC1$Correlation_Betwwen_Prev_Closeness_and_New_Degree, color = 'Closeness Centrality')) + geom_line(aes(BC1$Start_Year,BC1$Correlation_Betwwen_Prev_Betweenness_and_New_Degree, color = 'Betweenness Centrality')) + opts(legend.title=theme_blank()) + coord_cartesian(ylim=c(-0.5, 1.0))\n")
        fi.write("ggsave(pdffile)\n\n")
        
        fi.write("p<-ggplot(DC1)\n")
        s = g.graphpath + '/' + str(g.field) + str(g.run) + '_' + str(g.type) + str(g.start_year) + '-' + str(g.end_year) + '_' + str(g.size) + 'years_CentralityVnewLinkswithNewAuthors.pdf'
        fi.write("pdffile <-c('" +s +"')\n")
        fi.write("pdf(pdffile)\n")
        fi.write("p + xlab('Year') + ylab('Correlation with Number of New Links with New Authors') + geom_point(aes(DC1$Start_Year,DC1$Correlation_Betwwen_Prev_Degree_and_New_Authors_Degree, color = 'Degree Centrality')) + geom_point(aes(CC1$Start_Year,CC1$Correlation_Betwwen_Prev_Closeness_and_New_Authors_Degree, color = 'Closeness Centrality')) + geom_point(aes(BC1$Start_Year,BC1$Correlation_Betwwen_Prev_Betweenness_and_New_Authors_Degree, color = 'Betweenness Centrality')) + geom_line(aes(DC1$Start_Year,DC1$Correlation_Betwwen_Prev_Degree_and_New_Authors_Degree, color = 'Degree Centrality')) + geom_line(aes(CC1$Start_Year,CC1$Correlation_Betwwen_Prev_Closeness_and_New_Authors_Degree, color = 'Closeness Centrality')) + geom_line(aes(BC1$Start_Year,BC1$Correlation_Betwwen_Prev_Betweenness_and_New_Authors_Degree, color = 'Betweenness Centrality')) + opts(legend.title=theme_blank()) + coord_cartesian(ylim=c(-0.5, 1.0))\n")
        fi.write("ggsave(pdffile)\n\n")
        
        fi.write("p<-ggplot(DC1)\n")
        s = g.graphpath + '/' + str(g.field) + str(g.run) + '_' + str(g.type) + str(g.start_year) + '-' + str(g.end_year) + '_' + str(g.size) + 'years_CentralityVnewLinkswithOldAuthors.pdf'
        fi.write("pdffile <-c('" +s +"')\n")
        fi.write("pdf(pdffile)\n")
        fi.write("p + xlab('Year') + ylab('Correlation with Number of New Links with Old Authors') + geom_point(aes(DC1$Start_Year,DC1$Correlation_Betwwen_Prev_Degree_and_New_Old_Degree, color = 'Degree Centrality')) + geom_point(aes(CC1$Start_Year,CC1$Correlation_Betwwen_Prev_Closeness_and_New_Old_Degree, color = 'Closeness Centrality')) + geom_point(aes(BC1$Start_Year,BC1$Correlation_Betwwen_Prev_Betweenness_and_New_Old_Degree, color = 'Betweenness Centrality')) + geom_line(aes(DC1$Start_Year,DC1$Correlation_Betwwen_Prev_Degree_and_New_Old_Degree, color = 'Degree Centrality')) + geom_line(aes(CC1$Start_Year,CC1$Correlation_Betwwen_Prev_Closeness_and_New_Old_Degree, color = 'Closeness Centrality')) + geom_line(aes(BC1$Start_Year,BC1$Correlation_Betwwen_Prev_Betweenness_and_New_Old_Degree, color = 'Betweenness Centrality')) + opts(legend.title=theme_blank()) + coord_cartesian(ylim=c(-0.5, 1.0))\n")
        fi.write("ggsave(pdffile)\n\n")
        
        fi.write("#Preferrential Attachment ends\n\n\n")
        fi.close()
        
    def addDegreeDistribution(self, g, fs):
        fi = open(fs, 'a')
        fi.write("\n\n#Degree Distribution starts\n")
        fi.write("M<- read.table('" + g.CollaborationDistributionFile + "', header = TRUE, sep =';')\n" )
        
        fi.write("p<-ggplot(M)\n")
        s = g.graphpath + '/' + str(g.field) + str(g.run) + '_' + str(g.type) + str(g.start_year) + '-' + str(g.end_year) + '_' + str(g.size) + 'years_CollaborationDistribution.pdf'
        fi.write("pdffile <-c('" +s +"')\n")
        fi.write("pdf(pdffile)\n")
        fi.write("p + xlab('Log10(Collaborators)') + ylab('Log10(Number of Authors)') + geom_point(aes(M$Collaborators, M$Frequency)) + geom_line(aes(M$Collaborators, M$Frequency)) + coord_trans('log10','log10')\n")
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
        
    def makeIndividualGraphs(self, fs):
        for g in self.GList:
            self.addGeneralInfo(g,fs)
            self.addAbbasi2(g,fs)
            self.addAbbasi3(g,fs)
            self.addCentrality(g,fs)
            self.addDegreeDistribution(g,fs)
            self.addAuthorDistribution(g,fs)
            
    def makeComparisonGraphs(self, fs):
        print 'No comparison graph'
        
    def makeR(self):
        fs = os.path.realpath('../network-stats/makegraphs.r')
        f = open(fs,'w')
        f.close()
        self.printLib(fs)
        self.makeIndividualGraphs(fs)
        self.makeComparisonGraphs(fs)
        
if __name__ == "__main__":
    G = GraphDrawer()
    G.getData('/Users/macbookadministrator/Academic/Research/Network/communities/parameters/parameters-global.txt')
    G.makeR()
    