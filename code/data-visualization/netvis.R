library(sna)
library(network)
library(stringr)

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
regexp <- "([0-9]{4})"
stupidlist <- strsplit(filepath, "/")
otherlist <- strsplit(stupidlist[[1]][[13]], "-")
firstyear <- str_extract(otherlist[[1]][[1]], regexp)
endyear <- str_extract(otherlist[[1]][[2]], regexp)
outpath <- paste(outpath, field, run, type, firstyear, "-", endyear, "_", size, "years_vis.png", sep="")
title <- paste(field, run, firstyear, "-", endyear, sep=" ")

#visualization processing
net_lcnet <- read.paj(file=filepath)
png(outpath)
plot.network(net_lcnet, vertex.cex=0.4, mode="kamadakawai")
title(main=title)
dev.off()

q()
