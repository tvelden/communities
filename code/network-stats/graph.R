library(ggplot2)

Field1GeneralInformationFile <- '/Users/Kallol/Testing/nwa-field1/runs/run1/output/statistics/field1run1discrete1991-2010_1years-statistics_files/field1run1discrete1991-2010_1GeneralInfo.csv'
Field2GeneralInformationFile <- '/Users/Kallol/Testing/nwa-field2/runs/run1/output/statistics/field2run1discrete1991-2010_1years-statistics_files/field2run1discrete1991-2010_1GeneralInfo.csv'


GI1 <- read.table(Field1GeneralInformationFile, header = TRUE, sep =';')
GI2 <- read.table(Field2GeneralInformationFile, header = TRUE, sep =';')

p<-ggplot(GI1)

pdffile <-c("/Users/Kallol/Testing/Graphs/PaperComparison.pdf")
pdf(pdffile)
p + xlab('Year') + ylab('Number of Papers Published') + geom_point(aes(GI1$Start_Year,GI1$Number_Of_Papers, color = 'Field 1')) + geom_point(aes(GI2$Start_Year,GI2$Number_Of_Papers, color = 'Field 2')) + geom_line(aes(GI1$Start_Year,GI1$Number_Of_Papers, color = 'Field 1')) + geom_line(aes(GI2$Start_Year,GI2$Number_Of_Papers, color = 'Field 2'))+ opts(legend.title=theme_blank())
ggsave(pdffile)


pdffile <-c("/Users/Kallol/Testing/Graphs/AuthorComparison.pdf")
pdf(pdffile)
p + xlab('Year') + ylab('Number of Active') + geom_point(aes(GI1$Start_Year,GI1$Number_Of_Authors, color = 'Field 1')) + geom_point(aes(GI2$Start_Year,GI2$Number_Of_Authors, color = 'Field 2')) + geom_line(aes(GI1$Start_Year,GI1$Number_Of_Authors, color = 'Field 1')) + geom_line(aes(GI2$Start_Year,GI2$Number_Of_Authors, color = 'Field 2'))+ opts(legend.title=theme_blank())
ggsave(pdffile)

pdffile <-c("/Users/Kallol/Testing/Graphs/LinkComparison.pdf")
pdf(pdffile)
p + xlab('Year') + ylab('Number of Links') + geom_point(aes(GI1$Start_Year,GI1$Number_Of_Edges, color = 'Field 1')) + geom_point(aes(GI2$Start_Year,GI2$Number_Of_Edges, color = 'Field 2')) + geom_line(aes(GI1$Start_Year,GI1$Number_Of_Edges, color = 'Field 1')) + geom_line(aes(GI2$Start_Year,GI2$Number_Of_Edges, color = 'Field 2'))+ opts(legend.title=theme_blank())
ggsave(pdffile)

pdffile <-c("/Users/Kallol/Testing/Graphs/Field1.pdf")
pdf(pdffile)
p + xlab('Year') + ylab('Number') + geom_point(aes(GI1$Start_Year,GI1$Number_Of_Papers, color = 'Papers')) + geom_point(aes(GI1$Start_Year,GI1$Number_Of_Authors, color = 'Authors')) + geom_point(aes(GI1$Start_Year,GI1$Number_Of_Edges, color = 'Links')) + geom_line(aes(GI1$Start_Year,GI1$Number_Of_Papers, color = 'Papers')) + geom_line(aes(GI1$Start_Year,GI1$Number_Of_Authors, color = 'Authors')) + geom_line(aes(GI1$Start_Year,GI1$Number_Of_Edges, color = 'Links')) + opts(legend.title=theme_blank())
ggsave(pdffile)


pdffile <-c("/Users/Kallol/Testing/Graphs/Field2.pdf")
pdf(pdffile)
p + xlab('Year') + ylab('Number') + geom_point(aes(GI2$Start_Year,GI2$Number_Of_Papers, color = 'Papers')) + geom_point(aes(GI2$Start_Year,GI2$Number_Of_Authors, color = 'Authors')) + geom_point(aes(GI2$Start_Year,GI2$Number_Of_Edges, color = 'Links')) + geom_line(aes(GI2$Start_Year,GI2$Number_Of_Papers, color = 'Papers')) + geom_line(aes(GI2$Start_Year,GI2$Number_Of_Authors, color = 'Authors')) + geom_line(aes(GI2$Start_Year,GI2$Number_Of_Edges, color = 'Links')) + opts(legend.title=theme_blank())
ggsave(pdffile)

