library(ggplot2)
library(scales)






#Preferrential Attachment starts
DC1<- read.table('/Users/macbookadministrator/Academic/Research/Network/Output/nwa-field2/runs/run1norm-dis-hfree/output/statistics/accumulative1991-2010_1years/generic/allyears/whole_net/tables/field2run1norm-dis-hfree_accumulative1991-2010_1years_wholenet_DegreeCentrality_hub.csv', header = TRUE, sep =';')
CC1<- read.table('/Users/macbookadministrator/Academic/Research/Network/Output/nwa-field2/runs/run1norm-dis-hfree/output/statistics/accumulative1991-2010_1years/generic/allyears/whole_net/tables/field2run1norm-dis-hfree_accumulative1991-2010_1years_wholenet_ClosenessCentrality_hub.csv', header = TRUE, sep =';')
BC1<- read.table('/Users/macbookadministrator/Academic/Research/Network/Output/nwa-field2/runs/run1norm-dis-hfree/output/statistics/accumulative1991-2010_1years/generic/allyears/whole_net/tables/field2run1norm-dis-hfree_accumulative1991-2010_1years_wholenet_BetweennessCentrality_hub.csv', header = TRUE, sep =';')


p<-ggplot(DC1)
pdffile <-c('/Users/macbookadministrator/Academic/Research/Network/Output/nwa-field2/runs/run1norm-dis-hfree/output/statistics/accumulative1991-2010_1years/generic/allyears/whole_net/images/field2run1norm-dis-hfree_accumulative1991-2010_1years_CentralityVnewLinks_hub.pdf')
pdf(pdffile)
p + xlab('Year') + ylab('Spearman Correlation with Number of New Links (Any Type)') + geom_point(aes(DC1$End_Year,DC1$Correlation_Between_Prev_Degree_and_New_Degree, shape = 'Degree Centrality')) + geom_point(aes(CC1$End_Year,CC1$Correlation_Between_Prev_Closeness_and_New_Degree, shape = 'Closeness Centrality')) + geom_point(aes(BC1$End_Year,BC1$Correlation_Between_Prev_Betweenness_and_New_Degree, shape = 'Betweenness Centrality')) + geom_line(aes(DC1$End_Year,DC1$Correlation_Between_Prev_Degree_and_New_Degree, shape = 'Degree Centrality')) + geom_line(aes(CC1$End_Year,CC1$Correlation_Between_Prev_Closeness_and_New_Degree, shape = 'Closeness Centrality')) + geom_line(aes(BC1$End_Year,BC1$Correlation_Between_Prev_Betweenness_and_New_Degree, shape = 'Betweenness Centrality')) + opts(legend.title=theme_blank()) + coord_cartesian(ylim=c(-0.5, 1.0))
ggsave(pdffile)

p<-ggplot(DC1)
pdffile <-c('/Users/macbookadministrator/Academic/Research/Network/Output/nwa-field2/runs/run1norm-dis-hfree/output/statistics/accumulative1991-2010_1years/generic/allyears/whole_net/images/field2run1norm-dis-hfree_accumulative1991-2010_1years_CentralityVnewLinkswithNewAuthors_hub.pdf')
pdf(pdffile)
p + xlab('Year') + ylab('Spearman correlation (Collaborations with New Authors)') + geom_point(aes(DC1$End_Year,DC1$Correlation_Between_Prev_Degree_and_New_Authors_Degree, shape = 'Degree Centrality')) + geom_point(aes(CC1$End_Year,CC1$Correlation_Between_Prev_Closeness_and_New_Authors_Degree, shape = 'Closeness Centrality')) + geom_point(aes(BC1$End_Year,BC1$Correlation_Between_Prev_Betweenness_and_New_Authors_Degree, shape = 'Betweenness Centrality')) + geom_line(aes(DC1$End_Year,DC1$Correlation_Between_Prev_Degree_and_New_Authors_Degree, shape = 'Degree Centrality')) + geom_line(aes(CC1$End_Year,CC1$Correlation_Between_Prev_Closeness_and_New_Authors_Degree, shape = 'Closeness Centrality')) + geom_line(aes(BC1$End_Year,BC1$Correlation_Between_Prev_Betweenness_and_New_Authors_Degree, shape = 'Betweenness Centrality')) + opts(legend.title=theme_blank()) + coord_cartesian(ylim=c(-0.5, 1.0))
ggsave(pdffile)

