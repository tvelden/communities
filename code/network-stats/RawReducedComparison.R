library(ggplot2)
library(scales)

Field1GeneralInfo <- read.table('/Users/Kallol/Testing/nwa-field1/runs/run1/output/statistics/field1run1discrete1991-2010_1years-statistics_files/field1run1discrete1991-2010_1GeneralInfo.csv', header = T, sep = ';')

Field1RAWGeneralInfo <- read.table('/Users/Kallol/Testing/nwa-field1/runs/run1RAW/output/statistics/field1run1RAWdiscrete1991-2010_1years-statistics_files/field1run1RAWdiscrete1991-2010_1GeneralInfo.csv', header = T, sep = ';')

Field2GeneralInfo <- read.table('/Users/Kallol/Testing/nwa-field2/runs/run1/output/statistics/field2run1discrete1991-2010_1years-statistics_files/field2run1discrete1991-2010_1GeneralInfo.csv', header = T, sep = ';')

Field2RAWGeneralInfo <- read.table('/Users/Kallol/Testing/nwa-field2/runs/run1RAW/output/statistics/field2run1RAWdiscrete1991-2010_1years-statistics_files/field2run1RAWdiscrete1991-2010_1GeneralInfo.csv', header = T, sep = ';')


#####Node Comparison graph
#Field 1
p<-ggplot(Field1GeneralInfo)
pdffile <-c('/Users/Kallol/Testing/Graphs/Field1RawReducedComparison_Nodes.pdf')
p + xlab('Year') + ylab('Number of Authors') + geom_point(aes(Field1GeneralInfo$Start_Year,Field1GeneralInfo$Number_Of_Authors, color = 'Reduced Field 1')) + geom_point(aes(Field1RAWGeneralInfo$Start_Year,Field1RAWGeneralInfo$Number_Of_Authors, color = 'Raw Field 1')) + geom_line(aes(Field1GeneralInfo$Start_Year,Field1GeneralInfo$Number_Of_Authors, color = 'Reduced Field 1')) + geom_line(aes(Field1RAWGeneralInfo$Start_Year,Field1RAWGeneralInfo$Number_Of_Authors, color = 'Raw Field 1'))+ opts(legend.title=theme_blank())
ggsave(pdffile)

#Field 2
p<-ggplot(Field2GeneralInfo)
pdffile <-c('/Users/Kallol/Testing/Graphs/Field2RawReducedComparison_Nodes.pdf')
p + xlab('Year') + ylab('Number of Authors') + geom_point(aes(Field2GeneralInfo$Start_Year,Field2GeneralInfo$Number_Of_Authors, color = 'Reduced Field 2')) + geom_point(aes(Field2RAWGeneralInfo$Start_Year,Field2RAWGeneralInfo$Number_Of_Authors, color = 'Raw Field 2')) + geom_line(aes(Field2GeneralInfo$Start_Year,Field2GeneralInfo$Number_Of_Authors, color = 'Reduced Field 2')) + geom_line(aes(Field2RAWGeneralInfo$Start_Year,Field2RAWGeneralInfo$Number_Of_Authors, color = 'Raw Field 2'))+ opts(legend.title=theme_blank())
ggsave(pdffile)

####Edge Comparison Graph
#Field 1
p<-ggplot(Field1GeneralInfo)
pdffile <-c('/Users/Kallol/Testing/Graphs/Field1RawReducedComparison_Edges.pdf')
p + xlab('Year') + ylab('Number of Edges') + geom_point(aes(Field1GeneralInfo$Start_Year,Field1GeneralInfo$Number_Of_Edges, color = 'Reduced Field 1')) + geom_point(aes(Field1RAWGeneralInfo$Start_Year,Field1RAWGeneralInfo$Number_Of_Edges, color = 'Raw Field 1')) + geom_line(aes(Field1GeneralInfo$Start_Year,Field1GeneralInfo$Number_Of_Edges, color = 'Reduced Field 1')) + geom_line(aes(Field1RAWGeneralInfo$Start_Year,Field1RAWGeneralInfo$Number_Of_Edges, color = 'Raw Field 1'))+ opts(legend.title=theme_blank())
ggsave(pdffile)

