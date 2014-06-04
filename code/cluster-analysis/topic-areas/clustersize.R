#clustersize.R
da = read.table("/Users/shiyansiadmin/Dropbox/Files/NewField2Data2/clustersize.txt",header=T)
tcc = c("AC1","AC2","AC3","AC4","AC5","AC6","AC7","AC8","AC9","AC10","AC11") 
color = c("black","grey","red","green","yellow","orange","purple","brown","lightblue","violet","darkblue","white")
subdata = da[1:22,]
plot(publ~year,data=subdata,ylim=c(0,900),xlim=c(1991,2012),lty=1,pch=2,type="o",col="black",main="Variation of Sizes of Accumulative Clusters",ylab="# of Publications",xlab="year")
for (i in 2:11) {
    k = i-1
    k1= 22*k+1
    k2= 22*k + 22
    subdata = da[k1:k2,]
    lines(publ~year,data=subdata,type="o",col=color[i],pch=2,lty=1)
}
legend("topleft", legend=tcc, col=color[1:11], pch=2,lty=1,cex=1)