p<-ggplot(DC1)
pdffile <-c('/Users/macbookadministrator/Academic/Research/Network/Output/nwa-field2/runs/run1norm-dis-hfree/output/statistics/accumulative1991-2010_1years/generic/allyears/whole_net/images/field2run1norm-dis-hfree_accumulative1991-2010_1years_CentralityVnewLinkswithOldAuthors_hub.pdf')
pdf(pdffile)
p + xlab('Year') + ylab('Spearman correlation (New Collaborations between Existing Authors)') + geom_point(aes(DC1$End_Year,DC1$Correlation_Between_Prev_Degree_and_New_Old_Degree, shape = 'Degree Centrality')) + geom_point(aes(CC1$End_Year,CC1$Correlation_Between_Prev_Closeness_and_New_Old_Degree, shape = 'Closeness Centrality')) + geom_point(aes(BC1$End_Year,BC1$Correlation_Between_Prev_Betweenness_and_New_Old_Degree, shape = 'Betweenness Centrality')) + geom_line(aes(DC1$End_Year,DC1$Correlation_Between_Prev_Degree_and_New_Old_Degree, shape = 'Degree Centrality')) + geom_line(aes(CC1$End_Year,CC1$Correlation_Between_Prev_Closeness_and_New_Old_Degree, shape = 'Closeness Centrality')) + geom_line(aes(BC1$End_Year,BC1$Correlation_Between_Prev_Betweenness_and_New_Old_Degree, shape = 'Betweenness Centrality')) + opts(legend.title=theme_blank()) + coord_cartesian(ylim=c(-0.5, 1.0))
ggsave(pdffile)

#Preferrential Attachment ends




#Degree Distribution starts
M<- read.table('/Users/macbookadministrator/Academic/Research/Network/Output/nwa-field2/runs/run1norm-dis-hfree/output/statistics/accumulative1991-2010_1years/generic/allyears/whole_net/tables/field2run1norm-dis-hfree_accumulative1991-2010_1years_wholenet_CollaborationDistribution_hub.csv', header = TRUE, sep =';')
p<-ggplot(M)
pdffile <-c('/Users/macbookadministrator/Academic/Research/Network/Output/nwa-field2/runs/run1norm-dis-hfree/output/statistics/accumulative1991-2010_1years/generic/allyears/whole_net/images/field2run1norm-dis-hfree_accumulative1991-2010_1years_CollaborationDistribution_hub.pdf')
pdf(pdffile)
p + xlab('Number of Authors') + ylab('Number of COllaborators (per author)') + geom_point(aes(M$Collaborators, M$Frequency)) + geom_line(aes(M$Collaborators, M$Frequency)) + coord_trans('log10','log10')
ggsave(pdffile)

#Degree Distribution ends




#p-Values for Preferrential Attachment starts
DC1<- read.table('/Users/macbookadministrator/Academic/Research/Network/Output/nwa-field2/runs/run1norm-dis-hfree/output/statistics/accumulative1991-2010_1years/generic/allyears/whole_net/tables/field2run1norm-dis-hfree_accumulative1991-2010_1years_wholenet_DegreeCentrality_hub.csv', header = TRUE, sep =';')
CC1<- read.table('/Users/macbookadministrator/Academic/Research/Network/Output/nwa-field2/runs/run1norm-dis-hfree/output/statistics/accumulative1991-2010_1years/generic/allyears/whole_net/tables/field2run1norm-dis-hfree_accumulative1991-2010_1years_wholenet_ClosenessCentrality_hub.csv', header = TRUE, sep =';')
BC1<- read.table('/Users/macbookadministrator/Academic/Research/Network/Output/nwa-field2/runs/run1norm-dis-hfree/output/statistics/accumulative1991-2010_1years/generic/allyears/whole_net/tables/field2run1norm-dis-hfree_accumulative1991-2010_1years_wholenet_BetweennessCentrality_hub.csv', header = TRUE, sep =';')


