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
regexp <- "([0-9]{4})"
stupidlist <- strsplit(filepath, "/")
otherlist <- strsplit(stupidlist[[1]][[13]], "-")
start <- str_extract(otherlist[[1]][[1]], regexp)
end <- str_extract(otherlist[[1]][[2]], regexp)
outpath <- paste(outpath, field, run, type, start, "-", end, "_", size, "years_lc.net", sep="")

#open csv file
data <- read.csv(csv)
print(data)

#import whole network, get edge, vertex count
wholenet <- read.graph(file=filepath, format="pajek")
total_size_nodes <- vcount(wholenet)
total_size_edges <- ecount(wholenet)

# induce large component, get edge, vertex count
c1 <- clusters(wholenet, mode="strong")
lcnet <- induced.subgraph(wholenet, which(c1$membership == which.max(c1$csize)))
lc_size_nodes <- vcount(lcnet)
lc_size_edges <- ecount(lcnet)

#get diameter of large component network
lc_diam <- average.path.length(lcnet, directed=FALSE)

#write csv
data2 <- data.frame(START=start, END=end, TOTAL_SIZE_NODES=total_size_nodes, TOTAL_SIZE_EDGES=total_size_edges, LC_SIZE_NODES=lc_size_nodes, LC_SIZE_EDGES=lc_size_edges, LC_DIAM=lc_diam)
newdata <- rbind(data, data2)
write.csv(newdata, csv, row.names=FALSE)

#write out large component graph
write.graph(lcnet, outpath, "pajek")
q()