#Field 2
p<-ggplot(Field2GeneralInfo)
pdffile <-c('/Users/Kallol/Testing/Graphs/Field2RawReducedComparison_Edges.pdf')
p + xlab('Year') + ylab('Number of Edges') + geom_point(aes(Field2GeneralInfo$Start_Year,Field2GeneralInfo$Number_Of_Edges, color = 'Reduced Field 2')) + geom_point(aes(Field2RAWGeneralInfo$Start_Year,Field2RAWGeneralInfo$Number_Of_Edges, color = 'Raw Field 2')) + geom_line(aes(Field2GeneralInfo$Start_Year,Field2GeneralInfo$Number_Of_Edges, color = 'Reduced Field 2')) + geom_line(aes(Field2RAWGeneralInfo$Start_Year,Field2RAWGeneralInfo$Number_Of_Edges, color = 'Raw Field 2'))+ opts(legend.title=theme_blank())
ggsave(pdffile)


###Paper Comparison
#Field 1
p<-ggplot(Field1GeneralInfo)
pdffile <-c('/Users/Kallol/Testing/Graphs/Field1RawReducedComparison_Papers.pdf')
p + xlab('Year') + ylab('Number of Papers Published') + geom_point(aes(Field1GeneralInfo$Start_Year,Field1GeneralInfo$Number_Of_Papers, color = 'Reduced Field 1')) + geom_point(aes(Field1RAWGeneralInfo$Start_Year,Field1RAWGeneralInfo$Number_Of_Papers, color = 'Raw Field 1')) + geom_line(aes(Field1GeneralInfo$Start_Year,Field1GeneralInfo$Number_Of_Papers, color = 'Reduced Field 1')) + geom_line(aes(Field1RAWGeneralInfo$Start_Year,Field1RAWGeneralInfo$Number_Of_Papers, color = 'Raw Field 1'))+ opts(legend.title=theme_blank())
ggsave(pdffile)

#Field2
p<-ggplot(Field2GeneralInfo)
pdffile <-c('/Users/Kallol/Testing/Graphs/Field2RawReducedComparison_Papers.pdf')
p + xlab('Year') + ylab('Number of Papers Published') + geom_point(aes(Field2GeneralInfo$Start_Year,Field2GeneralInfo$Number_Of_Papers, color = 'Reduced Field 2')) + geom_point(aes(Field2RAWGeneralInfo$Start_Year,Field2RAWGeneralInfo$Number_Of_Papers, color = 'Raw Field 2')) + geom_line(aes(Field2GeneralInfo$Start_Year,Field2GeneralInfo$Number_Of_Papers, color = 'Reduced Field 2')) + geom_line(aes(Field2RAWGeneralInfo$Start_Year,Field2RAWGeneralInfo$Number_Of_Papers, color = 'Raw Field 2'))+ opts(legend.title=theme_blank())
ggsave(pdffile)

###Bettencort Graph: Discrete


Field1GeneralInfo <- read.table('/Users/Kallol/Testing/nwa-field1/runs/run1/output/statistics/field1run1discrete1991-2010_1years-statistics_files/field1run1discrete1991-2010_1GeneralInfo.csv', header = T, sep = ';')

Field1RAWGeneralInfo <- read.table('/Users/Kallol/Testing/nwa-field1/runs/run1RAW/output/statistics/field1run1RAWdiscrete1991-2010_1years-statistics_files/field1run1RAWdiscrete1991-2010_1GeneralInfo.csv', header = T, sep = ';')

Field2GeneralInfo <- read.table('/Users/Kallol/Testing/nwa-field2/runs/run1/output/statistics/field2run1discrete1991-2010_1years-statistics_files/field2run1discrete1991-2010_1GeneralInfo.csv', header = T, sep = ';')

