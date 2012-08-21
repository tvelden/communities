library(sna)
library(network)
library(stringr)

#suppresses Rplot.pdf output
options(device = function(...) {
    .Call("R_GD_nullDevice", PACKAGE = "grDevices")
})

#parse arguments
args=(commandArgs(trailingOnly=TRUE))
if(length(args)==0){
	print("No arguments supplied")
} else {
	for(i in 1:length(args)){
		eval(parse(text=args[[i]]))
	}
}

#extract start and end year of time slice from file name
yearsplit <- strsplit(years, "-")
start <- yearsplit[[1]][[1]]
end <- yearsplit[[1]][[2]]
#outpath <- paste(outpath, field, run, type, firstyear, "-", end, "_", size, "years_vis.png", sep="")
title <- paste(field, run, start, "-", end, sep=" ")
print(outpath)
print(title)
#visualization processing
net_lcnet <- read.paj(file=filepath)
png(outpath)
plot.network(net_lcnet, vertex.cex=0.4, mode="kamadakawai")
title(main=title)
dev.off()

q()