DC1<-read.table('/Users/Kallol/Testing/nwa-field1/runs/run1/output/statistics/field1run1discrete1991-2010_1years-statistics_files/field1run1discrete1991-2010_1years-DegreeCentrality.csv', header = TRUE, sep =';')
CC1<-read.table('/Users/Kallol/Testing/nwa-field1/runs/run1/output/statistics/field1run1discrete1991-2010_1years-statistics_files/field1run1discrete1991-2010_1years-ClosenessCentrality.csv', header = TRUE, sep =';')
BC1<-read.table('/Users/Kallol/Testing/nwa-field1/runs/run1/output/statistics/field1run1discrete1991-2010_1years-statistics_files/field1run1discrete1991-2010_1years-BetweennessCentrality.csv', header = TRUE, sep =';')

p<-ggplot(DC1)

pdffile <-c("/Users/Kallol/Testing/Graphs/PA_Field1_ComparisonForNewLinkAttachment.pdf")
pdf(pdffile)
p + xlab('Year') + ylab('Correlation with Number of New Links (Any Type)') + geom_point(aes(DC1$Start_Year,DC1$Correlation_Betwwen_Prev_Degree_and_New_Degree, color = 'Degree Centrality')) + geom_point(aes(CC1$Start_Year,CC1$Correlation_Betwwen_Prev_Closeness_and_New_Degree, color = 'Closeness Centrality')) + geom_point(aes(BC1$Start_Year,BC1$Correlation_Betwwen_Prev_Betweenness_and_New_Degree, color = 'Betweenness Centrality')) + geom_line(aes(DC1$Start_Year,DC1$Correlation_Betwwen_Prev_Degree_and_New_Degree, color = 'Degree Centrality')) + geom_line(aes(CC1$Start_Year,CC1$Correlation_Betwwen_Prev_Closeness_and_New_Degree, color = 'Closeness Centrality')) + geom_line(aes(BC1$Start_Year,BC1$Correlation_Betwwen_Prev_Betweenness_and_New_Degree, color = 'Betweenness Centrality')) + opts(legend.title=theme_blank()) + coord_cartesian(ylim=c(-0.5, 1.0))

ggsave(pdffile)

pdffile <-c("/Users/Kallol/Testing/Graphs/PA_Field1_ComparisonForNewLinkWithNewAuthorsAttachment.pdf")
pdf(pdffile)
p + xlab('Year') + ylab('Correlation with Number of New Links with New Authors') + geom_point(aes(DC1$Start_Year,DC1$Correlation_Betwwen_Prev_Degree_and_New_Authors_Degree, color = 'Degree Centrality')) + geom_point(aes(CC1$Start_Year,CC1$Correlation_Betwwen_Prev_Closeness_and_New_Authors_Degree, color = 'Closeness Centrality')) + geom_point(aes(BC1$Start_Year,BC1$Correlation_Betwwen_Prev_Betweenness_and_New_Authors_Degree, color = 'Betweenness Centrality')) + geom_line(aes(DC1$Start_Year,DC1$Correlation_Betwwen_Prev_Degree_and_New_Authors_Degree, color = 'Degree Centrality')) + geom_line(aes(CC1$Start_Year,CC1$Correlation_Betwwen_Prev_Closeness_and_New_Authors_Degree, color = 'Closeness Centrality')) + geom_line(aes(BC1$Start_Year,BC1$Correlation_Betwwen_Prev_Betweenness_and_New_Authors_Degree, color = 'Betweenness Centrality')) + opts(legend.title=theme_blank()) + coord_cartesian(ylim=c(-0.5, 1.0))
ggsave(pdffile)