Field2RAWGeneralInfo <- read.table('/Users/Kallol/Testing/nwa-field2/runs/run1RAW/output/statistics/field2run1RAWdiscrete1991-2010_1years-statistics_files/field2run1RAWdiscrete1991-2010_1GeneralInfo.csv', header = T, sep = ';')

#Field 1
#RAW
p<-ggplot(Field1RAWGeneralInfo)
res=lm(log10(Field1RAWGeneralInfo$Number_Of_Authors)~log10(Field1RAWGeneralInfo$Number_of_Unweighted_Edges ))
pdffile <-c('/Users/Kallol/Testing/Graphs/Field1RAWDiscreteBettencourtFigure1_Author_Connection.pdf')
p + xlab('log(number of authors)') + ylab('log(number of conenctions)') + geom_point(aes(Field1RAWGeneralInfo$Number_of_Unweighted_Edges,Field1RAWGeneralInfo$Number_of_Unweighted_Edges )) + coord_trans(x = "log10", y = "log10") + geom_smooth(aes(x = Field1RAWGeneralInfo$Number_of_Unweighted_Edges, y = Field1RAWGeneralInfo$Number_of_Unweighted_Edges), method = lm) + opts(title = res)
ggsave(pdffile)
#Reduced
p<-ggplot(Field1GeneralInfo)
res=lm(log10(Field1GeneralInfo$Number_Of_Authors)~log10(Field1GeneralInfo$Number_of_Unweighted_Edges ))
pdffile <-c('/Users/Kallol/Testing/Graphs/Field1DiscreteBettencourtFigure1_Author_Connection.pdf')
p + xlab('log(number of authors)') + ylab('log(number of conenctions)') + geom_point(aes(Field1GeneralInfo$Number_of_Unweighted_Edges,Field1GeneralInfo$Number_of_Unweighted_Edges )) + coord_trans(x = "log10", y = "log10") + geom_smooth(aes(x = Field1GeneralInfo$Number_of_Unweighted_Edges, y = Field1GeneralInfo$Number_of_Unweighted_Edges), method = lm) + opts(title = res)
ggsave(pdffile)

#Field2
#RAW
p<-ggplot(Field2RAWGeneralInfo)
res=lm(log10(Field2RAWGeneralInfo$Number_Of_Authors)~log10(Field2RAWGeneralInfo$Number_of_Unweighted_Edges ))
pdffile <-c('/Users/Kallol/Testing/Graphs/Field2RAWDiscreteBettencourtFigure1_Author_Connection.pdf')
p + xlab('log(number of authors)') + ylab('log(number of conenctions)') + geom_point(aes(Field2RAWGeneralInfo$Number_of_Unweighted_Edges,Field2RAWGeneralInfo$Number_of_Unweighted_Edges )) + coord_trans(x = "log10", y = "log10") + geom_smooth(aes(x = Field2RAWGeneralInfo$Number_of_Unweighted_Edges, y = Field2RAWGeneralInfo$Number_of_Unweighted_Edges), method = lm) + opts(title = res)
ggsave(pdffile)

#Redued
p<-ggplot(Field2GeneralInfo)
res=lm(log10(Field2GeneralInfo$Number_Of_Authors)~log10(Field2GeneralInfo$Number_of_Unweighted_Edges ))
pdffile <-c('/Users/Kallol/Testing/Graphs/Field2DiscreteBettencourtFigure1_Author_Connection.pdf')
p + xlab('log(number of authors)') + ylab('log(number of conenctions)') + geom_point(aes(Field2GeneralInfo$Number_of_Unweighted_Edges,Field2GeneralInfo$Number_of_Unweighted_Edges )) + coord_trans(x = "log10", y = "log10") + geom_smooth(aes(x = Field2GeneralInfo$Number_of_Unweighted_Edges, y = Field2GeneralInfo$Number_of_Unweighted_Edges), method = lm) + opts(title = res)
ggsave(pdffile)

