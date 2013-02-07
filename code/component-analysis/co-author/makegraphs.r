library(ggplot2)
library(scales)






#Largest Component starts
M<- read.table('/Users/macbookadministrator/Academic/Research/Network/Output/nwa-field2/runs/run1norm-dis-hfree-red/output/statistics/accumulative1991-2010_1years/generic/allyears/components/tables/field2run1norm-dis-hfree-red_accumulative1991-2010_1years_Large-SecondLargeData.csv', header = TRUE, sep =';')
p<-ggplot(M)
pdffile <-c('/Users/macbookadministrator/Academic/Research/Network/Output/nwa-field2/runs/run1norm-dis-hfree-red/output/statistics/accumulative1991-2010_1years/generic/allyears/components/images/field2run1norm-dis-hfree-red_accumulative1991-2010_1years_LargestComponent.pdf')
pdf(pdffile)
p + xlab('Year') + ylab('% of authors newly joining largest component') + geom_point(aes(M$End_year, M$Ever_Second_Percent, shape = 'Second Ever')) + geom_line(aes(M$End_year, M$Ever_Second_Percent, shape = 'Second Ever')) + geom_point(aes(M$End_year, M$Just_Previous_Percent, shape = 'Previous Second')) + geom_line(aes(M$End_year, M$Just_Previous_Percent, shape = 'Previous Second'))+ geom_point(aes(M$End_year, M$Percent_from_others, shape = 'From Other Components')) + geom_line(aes(M$End_year, M$Percent_from_others, shape = 'From Other Components')) + geom_point(aes(M$End_year, M$Percent_Previous_Largest,  shape = 'From Previous Largest')) + geom_line(aes(M$End_year, M$Percent_Previous_Largest,  shape = 'From Previous Largest')) + geom_point(aes(M$End_year, M$Percent_New,   shape = 'From New')) + geom_line(aes(M$End_year, M$Percent_New,  shape = 'From New'))+ scale_shape_manual(values=c(2,4,16,7,15,5)) 
ggsave(pdffile)

#Largest Component ends




#Largest Component 2 starts
p<-ggplot(M)
pdffile <-c('/Users/macbookadministrator/Academic/Research/Network/Output/nwa-field2/runs/run1norm-dis-hfree-red/output/statistics/accumulative1991-2010_1years/generic/allyears/components/images/field2run1norm-dis-hfree-red_accumulative1991-2010_1years_LargestComponent2.pdf')
pdf(pdffile)
p + xlab('Year') + ylab('% of authors newly joining largest component') + geom_point(aes(M$End_year, (M$Number_from_Just_Previous_Second/(M$Number_from_Just_Previous_Second + M$Number_from_Others + M$New))*100.00,  shape = '2nd component'))+ geom_line(aes(M$End_year, (M$Number_from_Just_Previous_Second/(M$Number_from_Just_Previous_Second + M$Number_from_Others + M$New))*100.00))+ geom_point(aes(M$End_year, (M$Number_from_Others/(M$Number_from_Just_Previous_Second + M$Number_from_Others + M$New))*100.00,  shape = 'other component')) + geom_line(aes(M$End_year, (M$Number_from_Others/(M$Number_from_Just_Previous_Second + M$Number_from_Others + M$New))*100.00)) + geom_point(aes(M$End_year, (M$New/(M$Number_from_Just_Previous_Second + M$Number_from_Others + M$New))*100.00,  shape = 'new author')) + geom_line(aes(M$End_year, (M$New/(M$Number_from_Just_Previous_Second + M$Number_from_Others + M$New))*100.00)) + scale_shape_manual(nam = 'Source', values=c(2,4,16,7,15,5)) + coord_cartesian(ylim=c(0, 100)) + 
ggsave(pdffile)

#Largest Component 2 ends