pdffile <-c("/Users/Kallol/Testing/Graphs/PA_Field1_ComparisonForNewLinkWithOldAuthorsAttachment.pdf")
pdf(pdffile)
p + xlab('Year') + ylab('Correlation with Number of New Links with Old Authors') + geom_point(aes(DC1$Start_Year,DC1$Correlation_Betwwen_Prev_Degree_and_New_Old_Degree, color = 'Degree Centrality')) + geom_point(aes(CC1$Start_Year,CC1$Correlation_Betwwen_Prev_Closeness_and_New_Old_Degree, color = 'Closeness Centrality')) + geom_point(aes(BC1$Start_Year,BC1$Correlation_Betwwen_Prev_Betweenness_and_New_Old_Degree, color = 'Betweenness Centrality')) + geom_line(aes(DC1$Start_Year,DC1$Correlation_Betwwen_Prev_Degree_and_New_Old_Degree, color = 'Degree Centrality')) + geom_line(aes(CC1$Start_Year,CC1$Correlation_Betwwen_Prev_Closeness_and_New_Old_Degree, color = 'Closeness Centrality')) + geom_line(aes(BC1$Start_Year,BC1$Correlation_Betwwen_Prev_Betweenness_and_New_Old_Degree, color = 'Betweenness Centrality')) + opts(legend.title=theme_blank()) + coord_cartesian(ylim=c(-0.5, 1.0))
ggsave(pdffile)

AB<-read.table("/Users/Kallol/Testing/AbbasiTable2.txt", header = TRUE, sep= ";")
AB1<-read.table("/Users/Kallol/Testing/abbasi/field1run1discrete1991-2010_1years-AbbasiTable2.csv", header=TRUE, sep = ';')
AB2<-read.table("/Users/Kallol/Testing/abbasi/field2run1discrete1991-2010_1years-AbbasiTable2.csv", header=TRUE, sep = ';')

p<-ggplot(AB1)
pdffile <-c("/Users/Kallol/Testing/Graphs/ComparisonCumulativeAuthors.pdf")
pdf(pdffile)
p + xlab('Year') + ylab('Cumulative Authors') + geom_point(aes(AB1$Start_Year,AB1$Cumulative_No_of_Authors, color = 'Field1')) + geom_point(aes(AB2$Start_Year,AB2$Cumulative_No_of_Authors, color = 'Field2')) + geom_point(aes(AB$Start_Year,AB$Cumulative_No_of_Authors, color = 'Abbasi'))+ geom_line(aes(AB1$Start_Year,AB1$Cumulative_No_of_Authors, color = 'Field1')) + geom_line(aes(AB2$Start_Year,AB2$Cumulative_No_of_Authors, color = 'Field2')) + geom_line(aes(AB$Start_Year,AB$Cumulative_No_of_Authors, color = 'Abbasi'))+ opts(legend.title=theme_blank())
ggsave(pdffile)


p<-ggplot(AB1)
pdffile <-c("/Users/Kallol/Testing/Graphs/ComparisonNewAuthors.pdf")
pdf(pdffile)
p + xlab('Year') + ylab('New Authors') + geom_point(aes(AB1$Start_Year,AB1$No_of_New_Authors, color = 'Field1')) + geom_point(aes(AB2$Start_Year,AB2$No_of_New_Authors, color = 'Field2')) + geom_point(aes(AB$Start_Year,AB$No_of_New_Authors, color = 'Abbasi')) +geom_line(aes(AB1$Start_Year,AB1$No_of_New_Authors, color = 'Field1')) + geom_line(aes(AB2$Start_Year,AB2$No_of_New_Authors, color = 'Field2')) + geom_line(aes(AB$Start_Year,AB$No_of_New_Authors, color = 'Abbasi')) + opts(legend.title=theme_blank())
ggsave(pdffile)

p<-ggplot(AB1)
pdffile <-c("/Users/Kallol/Testing/Graphs/ComparisonNewAuthorsCoonectedToNew.pdf")
pdf(pdffile)
p + xlab('Year') + ylab('% of New Authors Connected to At Least One New Author') + geom_point(aes(AB1$Start_Year,AB1$Percent_Of_New_Authors_Connected_to_atleast_one_new_author, color = 'Field1')) + geom_point(aes(AB2$Start_Year,AB2$Percent_Of_New_Authors_Connected_to_atleast_one_new_author, color = 'Field2')) + geom_point(aes(AB$Start_Year,AB$Percent_Of_New_Authors_Connected_to_atleast_one_new_author, color = 'Abbasi')) + geom_line(aes(AB1$Start_Year,AB1$Percent_Of_New_Authors_Connected_to_atleast_one_new_author, color = 'Field1')) + geom_line(aes(AB2$Start_Year,AB2$Percent_Of_New_Authors_Connected_to_atleast_one_new_author, color = 'Field2')) + geom_line(aes(AB$Start_Year,AB$Percent_Of_New_Authors_Connected_to_atleast_one_new_author, color = 'Abbasi')) + opts(legend.title=theme_blank())
ggsave(pdffile)

