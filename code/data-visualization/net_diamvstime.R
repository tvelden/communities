library(igraph)
library(ggplot2)

#suppresses Rplot.pdf output
options(device = function(...) {
    pdf(file=NULL)
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
	print(data.df)
	nodes.outpath <- paste(outpath, "_diam.png", sep="")
	nodes.title <- paste("Largest Component Diameter -", field, run, sep=" ")

	#create plot from csv data
	p <- ggplot(data.df, aes(END, LC_DIAM)) + geom_line(colour="black") + geom_point(colour="red")
	p <- p  + opts(title = nodes.title)
	p <- p + opts(axis.text.x = theme_text(face="bold", size="14"), axis.text.y = theme_text(face="bold", size="14"))
	p <- p + xlab("Year") + ylab("Diameter")
	p <- p + aes(ymin=0) + xlim(as.integer(start_year), as.integer(end_year))
	summary(p)
	ggsave(p, file=nodes.outpath, dpi=72)

} else if ( net_type == "sndlc" ) {
	#print("Plotting Whole Network Growth")
	data.df <- read.csv(csv)
	#print(data.df)
	nodes.outpath <- paste(outpath, "_diam.png", sep="")
	nodes.title <- paste("Second Largest Component Diameter", field, run, sep=" ")
	#print(nodes.title)

	#create plot from csv data
	p <- ggplot(data.df, aes(END, SNDLC_DIAM)) + geom_line(colour="black") + geom_point(colour="red")
	p <- p  + opts(title = nodes.title)
	p <- p + opts(axis.text.x = theme_text(face="bold", size="14"), axis.text.y = theme_text(face="bold", size="14"))
	p <- p + xlab("Year") + ylab("Size")
	p <- p + aes(ymin=0) + xlim(as.integer(start_year), as.integer(end_year))
	summary(p)
	ggsave(p, file=nodes.outpath, dpi=72)


}

q()
