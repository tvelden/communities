#draw the variation of number of authors for all the clusters
filesource="/Users/shiyansiadmin/Dropbox/Files/Results/Annual/"
pdf(paste(filesource,"NumberOfAuthors.pdf",sep=""))
par(mfrow=c(2,3))
for (i in 1:6) {
	tab=read.table(paste(filesource,"NumberOfAuthorsOfCluster",toString(i),sep=""),header=TRUE)
	plot(tab,ylim=c(0,2000),type="o")
	title(main=paste("Cluster",toString(i),sep=""))
}
par(mfrow=c(2,3))
for (i in 7:12) {
	tab=read.table(paste(filesource,"NumberOfAuthorsOfCluster",toString(i),sep=""),header=TRUE)
	plot(tab,ylim=c(0,2000),type="o")
	title(main=paste("Cluster",toString(i),sep=""))
}
dev.off()