p<-ggplot(AB1)
pdffile <-c("/Users/Kallol/Testing/Graphs/ComparisonNewAuthorsCoonectedToOld.pdf")
pdf(pdffile)
p + xlab('Year') + ylab('% of New Authors Connected to At Least One Old Author') + geom_point(aes(AB1$Start_Year,AB1$Percent_Of_New_Authors_Connected_to_atleast_one_old_author, color = 'Field1')) + geom_point(aes(AB2$Start_Year,AB2$Percent_Of_New_Authors_Connected_to_atleast_one_old_author, color = 'Field2')) + geom_point(aes(AB$Start_Year,AB$Percent_Of_New_Authors_Connected_to_atleast_one_old_author, color = 'Abbasi')) +geom_line(aes(AB1$Start_Year,AB1$Percent_Of_New_Authors_Connected_to_atleast_one_old_author, color = 'Field1')) + geom_line(aes(AB2$Start_Year,AB2$Percent_Of_New_Authors_Connected_to_atleast_one_old_author, color = 'Field2')) + geom_line(aes(AB$Start_Year,AB$Percent_Of_New_Authors_Connected_to_atleast_one_old_author, color = 'Abbasi')) + opts(legend.title=theme_blank())
ggsave(pdffile)

p<-ggplot(AB1)
pdffile <-c("/Users/Kallol/Testing/Graphs/ComparisonOldAuthorsCoonectedToNew.pdf")
pdf(pdffile)
p + xlab('Year') + ylab('Percent of Old Authors Connected to At Least One Old Author') + geom_point(aes(AB1$Start_Year,AB1$Percent_Of_Old_Authors_Connected_to_atleast_one_new_author, color = 'Field1')) + geom_point(aes(AB2$Start_Year,AB2$Percent_Of_Old_Authors_Connected_to_atleast_one_new_author, color = 'Field2')) + geom_point(aes(AB$Start_Year,AB$Percent_Of_Old_Authors_Connected_to_atleast_one_new_author, color = 'Abbasi')) + geom_line(aes(AB1$Start_Year,AB1$Percent_Of_Old_Authors_Connected_to_atleast_one_new_author, color = 'Field1')) + geom_line(aes(AB2$Start_Year,AB2$Percent_Of_Old_Authors_Connected_to_atleast_one_new_author, color = 'Field2')) + geom_line(aes(AB$Start_Year,AB$Percent_Of_Old_Authors_Connected_to_atleast_one_new_author, color = 'Abbasi')) + opts(legend.title=theme_blank())
ggsave(pdffile)

p<-ggplot(AB1)
pdffile <-c("/Users/Kallol/Testing/Graphs/ComparisonOldAuthorsCoonectedToOld.pdf")
pdf(pdffile)
p + xlab('Year') + ylab('Percent of Old Authors Connected to At Least One Old Author') + geom_point(aes(AB1$Start_Year,AB1$Percent_Of_Old_Authors_Connected_to_atleast_one_old_author, color = 'Field1')) + geom_point(aes(AB2$Start_Year,AB2$Percent_Of_Old_Authors_Connected_to_atleast_one_old_author, color = 'Field2')) + geom_point(aes(AB$Start_Year,AB$Percent_Of_Old_Authors_Connected_to_atleast_one_old_author, color = 'Abbasi')) + geom_line(aes(AB1$Start_Year,AB1$Percent_Of_Old_Authors_Connected_to_atleast_one_old_author, color = 'Field1')) + geom_line(aes(AB2$Start_Year,AB2$Percent_Of_Old_Authors_Connected_to_atleast_one_old_author, color = 'Field2')) + geom_line(aes(AB$Start_Year,AB$Percent_Of_Old_Authors_Connected_to_atleast_one_old_author, color = 'Abbasi')) + opts(legend.title=theme_blank())
ggsave(pdffile)

