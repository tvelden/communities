library(igraph)
library(ggplot2)

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

if ( net_type == "lc" ) {
	#print("Plotting Large Component Growth")
	data.df <- read.csv(csv)
	#print(data.df)
	nodes.actual.outpath <- paste(outpath, "_actual_nodes.png", sep="")
	edges.actual.outpath <- paste(outpath, "_actual_edges.png", sep="")
	nodes.percent.outpath <- paste(outpath, "_percent_nodes.png", sep="")
	edges.percent.outpath <- paste(outpath, "_percent_edges.png", sep="")
	nodes.title <- paste("Largest Component Diameter vs. Size (by Nodes)", field, run, sep=" ")
	#print(nodes.title)
	edges.title <- paste("Largest Component Diameter vs. Size (by Edges)", field, run, sep=" ")
	#print(edges.title)

	#create plot from csv data for nodes with actual numbers
	p <- ggplot(data.df, aes(LC_SIZE_NODES, LC_DIAM)) + geom_point(shape=1, colour="red")
	p <- p  + opts(title = nodes.title)
	p <- p + opts(axis.text.x = theme_text(face="bold", size="14"), axis.text.y = theme_text(face="bold", size="14"))
	p <- p + xlab("# of Authors in Large Component") + ylab("Diameter of Large Component")
	p <- p + aes(ymin=0) + aes(xmin=0)
	summary(p)
	ggsave(p, file=nodes.actual.outpath, dpi=72)
	
	#create plot from csv data for nodes as percent of total network
	j <- ggplot(data.df, aes((LC_SIZE_NODES/TOTAL_SIZE_NODES)*100, LC_DIAM)) + geom_point(shape=1, colour="red")
	j <- j  + opts(title = nodes.title)
	j <- j + opts(axis.text.x = theme_text(face="bold", size="14"), axis.text.y = theme_text(face="bold", size="14"))
	j <- j + xlab("% of Authors in Large Component") + ylab("Diameter of Large Component")
	j <- j + aes(ymin=0) + xlim(0, 100)
	summary(j)
	ggsave(j, file=nodes.percent.outpath, dpi=72)

	#create plot from csv data for edges with the actual numbers
	q <- ggplot(data.df, aes(LC_SIZE_EDGES, LC_DIAM)) + geom_point(shape=1, colour="red")
	q <- q  + opts(title = edges.title)
	q <- q + opts(axis.text.x = theme_text(face="bold", size="14"), axis.text.y = theme_text(face="bold", size="14"))
	q <- q + xlab("# of Edges in Large Component") + ylab("Diameter of Large Component")
	q <- q + aes(ymin=0) + aes(xmin=0)
	summary(q)
	ggsave(q, file=edges.actual.outpath, dpi=72)

	#create plot from csv data for edges with the actual numbers
	h <- ggplot(data.df, aes((LC_SIZE_EDGES/TOTAL_SIZE_EDGES)*100, LC_DIAM)) + geom_point(shape=1, colour="red")
	h <- h  + opts(title = edges.title)
	h <- h + opts(axis.text.x = theme_text(face="bold", size="14"), axis.text.y = theme_text(face="bold", size="14"))
	h <- h + xlab("% of Edges in Large Component") + ylab("Diameter of Large Component")
	h <- h + aes(ymin=0) + xlim(0, 100)
	summary(h)
	ggsave(h, file=edges.percent.outpath, dpi=72)

} else if ( net_type == "sndlc" ) {
	#print("Plotting Second Largest Component Diameter")
	data.df <- read.csv(csv)
	whole.df <- read.csv(csv2)
	total.df <- merge(data.df, whole.df)
	#print(data.df)
	nodes.actual.outpath <- paste(outpath, "_actual_nodes.png", sep="")
	edges.actual.outpath <- paste(outpath, "_actual_edges.png", sep="")
	nodes.percent.outpath <- paste(outpath, "_percent_nodes.png", sep="")
	edges.percent.outpath <- paste(outpath, "_percent_edges.png", sep="")
	nodes.title <- paste("Second Largest Component Diameter vs. Size (by Nodes)", field, run, sep=" ")
	#print(nodes.title)
	edges.title <- paste("Second Largest Component Diameter vs. Size (by Edges)", field, run, sep=" ")
	#print(edges.title)

	#create plot of second largest component from csv data with actual numbers in terms of nodes
	p <- ggplot(data.df, aes(SNDLC_SIZE_NODES, SNDLC_DIAM)) + geom_point(shape=1, colour="red")
	p <- p  + opts(title = nodes.title)
	p <- p + opts(axis.text.x = theme_text(face="bold", size="14"), axis.text.y = theme_text(face="bold", size="14"))
	p <- p + xlab("# of Authors in the Second Largest Component") + ylab("Diameter of Second Largest Component")
	p <- p + aes(ymin=0) + aes(xmin=0)
	summary(p)
	ggsave(p, file=nodes.actual.outpath, dpi=72)

	#create plot of second largest component from csv data with percent in terms of nodes
	h <- ggplot(total.df, aes((SNDLC_SIZE_NODES/TOTAL_SIZE_NODES)*100, SNDLC_DIAM)) + geom_point(shape=1, colour="red")
	h <- h  + opts(title = nodes.title)
	h <- h + opts(axis.text.x = theme_text(face="bold", size="14"), axis.text.y = theme_text(face="bold", size="14"))
	h <- h + xlab("% of Authors in the Second Largest Component") + ylab("Diameter of Second Largest Component")
	h <- h + aes(ymin=0) + xlim(0, 100)
	summary(h)
	ggsave(h, file=nodes.percent.outpath, dpi=72)


	#create plot of second largest component from csv data with actual numbers in terms of edges
	q <- ggplot(data.df, aes(SNDLC_SIZE_EDGES, SNDLC_DIAM)) + geom_point(shape=1, colour="red")
	q <- q  + opts(title = edges.title)
	q <- q + opts(axis.text.x = theme_text(face="bold", size="14"), axis.text.y = theme_text(face="bold", size="14"))
	q <- q + xlab("# of Edges in the Second Largest Component") + ylab("Diameter of Second Largest Component")
	q <- q + aes(ymin=0) + aes(xmin=0)
	summary(q)
	ggsave(q, file=edges.actual.outpath, dpi=72)

	#create a plot of second largest component from csv data with percent of network in terms of edges
	k <- ggplot(total.df, aes(END, (SNDLC_SIZE_EDGES/TOTAL_SIZE_EDGES)*100, SNDLC_DIAM)) + geom_point(shape=1, colour="red")
	k <- k  + opts(title = edges.title)
	k <- k + opts(axis.text.x = theme_text(face="bold", size="14"), axis.text.y = theme_text(face="bold", size="14"))
	k <- k + xlab("% of Edges in the Second Largest Component") + ylab("Diameter of Second Largest Component")
	k <- k + aes(ymin=0) + xlim(0, 100)
	summary(k)
	ggsave(k, file=edges.percent.outpath, dpi=72)

}
q()
