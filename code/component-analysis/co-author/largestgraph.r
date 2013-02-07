library(ggplot2)
library(scales)




AB1<- read.table('/Users/macbookadministrator/Academic/Research/Network/Output/nwa-field1/runs/run1norm-dis-hfree-red/output/networks/discrete1991-2010_1years/generic/field1run1norm-dis-hfree-red_discrete1991-2010_1years_LargestGrowth.csv', header = TRUE, sep =';')
AB2<- read.table('/Users/macbookadministrator/Academic/Research/Network/Output/nwa-field1/runs/run1norm-dis-hfree-red/output/networks/discrete1991-2010_2years/generic/field1run1norm-dis-hfree-red_discrete1991-2010_2years_LargestGrowth.csv', header = TRUE, sep =';')
AB3<- read.table('/Users/macbookadministrator/Academic/Research/Network/Output/nwa-field1/runs/run1norm-dis-hfree-red/output/networks/discrete1991-2010_3years/generic/field1run1norm-dis-hfree-red_discrete1991-2010_3years_LargestGrowth.csv', header = TRUE, sep =';')
AB4<- read.table('/Users/macbookadministrator/Academic/Research/Network/Output/nwa-field1/runs/run1norm-dis-hfree-red/output/networks/discrete1991-2010_4years/generic/field1run1norm-dis-hfree-red_discrete1991-2010_4years_LargestGrowth.csv', header = TRUE, sep =';')
AB5<- read.table('/Users/macbookadministrator/Academic/Research/Network/Output/nwa-field1/runs/run1norm-dis-hfree-red/output/networks/discrete1991-2010_5years/generic/field1run1norm-dis-hfree-red_discrete1991-2010_5years_LargestGrowth.csv', header = TRUE, sep =';')
AB6<- read.table('/Users/macbookadministrator/Academic/Research/Network/Output/nwa-field1/runs/run1norm-dis-hfree-red/output/networks/discrete1991-2010_6years/generic/field1run1norm-dis-hfree-red_discrete1991-2010_6years_LargestGrowth.csv', header = TRUE, sep =';')
AB7<- read.table('/Users/macbookadministrator/Academic/Research/Network/Output/nwa-field1/runs/run1norm-dis-hfree-red/output/networks/discrete1991-2010_7years/generic/field1run1norm-dis-hfree-red_discrete1991-2010_7years_LargestGrowth.csv', header = TRUE, sep =';')
AB8<- read.table('/Users/macbookadministrator/Academic/Research/Network/Output/nwa-field1/runs/run1norm-dis-hfree-red/output/networks/discrete1991-2010_8years/generic/field1run1norm-dis-hfree-red_discrete1991-2010_8years_LargestGrowth.csv', header = TRUE, sep =';')
AB9<- read.table('/Users/macbookadministrator/Academic/Research/Network/Output/nwa-field1/runs/run1norm-dis-hfree-red/output/networks/discrete1991-2010_9years/generic/field1run1norm-dis-hfree-red_discrete1991-2010_9years_LargestGrowth.csv', header = TRUE, sep =';')


p1<-ggplot(AB1)
pdffile <-c('/Users/macbookadministrator/Academic/Research/Network/Output/nwa-field1/runs/run1norm-dis-hfree-red/output/statistics/discrete1991-2010_1years/generic/allyears/components/images/field1run1norm-dis-hfree-red_discrete1991-2010_1years_LargestGraph.pdf')
pdf(pdffile)
p1 + xlab('Year') + ylab('Percent') + geom_point(aes(AB1$End_Year,AB1$Percent, color = '1')) + geom_line(aes(AB1$End_Year,AB1$Percent, color = '1')) + opts(legend.title=theme_blank()) + scale_y_continuous(limits = c(0, 100))
ggsave(pdffile)



p2<-ggplot(AB2)
pdffile <-c('/Users/macbookadministrator/Academic/Research/Network/Output/nwa-field1/runs/run1norm-dis-hfree-red/output/statistics/discrete1991-2010_2years/generic/allyears/components/images/field1run1norm-dis-hfree-red_discrete1991-2010_2years_LargestGraph.pdf')
pdf(pdffile)
p2 + xlab('Year') + ylab('Percent') + geom_point(aes(AB2$End_Year,AB2$Percent, color = '2')) + geom_line(aes(AB2$End_Year,AB2$Percent, color = '2')) + opts(legend.title=theme_blank()) + scale_y_continuous(limits = c(0, 100))
ggsave(pdffile)



