library(ggplot2)
library(scales)

#Directory setting and input

##################################

parameter<-read.table('../../parameters/parameters-global.csv', head = T, sep = ';')
community<-'../..'
dir<-paste(getwd(),'/',community, '/',parameter$NET_PATH,'/', sep= '')

GeneralInformationFile <- paste(dir,'nwa-',parameter$FIELD,'/runs/',parameter$RUN,'/output/statistics/',parameter$TYPE,parameter$START_YEAR,'-',parameter$END_YEAR,'_',parameter$SIZE,'years/whole_net/data/',parameter$FIELD,parameter$RUN,parameter$TYPE,parameter$START_YEAR,'-',parameter$END_YEAR,'_',parameter$SIZE,'GeneralInfo.csv',sep = '')
GI <- read.table(GeneralInformationFile, header = TRUE, sep =';') #GI is the table

##################################


#Number of Papers
p<-ggplot(GI)
f<- paste(dir, 'nwa-',parameter$FIELD,'/','runs/',parameter$RUN,'/output/statistics/',parameter$TYPE,parameter$START_YEAR,'-',parameter$END_YEAR,'_',parameter$SIZE,'years/whole_net/graphs/',parameter$FIELD,parameter$RUN,parameter$TYPE,parameter$START_YEAR,'-',parameter$END_YEAR,'_',parameter$SIZE,'NumberOfPapers.pdf', sep = '')
pdffile <-c(f)
pdf(pdffile)
p + xlab('Year') + ylab('Number of Papers Published') + geom_point(aes(GI$End_Year,GI$Number_Of_Papers, color = 'Papers')) + geom_line(aes(GI$End_Year,GI$Number_Of_Papers, color = 'Papers')) +  opts(legend.title=theme_blank())+ opts(title = paste('Field',substr(parameter$FIELD,6,6)))
ggsave(pdffile)


##################################


#Number of Authors
p<-ggplot(GI)
f<- paste(dir, 'nwa-',parameter$FIELD,'/','runs/',parameter$RUN,'/output/statistics/',parameter$TYPE,parameter$START_YEAR,'-',parameter$END_YEAR,'_',parameter$SIZE,'years/whole_net/graphs/',parameter$FIELD,parameter$RUN,parameter$TYPE,parameter$START_YEAR,'-',parameter$END_YEAR,'_',parameter$SIZE,'NumberOfAuthors.pdf', sep = '')
pdffile <-c(f)
pdf(pdffile)
p + xlab('Year') + ylab('Number of Authors')  + geom_point(aes(GI$End_Year,GI$Number_Of_Authors, color = 'Authors')) + geom_line(aes(GI$End_Year,GI$Number_Of_Authors, color = 'Authors')) + opts(legend.title=theme_blank())+ opts(title = paste('Field',substr(parameter$FIELD,6,6)))
ggsave(pdffile)


##################################


#Number of Edges
p<-ggplot(GI)
f<- paste(dir, 'nwa-',parameter$FIELD,'/','runs/',parameter$RUN,'/output/statistics/',parameter$TYPE,parameter$START_YEAR,'-',parameter$END_YEAR,'_',parameter$SIZE,'years/whole_net/graphs/',parameter$FIELD,parameter$RUN,parameter$TYPE,parameter$START_YEAR,'-',parameter$END_YEAR,'_',parameter$SIZE,'NumberOfEdges.pdf', sep = '')
pdffile <-c(f)
pdf(pdffile)
p + xlab('Year') + ylab('Number of Edges') + geom_point(aes(GI$End_Year,GI$Number_Of_Edges, color = 'Edges'))  + geom_line(aes(GI$End_Year,GI$Number_Of_Edges, color = 'Edges')) + opts(legend.title=theme_blank())+ opts(title = paste('Field',substr(parameter$FIELD,6,6)))+ opts(title = paste('Field',substr(parameter$FIELD,6,6)))
ggsave(pdffile)


##################################

#Number of Different Edges (Links)
p<-ggplot(GI)
f<- paste(dir, 'nwa-',parameter$FIELD,'/','runs/',parameter$RUN,'/output/statistics/',parameter$TYPE,parameter$START_YEAR,'-',parameter$END_YEAR,'_',parameter$SIZE,'years/whole_net/graphs/',parameter$FIELD,parameter$RUN,parameter$TYPE,parameter$START_YEAR,'-',parameter$END_YEAR,'_',parameter$SIZE,'NumberOfLinks.pdf', sep = '')
pdffile <-c(f)
pdf(pdffile)
p + xlab('Year') + ylab('Number of Links') + geom_point(aes(GI$End_Year,GI$Number_Of_Unweighted_Edges, color = 'Links')) + geom_line(aes(GI$End_Year,GI$Number_Of_Unweighted_Edges, color = 'Links')) + opts(legend.title=theme_blank()) + opts(title = paste('Field',substr(parameter$FIELD,6,6)))
ggsave(pdffile)


##################################

#Summary
p<-ggplot(GI)
f<- paste(dir, 'nwa-',parameter$FIELD,'/','runs/',parameter$RUN,'/output/statistics/',parameter$TYPE,parameter$START_YEAR,'-',parameter$END_YEAR,'_',parameter$SIZE,'years/whole_net/graphs/',parameter$FIELD,parameter$RUN,parameter$TYPE,parameter$START_YEAR,'-',parameter$END_YEAR,'_',parameter$SIZE,'Summary.pdf', sep = '')
pdffile <-c(f)
pdf(pdffile)
p + xlab('Year') + ylab('Number') + geom_point(aes(GI$End_Year,GI$Number_Of_Papers, color = 'Papers')) + geom_line(aes(GI$End_Year,GI$Number_Of_Papers, color = 'Papers')) + geom_point(aes(GI$End_Year,GI$Number_Of_Authors, color = 'Authors')) + geom_line(aes(GI$End_Year,GI$Number_Of_Authors, color = 'Authors')) + geom_point(aes(GI$End_Year,GI$Number_Of_Edges, color = 'Edges'))  + geom_line(aes(GI$End_Year,GI$Number_Of_Edges, color = 'Edges')) + geom_point(aes(GI$End_Year,GI$Number_Of_Unweighted_Edges, color = 'Links')) + geom_line(aes(GI$End_Year,GI$Number_Of_Unweighted_Edges, color = 'Links')) + opts(legend.title=theme_blank()) + opts(title = paste('Field',substr(parameter$FIELD,6,6)))
ggsave(pdffile)