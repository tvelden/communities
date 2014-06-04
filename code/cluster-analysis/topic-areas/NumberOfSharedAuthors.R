#Portion of shared authors through years
filesource="/Users/shiyansiadmin/Dropbox/Files/Results/Annual/"
library(ggplot2)
for (i in 1:12) {
	#pdf(paste(filesource,'PortionOfSharedAuthorsInCluster',toString(i),'.pdf',sep=""))
	tab=read.table(paste(filesource,"InstancesOfCluster",toString(i),sep=""),header=TRUE)
	ggplot(tab,aes(x=Year, y=NoOfAuthors, fill=Label))+geom_area()
	ggsave(paste(filesource,'NumberOfSharedAuthorsInCluster',toString(i),'.pdf',sep=""))
	#dev.off()
}