p3<-ggplot(AB3)
pdffile <-c('/Users/macbookadministrator/Academic/Research/Network/Output/nwa-field1/runs/run1norm-dis-hfree-red/output/statistics/discrete1991-2010_3years/generic/allyears/components/images/field1run1norm-dis-hfree-red_discrete1991-2010_3years_LargestGraph.pdf')
pdf(pdffile)
p3 + xlab('Year') + ylab('Percent') + geom_point(aes(AB3$End_Year,AB3$Percent, color = '3')) + geom_line(aes(AB3$End_Year,AB3$Percent, color = '3')) + opts(legend.title=theme_blank()) + scale_y_continuous(limits = c(0, 100))
ggsave(pdffile)



p4<-ggplot(AB4)
pdffile <-c('/Users/macbookadministrator/Academic/Research/Network/Output/nwa-field1/runs/run1norm-dis-hfree-red/output/statistics/discrete1991-2010_4years/generic/allyears/components/images/field1run1norm-dis-hfree-red_discrete1991-2010_4years_LargestGraph.pdf')
pdf(pdffile)
p4 + xlab('Year') + ylab('Percent') + geom_point(aes(AB4$End_Year,AB4$Percent, color = '4')) + geom_line(aes(AB4$End_Year,AB4$Percent, color = '4')) + opts(legend.title=theme_blank()) + scale_y_continuous(limits = c(0, 100))
ggsave(pdffile)



p5<-ggplot(AB5)
pdffile <-c('/Users/macbookadministrator/Academic/Research/Network/Output/nwa-field1/runs/run1norm-dis-hfree-red/output/statistics/discrete1991-2010_5years/generic/allyears/components/images/field1run1norm-dis-hfree-red_discrete1991-2010_5years_LargestGraph.pdf')
pdf(pdffile)
p5 + xlab('Year') + ylab('Percent') + geom_point(aes(AB5$End_Year,AB5$Percent, color = '5')) + geom_line(aes(AB5$End_Year,AB5$Percent, color = '5')) + opts(legend.title=theme_blank()) + scale_y_continuous(limits = c(0, 100))
ggsave(pdffile)



p6<-ggplot(AB6)
pdffile <-c('/Users/macbookadministrator/Academic/Research/Network/Output/nwa-field1/runs/run1norm-dis-hfree-red/output/statistics/discrete1991-2010_6years/generic/allyears/components/images/field1run1norm-dis-hfree-red_discrete1991-2010_6years_LargestGraph.pdf')
pdf(pdffile)
p6 + xlab('Year') + ylab('Percent') + geom_point(aes(AB6$End_Year,AB6$Percent, color = '6')) + geom_line(aes(AB6$End_Year,AB6$Percent, color = '6')) + opts(legend.title=theme_blank()) + scale_y_continuous(limits = c(0, 100))
ggsave(pdffile)



p7<-ggplot(AB7)
pdffile <-c('/Users/macbookadministrator/Academic/Research/Network/Output/nwa-field1/runs/run1norm-dis-hfree-red/output/statistics/discrete1991-2010_7years/generic/allyears/components/images/field1run1norm-dis-hfree-red_discrete1991-2010_7years_LargestGraph.pdf')
pdf(pdffile)
p7 + xlab('Year') + ylab('Percent') + geom_point(aes(AB7$End_Year,AB7$Percent, color = '7')) + geom_line(aes(AB7$End_Year,AB7$Percent, color = '7')) + opts(legend.title=theme_blank()) + scale_y_continuous(limits = c(0, 100))
ggsave(pdffile)



p8<-ggplot(AB8)
pdffile <-c('/Users/macbookadministrator/Academic/Research/Network/Output/nwa-field1/runs/run1norm-dis-hfree-red/output/statistics/discrete1991-2010_8years/generic/allyears/components/images/field1run1norm-dis-hfree-red_discrete1991-2010_8years_LargestGraph.pdf')
pdf(pdffile)
p8 + xlab('Year') + ylab('Percent') + geom_point(aes(AB8$End_Year,AB8$Percent, color = '8')) + geom_line(aes(AB8$End_Year,AB8$Percent, color = '8')) + opts(legend.title=theme_blank()) + scale_y_continuous(limits = c(0, 100))
ggsave(pdffile)



p9<-ggplot(AB9)
pdffile <-c('/Users/macbookadministrator/Academic/Research/Network/Output/nwa-field1/runs/run1norm-dis-hfree-red/output/statistics/discrete1991-2010_9years/generic/allyears/components/images/field1run1norm-dis-hfree-red_discrete1991-2010_9years_LargestGraph.pdf')
pdf(pdffile)
p9 + xlab('Year') + ylab('Percent') + geom_point(aes(AB9$End_Year,AB9$Percent, color = '9')) + geom_line(aes(AB9$End_Year,AB9$Percent, color = '9')) + opts(legend.title=theme_blank()) + scale_y_continuous(limits = c(0, 100))
ggsave(pdffile)