###Bettencort Graph: Accumulative

Field1GeneralInfo <- read.table('/Users/Kallol/Testing/nwa-field1/runs/run1/output/statistics/field1run1accumulative1991-2010_1years-statistics_files/field1run1accumulative1991-2010_1GeneralInfo.csv', header = T, sep = ';')

Field1RAWGeneralInfo <- read.table('/Users/Kallol/Testing/nwa-field1/runs/run1RAW/output/statistics/field1run1RAWaccumulative1991-2010_1years-statistics_files/field1run1RAWaccumulative1991-2010_1GeneralInfo.csv', header = T, sep = ';')

Field2GeneralInfo <- read.table('/Users/Kallol/Testing/nwa-field2/runs/run1/output/statistics/field2run1accumulative1991-2010_1years-statistics_files/field2run1accumulative1991-2010_1GeneralInfo.csv', header = T, sep = ';')

Field2RAWGeneralInfo <- read.table('/Users/Kallol/Testing/nwa-field2/runs/run1RAW/output/statistics/field2run1RAWaccumulative1991-2010_1years-statistics_files/field2run1RAWaccumulative1991-2010_1GeneralInfo.csv', header = T, sep = ';')


#Field 1
#RAW
p<-ggplot(Field1RAWGeneralInfo)
res=lm(log10(Field1RAWGeneralInfo$Number_Of_Authors)~log10(Field1RAWGeneralInfo$Number_of_Unweighted_Edges ))
pdffile <-c('/Users/Kallol/Testing/Graphs/Field1RAWAccumulativeBettencourtFigure1_Author_Connection.pdf')
p + xlab('log(number of authors)') + ylab('log(number of conenctions)') + geom_point(aes(Field1RAWGeneralInfo$Number_of_Unweighted_Edges,Field1RAWGeneralInfo$Number_of_Unweighted_Edges )) + coord_trans(x = "log10", y = "log10") + geom_smooth(aes(x = Field1RAWGeneralInfo$Number_of_Unweighted_Edges, y = Field1RAWGeneralInfo$Number_of_Unweighted_Edges), method = lm) + opts(title = res)
ggsave(pdffile)
#Reduced
p<-ggplot(Field1GeneralInfo)
res=lm(log10(Field1GeneralInfo$Number_Of_Authors)~log10(Field1GeneralInfo$Number_of_Unweighted_Edges ))
pdffile <-c('/Users/Kallol/Testing/Graphs/Field1AccumulativeBettencourtFigure1_Author_Connection.pdf')
p + xlab('log(number of authors)') + ylab('log(number of conenctions)') + geom_point(aes(Field1GeneralInfo$Number_of_Unweighted_Edges,Field1GeneralInfo$Number_of_Unweighted_Edges )) + coord_trans(x = "log10", y = "log10") + geom_smooth(aes(x = Field1GeneralInfo$Number_of_Unweighted_Edges, y = Field1GeneralInfo$Number_of_Unweighted_Edges), method = lm) + opts(title = res)
ggsave(pdffile)

#Field2
#RAW
p<-ggplot(Field2RAWGeneralInfo)
res=lm(log10(Field2RAWGeneralInfo$Number_Of_Authors)~log10(Field2RAWGeneralInfo$Number_of_Unweighted_Edges ))
pdffile <-c('/Users/Kallol/Testing/Graphs/Field2RAWAccumulativeBettencourtFigure1_Author_Connection.pdf')
p + xlab('log(number of authors)') + ylab('log(number of conenctions)') + geom_point(aes(Field2RAWGeneralInfo$Number_of_Unweighted_Edges,Field2RAWGeneralInfo$Number_of_Unweighted_Edges )) + coord_trans(x = "log10", y = "log10") + geom_smooth(aes(x = Field2RAWGeneralInfo$Number_of_Unweighted_Edges, y = Field2RAWGeneralInfo$Number_of_Unweighted_Edges), method = lm) + opts(title = res)
ggsave(pdffile)