p<-ggplot(AB1)
pdffile <-c("/Users/Kallol/Testing/Graphs/ComparisonOldAuthorsCoonectedToAny.pdf")
pdf(pdffile)
p + xlab('Year') + ylab('Percent of Old Authors Connected to Any Author') + geom_point(aes(AB1$Start_Year,AB1$Percent_Of_Old_Authors_Connected_to_atleast_one_any_author, color = 'Field1')) + geom_point(aes(AB2$Start_Year,AB2$Percent_Of_Old_Authors_Connected_to_atleast_one_any_author, color = 'Field2')) + geom_point(aes(AB$Start_Year,AB$Percent_Of_Old_Authors_Connected_to_atleast_one_any_author, color = 'Abbasi')) + geom_line(aes(AB1$Start_Year,AB1$Percent_Of_Old_Authors_Connected_to_atleast_one_any_author, color = 'Field1')) + geom_line(aes(AB2$Start_Year,AB2$Percent_Of_Old_Authors_Connected_to_atleast_one_any_author, color = 'Field2')) + geom_line(aes(AB$Start_Year,AB$Percent_Of_Old_Authors_Connected_to_atleast_one_any_author, color = 'Abbasi')) + opts(legend.title=theme_blank())
ggsave(pdffile)

ABT<-read.table("/Users/Kallol/Testing/Abbasitable3.txt", header=TRUE, sep = ';')
ABT1<-read.table("/Users/Kallol/Testing/abbasi/field1run1discrete1991-2010_1years-AbbasiTable3.csv", header=TRUE, sep = ';')
ABT2<-read.table("/Users/Kallol/Testing/abbasi/field2run1discrete1991-2010_1years-AbbasiTable3.csv", header=TRUE, sep = ';')

p<-ggplot(ABT2)
pdffile <-c("/Users/Kallol/Testing/Graphs/ComparisonCumulativeLinks.pdf")
pdf(pdffile)
p + xlab('Year') + ylab('Cumulative Links') + geom_point(aes(ABT1$Start_Year,ABT1$Cumulative_Number_of_Links, color = 'Field1')) + geom_point(aes(ABT2$Start_Year,ABT2$Cumulative_Number_of_Links, color = 'Field2')) + geom_point(aes(ABT$Start_Year,ABT$Cumulative_Number_of_Links, color = 'Abbasi')) + geom_line(aes(ABT1$Start_Year,ABT1$Cumulative_Number_of_Links, color = 'Field1')) + geom_line(aes(ABT2$Start_Year,ABT2$Cumulative_Number_of_Links, color = 'Field2')) + geom_line(aes(ABT$Start_Year,ABT$Cumulative_Number_of_Links, color = 'Abbasi')) + opts(legend.title=theme_blank())
ggsave(pdffile)

p<-ggplot(ABT2)
pdffile <-c("/Users/Kallol/Testing/Graphs/ComparisonNewLinks.pdf")
pdf(pdffile)
p + xlab('Year') + ylab('New Links') + geom_point(aes(ABT1$Start_Year,ABT1$Number_of_New_Links, color = 'Field1')) + geom_point(aes(ABT2$Start_Year,ABT2$Number_of_New_Links, color = 'Field2')) + geom_point(aes(ABT$Start_Year,ABT$Number_of_New_Links, color = 'Abbasi')) + geom_line(aes(ABT1$Start_Year,ABT1$Number_of_New_Links, color = 'Field1')) + geom_line(aes(ABT2$Start_Year,ABT2$Number_of_New_Links, color = 'Field2')) + geom_line(aes(ABT$Start_Year,ABT$Number_of_New_Links, color = 'Abbasi')) + opts(legend.title=theme_blank())
ggsave(pdffile)


p<-ggplot(ABT2)
pdffile <-c("/Users/Kallol/Testing/Graphs/ComparisonNewtoNewLinks.pdf")
pdf(pdffile)
p + xlab('Year') + ylab('Percent of New to New Links') + geom_point(aes(ABT1$Start_Year,ABT1$Percent_of_New_Links_Among_New_Authors, color = 'Field1')) + geom_point(aes(ABT2$Start_Year,ABT2$Percent_of_New_Links_Among_New_Authors, color = 'Field2')) + geom_point(aes(ABT$Start_Year,ABT$Percent_of_New_Links_Among_New_Authors, color = 'Abbasi')) + geom_line(aes(ABT1$Start_Year,ABT1$Percent_of_New_Links_Among_New_Authors, color = 'Field1')) + geom_line(aes(ABT2$Start_Year,ABT2$Percent_of_New_Links_Among_New_Authors, color = 'Field2')) + geom_line(aes(ABT$Start_Year,ABT$Percent_of_New_Links_Among_New_Authors, color = 'Abbasi')) + opts(legend.title=theme_blank())
ggsave(pdffile)

