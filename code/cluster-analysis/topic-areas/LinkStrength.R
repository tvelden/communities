#LinkStrength Explanation
ta = read.table("/Users/shiyansiadmin/Dropbox/Files/NewField2Data2/affinity2/ResidualMatrixAuthorsAll")

colnames(ma) = c("year",pp,pp2)
pdf("/Users/shiyansiadmin/Dropbox/Files/NewField2Data2/affinity2/ResidualAuthorsPlot.pdf")
for (i in 1:10) {
    for (j in (i+1):11) {
        yy = c(1991:2008)
        ma = matrix(yy,18,3)
        pp = paste("Cluster",toString(i),"- Cluster",toString(j))
        pp2 = paste("Cluster",toString(j),"- Cluster",toString(i))
        for (year in 1:18) {
            ma[year,2] = ta[i+11*(year-1),j]
            ma[year,3] = ta[j+11*(year-1),i]
        }
        plot(ma[,1],ma[,2],type="o",col ="red",xlab="year",ylab="Residual",ylim=c(-30,30),pch=1,lty=1,main="Variation of Residual Citation Based")
        lines(ma[,1],ma[,3],type="o",col ="blue",pch=2,lty=1)
        legend("topright",col=c("red","blue"),legend=c(pp,pp2),pch=1:2,lty=1)
    }
}
dev.off()