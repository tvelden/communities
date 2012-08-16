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
	nodes.outpath <- paste(outpath, "_actual_nodes.png", sep="")
	edges.outpath <- paste(outpath, "_actual_edges.png", sep="")
	nodes.title <- paste("Largest Component Growth (by Nodes)", field, run, sep=" ")
	#print(nodes.title)
	edges.title <- paste("Largest Component Growth (by Edges)", field, run, sep=" ")
	#print(edges.title)

	#create plot from csv data
	p <- ggplot(data.df, aes(END, LC_SIZE_NODES)) + geom_line(colour="black") + geom_point(colour="red")
	p <- p  + opts(title = nodes.title)
	p <- p + opts(axis.text.x = theme_text(face="bold", size="14"), axis.text.y = theme_text(face="bold", size="14"))
	p <- p + xlab("Year") + ylab("Size")
	p <- p + aes(ymin=0) + xlim(as.integer(start_year), as.integer(end_year))
	summary(p)
	ggsave(p, file=nodes.outpath, dpi=72)

	q <- ggplot(data.df, aes(END, LC_SIZE_EDGES)) + geom_line(colour="black") + geom_point(colour="red")
	q <- q  + opts(title = edges.title)
	q <- q + opts(axis.text.x = theme_text(face="bold", size="14"), axis.text.y = theme_text(face="bold", size="14"))
	q <- q + xlab("Year") + ylab("Size")
	q <- q + aes(ymin=0) + xlim(as.integer(start_year), as.integer(end_year))
	summary(q)
	ggsave(q, file=edges.outpath, dpi=72)

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
}	
q()
