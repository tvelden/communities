library(igraph)
library(ggplot2)

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
	nodes.title <- paste("Largest Component Growth (by Nodes)", field, run, sep=" ")
	#print(nodes.title)
	edges.title <- paste("Largest Component Growth (by Edges)", field, run, sep=" ")
	#print(edges.title)

	#create plot from csv data for nodes with actual numbers
	p <- ggplot(data.df, aes(END, LC_SIZE_NODES)) + geom_line(colour="black") + geom_point(colour="red")
	p <- p  + opts(title = nodes.title)
	p <- p + opts(axis.text.x = theme_text(face="bold", size="14"), axis.text.y = theme_text(face="bold", size="14"))
	p <- p + xlab("Year") + ylab("Size")
	p <- p + aes(ymin=0) + xlim(as.integer(start_year), as.integer(end_year))
	summary(p)
	ggsave(p, file=nodes.actual.outpath, dpi=72)
	
	#create plot from csv data for nodes as percent of total network
	j <- ggplot(data.df, aes(END, (LC_SIZE_NODES/TOTAL_SIZE_NODES)*100)) + geom_line(colour="black") + geom_point(colour="red")
	j <- j  + opts(title = nodes.title)
	j <- j + opts(axis.text.x = theme_text(face="bold", size="14"), axis.text.y = theme_text(face="bold", size="14"))
	j <- j + xlab("Year") + ylab("Size(%)")
	j <- j + ylim(0, 100) + xlim(as.integer(start_year), as.integer(end_year))
	summary(j)
	ggsave(j, file=nodes.percent.outpath, dpi=72)

	#create plot from csv data for edges with the actual numbers
	q <- ggplot(data.df, aes(END, LC_SIZE_EDGES)) + geom_line(colour="black") + geom_point(colour="red")
	q <- q  + opts(title = edges.title)
	q <- q + opts(axis.text.x = theme_text(face="bold", size="14"), axis.text.y = theme_text(face="bold", size="14"))
	q <- q + xlab("Year") + ylab("Size")
	q <- q + aes(ymin=0) + xlim(as.integer(start_year), as.integer(end_year))
	summary(q)
	ggsave(q, file=edges.actual.outpath, dpi=72)

	#create plot from csv data for edges with the actual numbers
	h <- ggplot(data.df, aes(END, (LC_SIZE_EDGES/TOTAL_SIZE_EDGES)*100)) + geom_line(colour="black") + geom_point(colour="red")
	h <- h  + opts(title = edges.title)
	h <- h + opts(axis.text.x = theme_text(face="bold", size="14"), axis.text.y = theme_text(face="bold", size="14"))
	h <- h + xlab("Year") + ylab("Size(%)")
	h <- h + ylim(0, 100) + xlim(as.integer(start_year), as.integer(end_year))
	summary(h)
	ggsave(h, file=edges.percent.outpath, dpi=72)

} else if ( net_type == "whole" ) {
	#print("Plotting Whole Network Growth")
	data.df <- read.csv(csv)
	#print(data.df)
	nodes.outpath <- paste(outpath, "_actual_nodes.png", sep="")
	edges.outpath <- paste(outpath, "_actual_edges.png", sep="")
	nodes.title <- paste("Whole Network Growth (by Nodes)", field, run, sep=" ")
	#print(nodes.title)
	edges.title <- paste("Whole Network Growth (by Edges)", field, run, sep=" ")
	#print(edges.title)

	#create plot from csv data
	p <- ggplot(data.df, aes(END, TOTAL_SIZE_NODES)) + geom_line(colour="black") + geom_point(colour="red")
	p <- p  + opts(title = nodes.title)
	p <- p + opts(axis.text.x = theme_text(face="bold", size="14"), axis.text.y = theme_text(face="bold", size="14"))
	p <- p + xlab("Year") + ylab("Size")
	p <- p + aes(ymin=0) + xlim(as.integer(start_year), as.integer(end_year))
	summary(p)
	ggsave(p, file=nodes.outpath, dpi=72)

	q <- ggplot(data.df, aes(END, TOTAL_SIZE_EDGES)) + geom_line(colour="black") + geom_point(colour="red")
	q <- q  + opts(title = edges.title)
	q <- q + opts(axis.text.x = theme_text(face="bold", size="14"), axis.text.y = theme_text(face="bold", size="14"))
	q <- q + xlab("Year") + ylab("Size")
	q <- q + aes(ymin=0) + xlim(as.integer(start_year), as.integer(end_year))
	summary(q)
	ggsave(q, file=edges.outpath, dpi=72)

} else if ( net_type == "sndlc" ) {
	#print("Plotting Large Component Growth")
	data.df <- read.csv(csv)
	whole.df <- read.csv(csv2)
	total.df <- merge(data.df, whole.df)
	#print(data.df)
	nodes.actual.outpath <- paste(outpath, "_actual_nodes.png", sep="")
	edges.actual.outpath <- paste(outpath, "_actual_edges.png", sep="")
	nodes.percent.outpath <- paste(outpath, "_percent_nodes.png", sep="")
	edges.percent.outpath <- paste(outpath, "_percent_edges.png", sep="")
	nodes.title <- paste("Second Largest Component Growth (by Nodes)", field, run, sep=" ")
	#print(nodes.title)
	edges.title <- paste("Second Largest Component Growth (by Edges)", field, run, sep=" ")
	#print(edges.title)

	#create plot of second largest component from csv data with actual numbers in terms of nodes
	p <- ggplot(data.df, aes(END, SNDLC_SIZE_NODES)) + geom_line(colour="black") + geom_point(colour="red")
	p <- p  + opts(title = nodes.title)
	p <- p + opts(axis.text.x = theme_text(face="bold", size="14"), axis.text.y = theme_text(face="bold", size="14"))
	p <- p + xlab("Year") + ylab("Size")
	p <- p + aes(ymin=0) + xlim(as.integer(start_year), as.integer(end_year))
	summary(p)
	ggsave(p, file=nodes.actual.outpath, dpi=72)

	#create plot of second largest component from csv data with percent in terms of nodes
	h <- ggplot(total.df, aes(END, (SNDLC_SIZE_NODES/TOTAL_SIZE_NODES)*100)) + geom_line(colour="black") + geom_point(colour="red")
	h <- h  + opts(title = nodes.title)
	h <- h + opts(axis.text.x = theme_text(face="bold", size="14"), axis.text.y = theme_text(face="bold", size="14"))
	h <- h + xlab("Year") + ylab("Size(%)")
	h <- h + ylim(0, 100) + xlim(as.integer(start_year), as.integer(end_year))
	summary(h)
	ggsave(h, file=nodes.percent.outpath, dpi=72)


	#create plot of second largest component from csv data with actual numbers in terms of edges
	q <- ggplot(data.df, aes(END, SNDLC_SIZE_EDGES)) + geom_line(colour="black") + geom_point(colour="red")
	q <- q  + opts(title = edges.title)
	q <- q + opts(axis.text.x = theme_text(face="bold", size="14"), axis.text.y = theme_text(face="bold", size="14"))
	q <- q + xlab("Year") + ylab("Size")
	q <- q + aes(ymin=0) + xlim(as.integer(start_year), as.integer(end_year))
	summary(q)
	ggsave(q, file=edges.actual.outpath, dpi=72)

	#create a plot of second largest component from csv data with percent of network in terms of edges
	k <- ggplot(total.df, aes(END, (SNDLC_SIZE_EDGES/TOTAL_SIZE_EDGES)*100)) + geom_line(colour="black") + geom_point(colour="red")
	k <- k  + opts(title = edges.title)
	k <- k + opts(axis.text.x = theme_text(face="bold", size="14"), axis.text.y = theme_text(face="bold", size="14"))
	k <- k + xlab("Year") + ylab("Size")
	k <- k + ylim(0, 100) + xlim(as.integer(start_year), as.integer(end_year))
	summary(k)
	ggsave(k, file=edges.percent.outpath, dpi=72)

}
q()