#Redued
p<-ggplot(Field2GeneralInfo)
res=lm(log10(Field2GeneralInfo$Number_Of_Authors)~log10(Field2GeneralInfo$Number_of_Unweighted_Edges ))
pdffile <-c('/Users/Kallol/Testing/Graphs/Field2AccumulativeBettencourtFigure1_Author_Connection.pdf')
p + xlab('log(number of authors)') + ylab('log(number of conenctions)') + geom_point(aes(Field2GeneralInfo$Number_of_Unweighted_Edges,Field2GeneralInfo$Number_of_Unweighted_Edges )) + coord_trans(x = "log10", y = "log10") + geom_smooth(aes(x = Field2GeneralInfo$Number_of_Unweighted_Edges, y = Field2GeneralInfo$Number_of_Unweighted_Edges), method = lm) + opts(title = res)
ggsave(pdffile)




M<-read.table('/Users/Kallol/Testing/nwa-field1/runs/run1/output/statistics/field1run1discrete1991-2010_1years-statistics_files/field1run1discrete1991-2010_1CollaborationDistribution.csv', header = TRUE, sep = ';')
M1<-read.table('/Users/Kallol/Testing/nwa-field1/runs/run1RAW/output/statistics/field1run1RAWdiscrete1991-2010_1years-statistics_files/field1run1RAWdiscrete1991-2010_1CollaborationDistribution.csv', header = TRUE, sep = ';')

pdffile <-c("/Users/kallol/Testing/Graphs/Field1Reduced_Milojevic_1.pdf")
pdf(pdffile)
p<-ggplot(M)
p + xlab('Log10(Collaborators)') + ylab('Log10(Number of Authors)') + geom_point(aes(log10(M$Collaborators), log10(M$Frequency))) + geom_line(aes(log10(M$Collaborators), log10(M$Frequency)))
ggsave(pdffile)

pdffile <-c("/Users/kallol/Testing/Graphs/Field1Raw_Milojevic_1.pdf")
pdf(pdffile)
p<-ggplot(M1)
p + xlab('Log10(Collaborators)') + ylab('Log10(Number of Authors)') + geom_point(aes(log10(M1$Collaborators), log10(M1$Frequency))) + geom_line(aes(log10(M1$Collaborators), log10(M1$Frequency)))
ggsave(pdffile)


M<-read.table('/Users/Kallol/Testing/nwa-field2/runs/run1/output/statistics/field2run1discrete1991-2010_1years-statistics_files/field2run1discrete1991-2010_1CollaborationDistribution.csv', header = TRUE, sep = ';')
M1<-read.table('/Users/Kallol/Testing/nwa-field2/runs/run1RAW/output/statistics/field2run1RAWdiscrete1991-2010_1years-statistics_files/field2run1RAWdiscrete1991-2010_1CollaborationDistribution.csv', header = TRUE, sep = ';')

pdffile <-c("/Users/kallol/Testing/Graphs/Field2Reduced_Milojevic_1.pdf")
pdf(pdffile)
p<-ggplot(M)
p + xlab('Log10(Collaborators)') + ylab('Log10(Number of Authors)') + geom_point(aes(log10(M$Collaborators), log10(M$Frequency))) + geom_line(aes(log10(M$Collaborators), log10(M$Frequency)))
ggsave(pdffile)

pdffile <-c("/Users/kallol/Testing/Graphs/Field2Raw_Milojevic_1.pdf")
pdf(pdffile)
p<-ggplot(M1)
p + xlab('Log10(Collaborators)') + ylab('Log10(Number of Authors)') + geom_point(aes(log10(M1$Collaborators), log10(M1$Frequency))) + geom_line(aes(log10(M1$Collaborators), log10(M1$Frequency)))
ggsave(pdffile)