p<-ggplot(ABT2)
pdffile <-c("/Users/Kallol/Testing/Graphs/ComparisonOldtoNewLinks.pdf")
pdf(pdffile)
p + xlab('Year') + ylab('Percent of Old to Old First Time  Links') + geom_point(aes(ABT1$Start_Year,ABT1$Percent_Of_Links_Between_New_and_Old, color = 'Field1')) + geom_point(aes(ABT2$Start_Year,ABT2$Percent_Of_Links_Between_New_and_Old, color = 'Field2')) + geom_point(aes(ABT$Start_Year,ABT$Percent_Of_Links_Between_New_and_Old, color = 'Abbasi')) + geom_line(aes(ABT1$Start_Year,ABT1$Percent_Of_Links_Between_New_and_Old, color = 'Field1')) + geom_line(aes(ABT2$Start_Year,ABT2$Percent_Of_Links_Between_New_and_Old, color = 'Field2')) + geom_line(aes(ABT$Start_Year,ABT$Percent_Of_Links_Between_New_and_Old, color = 'Abbasi')) + opts(legend.title=theme_blank())
ggsave(pdffile)

p<-ggplot(ABT2)
pdffile <-c("/Users/Kallol/Testing/Graphs/ComparisonOldtoOldFirstTimeLinks.pdf")
pdf(pdffile)
p + xlab('Year') + ylab('Percent of Old to Old First Time  Links') + geom_point(aes(ABT1$Start_Year,ABT1$Percent_of_New_Links_Between_Two_Old_Authors_Not_Connected_Before, color = 'Field1')) + geom_point(aes(ABT2$Start_Year,ABT2$Percent_of_New_Links_Between_Two_Old_Authors_Not_Connected_Before, color = 'Field2')) + geom_point(aes(ABT$Start_Year,ABT$Percent_of_New_Links_Between_Two_Old_Authors_Not_Connected_Before, color = 'Abbasi')) + geom_line(aes(ABT1$Start_Year,ABT1$Percent_of_New_Links_Between_Two_Old_Authors_Not_Connected_Before, color = 'Field1')) + geom_line(aes(ABT2$Start_Year,ABT2$Percent_of_New_Links_Between_Two_Old_Authors_Not_Connected_Before, color = 'Field2')) + geom_line(aes(ABT$Start_Year,ABT$Percent_of_New_Links_Between_Two_Old_Authors_Not_Connected_Before, color = 'Abbasi')) + opts(legend.title=theme_blank())
ggsave(pdffile)

p<-ggplot(ABT2)
pdffile <-c("/Users/Kallol/Testing/Graphs/ComparisonOldtoOldRepeatingNewLinks.pdf")
pdf(pdffile)
p + xlab('Year') + ylab('Percent of Old to Old Repeating Links') + geom_point(aes(ABT1$Start_Year,ABT1$Percent_of_Links_Among_Old_Authors_Connected_Before, color = 'Field1')) + geom_point(aes(ABT2$Start_Year,ABT2$Percent_of_Links_Among_Old_Authors_Connected_Before, color = 'Field2')) + geom_point(aes(ABT$Start_Year,ABT$Percent_of_Links_Among_Old_Authors_Connected_Before, color = 'Abbasi')) + geom_line(aes(ABT1$Start_Year,ABT1$Percent_of_Links_Among_Old_Authors_Connected_Before, color = 'Field1')) + geom_line(aes(ABT2$Start_Year,ABT2$Percent_of_Links_Among_Old_Authors_Connected_Before, color = 'Field2')) + geom_line(aes(ABT$Start_Year,ABT$Percent_of_Links_Among_Old_Authors_Connected_Before, color = 'Abbasi')) + opts(legend.title=theme_blank())
ggsave(pdffile)


