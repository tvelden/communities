filesource="/Users/shiyansiadmin/Dropbox/Files/Results/Annual/Inherit/"
for (source in 1:12) {
	pdf(paste(filesource,'plot from Cluster',toString(source),'.pdf',sep=""))
	max_y =0 
	x = matrix(nrow=14,ncol=18)
	labels = c()
	colors = c()
	for (i in 1:12) { 
		if (i != source) {
			x[i, ] = scan(paste(filesource,"AuthorPortionYear3 From Cluster",toString(source)," To Cluster",toString(i),sep=""))
			max_y =max(max_y,x[i,])
			labels[i] = paste("Clu", toString(source), "--Clu",toString(i),sep="")
			if (i<=7) {
			    colors[i] = rgb(i/7,0,0)
			} else {
				if (i<=10) {
					colors[i] = rgb(0,(i-7)/4,0)
				} else {
					colors[i] = rgb(0,0,(i-10)/3)
				}
			}
		}
	}
	year = c(1992:2009)
	if (source==1) {
		plot (x[2,]~year, xlab="year" , ylab="portion of authors", type = "o" , col = colors[2] , pch=2, lty=2,ylim=c(0,max_y))
	} else {
		plot (x[1,]~year, xlab="year" , ylab="portion of authors", type = "o" , col = colors[1] , pch=1, lty=2,ylim=c(0,max_y))
	}
	for (i in 1:12) {
		if (i!=source) {
			if ((source==1) && (i!=2)) {
				lines(x[i,]~year, type="o", col = colors[i], pch=i, lty=2)
			}
			if ((source!=1) && (i!=1)) {
				lines(x[i,]~year, type="o", col = colors[i], pch=i, lty=2)
			}
		}
	}
	legend("topright", legend=labels[1:12], col=colors[1:12], pch=1:12,lty=2,cex=0.5)
	title(main=paste("Source = Cluster",toString(source),sep=""))
	dev.off()
}