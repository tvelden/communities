# Portion Match Visualization
pdf("/Users/shiyansiadmin/Dropbox/Files/NewMatch.pdf")
tcc = c("DC1","DC2","DC3","DC4","DC5","DC6","DC7","DC8","DC9","DC10","DC11") 
color = c("black","grey","red","green","yellow","orange","purple","brown","lightblue","violet","darkblue","white")
for (k in 1:1) {
    da = read.table(paste("/Users/shiyansiadmin/Dropbox/Files/8slicesPortion",toString(k),sep=""),header=TRUE)
    dar= da[,2:12]
    rownames(dar) = tcc
    damatrix = as.matrix(dar)
    ta = as.table(damatrix)
    ta = t(ta)
    propro = prop.table(ta,2)
    barplot(propro,legend.text=T,col=color,args.legend = list(x = ncol(propro) + 3.5, y=max(colSums(propro))),bty="n",main=paste(toString(1991+(k-1)*7),"-",toString(1998+(k-1)*7)," Overlap of Dynamic Clusters (DC) with Accumulative Clusters (AC)",sep=""))
}
dev.off()