p<-ggplot(DC1)
pdffile <-c('/Users/macbookadministrator/Academic/Research/Network/Output/nwa-field2/runs/run1norm-dis-hfree/output/statistics/accumulative1991-2010_1years/generic/allyears/whole_net/images/field2run1norm-dis-hfree_accumulative1991-2010_1years_pCentralityVnewLinks_hub.pdf')
pdf(pdffile)
p + xlab('Year') + ylab('p-Values of the Spearman Correlation with Number of New Links (Any Type)') + geom_point(aes(DC1$End_Year,DC1$pCDND, shape = 'Degree Centrality')) + geom_point(aes(CC1$End_Year,CC1$pCDND, shape = 'Closeness Centrality')) + geom_point(aes(BC1$End_Year,BC1$pCDND, shape = 'Betweenness Centrality')) + geom_line(aes(DC1$End_Year,DC1$pCDND, shape = 'Degree Centrality')) + geom_line(aes(CC1$End_Year,CC1$pCDND, shape = 'Closeness Centrality')) + geom_line(aes(BC1$End_Year,BC1$pCDND, shape = 'Betweenness Centrality')) + opts(legend.title=theme_blank())
ggsave(pdffile)

p<-ggplot(DC1)
pdffile <-c('/Users/macbookadministrator/Academic/Research/Network/Output/nwa-field2/runs/run1norm-dis-hfree/output/statistics/accumulative1991-2010_1years/generic/allyears/whole_net/images/field2run1norm-dis-hfree_accumulative1991-2010_1years_pCentralityVnewLinkswithNewAuthors_hub.pdf')
pdf(pdffile)
p + xlab('Year') + ylab('p-Values of the Spearman correlation (Collaborations with New Authors)') + geom_point(aes(DC1$End_Year,DC1$pCDNAD, shape = 'Degree Centrality')) + geom_point(aes(CC1$End_Year,CC1$pCDNAD, shape = 'Closeness Centrality')) + geom_point(aes(BC1$End_Year,BC1$pCDNAD, shape = 'Betweenness Centrality')) + geom_line(aes(DC1$End_Year,DC1$pCDNAD, shape = 'Degree Centrality')) + geom_line(aes(CC1$End_Year,CC1$pCDNAD, shape = 'Closeness Centrality')) + geom_line(aes(BC1$End_Year,BC1$pCDNAD, shape = 'Betweenness Centrality')) + opts(legend.title=theme_blank())
ggsave(pdffile)

p<-ggplot(DC1)
pdffile <-c('/Users/macbookadministrator/Academic/Research/Network/Output/nwa-field2/runs/run1norm-dis-hfree/output/statistics/accumulative1991-2010_1years/generic/allyears/whole_net/images/field2run1norm-dis-hfree_accumulative1991-2010_1years_pCentralityVnewLinkswithOldAuthors_hub.pdf')
pdf(pdffile)
p + xlab('Year') + ylab('p-Values of the Spearman correlation (New Collaborations between Existing Authors)')+ geom_point(aes(DC1$End_Year,DC1$pCDNOD, shape = 'Degree Centrality')) + geom_point(aes(CC1$End_Year,CC1$pCDNOD, shape = 'Closeness Centrality')) + geom_point(aes(BC1$End_Year,BC1$pCDNOD, shape = 'Betweenness Centrality')) + geom_line(aes(DC1$End_Year,DC1$pCDNOD, shape = 'Degree Centrality')) + geom_line(aes(CC1$End_Year,CC1$pCDNOD, shape = 'Closeness Centrality')) + geom_line(aes(BC1$End_Year,BC1$pCDNOD, shape = 'Betweenness Centrality')) + opts(legend.title=theme_blank())
ggsave(pdffile)

#p-Values of Preferrential Attachment ends


