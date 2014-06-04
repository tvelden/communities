filesource="/Users/shiyansiadmin/Dropbox/Files/Results/Annual/Inherit/"
for (target in 1:12) {
	pdf(paste(filesource,'plot to Cluster',toString(target),'.pdf',sep=""))
	max_y =0 
	x = matrix(nrow=14,ncol=18)
	labels = c()
	colors = c()
	for (i in 1:12) { 
		if (i != target) {
			x[i, ] = scan(paste(filesource,"AuthorPortionYear3 From Cluster",toString(i)," To Cluster",toString(target),sep=""))
			max_y =max(max_y,x[i,])
			labels[i] = paste("Clu", toString(i), "--Clu",toString(target),sep="")
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
	if (target==1) {
		plot (x[2,]~year, xlab="year" , ylab="portion of authors", type = "o" , col = colors[2] , pch=2, lty=2,ylim=c(0,max_y))
	} else {
		plot (x[1,]~year, xlab="year" , ylab="portion of authors", type = "o" , col = colors[1] , pch=1, lty=2,ylim=c(0,max_y))
	}
	for (i in 1:12) {
		if (i!=target) {
			if ((target==1) && (i!=2)) {
				lines(x[i,]~year, type="o", col = colors[i], pch=i, lty=2)
			}
			if ((target!=1) && (i!=1)) {
				lines(x[i,]~year, type="o", col = colors[i], pch=i, lty=2)
			}
		}
	}
	legend("topright", legend=labels[1:12], col=colors[1:12], pch=1:12,lty=2,cex=0.5)
	title(main=paste("Target = Cluster",toString(target),sep=""))
	dev.off()
}