p<-ggplot(ABT1)
pdffile <-c("/Users/Kallol/Testing/Graphs/Field1NewLinks.pdf")
pdf(pdffile)
p + xlab('Year') + ylab('Percent New Links') + geom_point(aes(ABT1$Start_Year,ABT1$Percent_of_New_Links_Among_New_Authors, color = 'New-New')) + geom_point(aes(ABT1$Start_Year,ABT1$Percent_Of_Links_Between_New_and_Old, color = 'New-Old')) + geom_point(aes(ABT1$Start_Year,ABT1$Percent_of_New_Links_Between_Two_Old_Authors_Not_Connected_Before, color = 'Old-Old-1st')) + geom_point(aes(ABT1$Start_Year,ABT1$Percent_of_Links_Among_Old_Authors_Connected_Before, color = 'Old-Old-Again')) + geom_line(aes(ABT1$Start_Year,ABT1$Percent_of_New_Links_Among_New_Authors, color = 'New-New')) + geom_line(aes(ABT1$Start_Year,ABT1$Percent_Of_Links_Between_New_and_Old, color = 'New-Old')) + geom_line(aes(ABT1$Start_Year,ABT1$Percent_of_New_Links_Between_Two_Old_Authors_Not_Connected_Before, color = 'Old-Old-1st')) + geom_line(aes(ABT1$Start_Year,ABT1$Percent_of_Links_Among_Old_Authors_Connected_Before, color = 'Old-Old-Again')) + opts(legend.title=theme_blank())
ggsave(pdffile)

p<-ggplot(ABT2)
pdffile <-c("/Users/Kallol/Testing/Graphs/Field2NewLinks.pdf")
pdf(pdffile)
p + xlab('Year') + ylab('Percent of New Links') + geom_point(aes(ABT2$Start_Year,ABT2$Percent_of_New_Links_Among_New_Authors, color = 'New-New')) + geom_point(aes(ABT2$Start_Year,ABT2$Percent_Of_Links_Between_New_and_Old, color = 'New-Old')) + geom_point(aes(ABT2$Start_Year,ABT2$Percent_of_New_Links_Between_Two_Old_Authors_Not_Connected_Before, color = 'Old-Old-1st')) + geom_point(aes(ABT2$Start_Year,ABT2$Percent_of_Links_Among_Old_Authors_Connected_Before, color = 'Old-Old-Again')) + geom_line(aes(ABT2$Start_Year,ABT2$Percent_of_New_Links_Among_New_Authors, color = 'New-New')) + geom_line(aes(ABT2$Start_Year,ABT2$Percent_Of_Links_Between_New_and_Old, color = 'New-Old')) + geom_line(aes(ABT2$Start_Year,ABT2$Percent_of_New_Links_Between_Two_Old_Authors_Not_Connected_Before, color = 'Old-Old-1st')) + geom_line(aes(ABT2$Start_Year,ABT2$Percent_of_Links_Among_Old_Authors_Connected_Before, color = 'Old-Old-Again')) + opts(legend.title=theme_blank())
ggsave(pdffile)

p<-ggplot(ABT2)
pdffile <-c("/Users/Kallol/Testing/Graphs/AbbasiNewLinks.pdf")
pdf(pdffile)
p + xlab('Year') + ylab('Percent of New Links') + geom_point(aes(ABT$Start_Year,ABT$Percent_of_New_Links_Among_New_Authors, color = 'New-New')) + geom_point(aes(ABT$Start_Year,ABT$Percent_Of_Links_Between_New_and_Old, color = 'New-Old')) + geom_point(aes(ABT$Start_Year,ABT$Percent_of_New_Links_Between_Two_Old_Authors_Not_Connected_Before, color = 'Old-Old-1st')) + geom_point(aes(ABT$Start_Year,ABT$Percent_of_Links_Among_Old_Authors_Connected_Before, color = 'Old-Old-Again')) + geom_line(aes(ABT$Start_Year,ABT$Percent_of_New_Links_Among_New_Authors, color = 'New-New')) + geom_line(aes(ABT$Start_Year,ABT$Percent_Of_Links_Between_New_and_Old, color = 'New-Old')) + geom_line(aes(ABT$Start_Year,ABT$Percent_of_New_Links_Between_Two_Old_Authors_Not_Connected_Before, color = 'Old-Old-1st')) + geom_line(aes(ABT$Start_Year,ABT$Percent_of_Links_Among_Old_Authors_Connected_Before, color = 'Old-Old-Again')) + opts(legend.title=theme_blank())
ggsave(pdffile)


