library(igraph)
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
yearsplit <- strsplit(years, "-")
start <- yearsplit[[1]][[1]]
end <- yearsplit[[1]][[2]]

#open csv file
data <- read.csv(csv)
print(data)

#induce second largest component, size in nodes/edges, diameter
wholenet <- read.graph(file=filepath, format="pajek")
c1 <- clusters(wholenet, mode="strong")
lc_index <- which.max(c1$csize)
c1$csize[lc_index]=0
sndlcnet <- induced.subgraph(wholenet, which(c1$membership == which.max(c1$csize)))
sndlc_size_nodes <- vcount(sndlcnet)
sndlc_size_edges <- ecount(sndlcnet)
sndlc_diam <- diameter(sndlcnet, directed=FALSE, unconnected=FALSE)

#write out csv
data2 <- data.frame(START=start, END=end, SNDLC_SIZE_NODES=sndlc_size_nodes, SNDLC_SIZE_EDGES=sndlc_size_edges, SNDLC_DIAM=sndlc_diam)
newdata <- rbind(data, data2)
write.csv(newdata, csv, row.names=FALSE)

#write out graph
write.graph(sndlcnet, outpath, "pajek")
q()


