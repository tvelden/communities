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

data.df <- read.csv(csv)
print(data.df)

# 1. create Old to New Authors plot using real numbers for all both inside and outside large component
nodes.outpath <- paste(outpath, field, run, "HUB_TO_NEW_plot.png", sep="")
nodes.title <- paste("Connections Between Hub Nodes And New Authors", field, run, sep=" ")
#create plot from csv data
p <- ggplot(data.df, aes(YEAR)) + geom_line(aes(y=HUBTONEW, colour="HUBTONEW"))
#add annotation and save
p <- p  + opts(title = nodes.title)
p <- p + opts(axis.text.x = theme_text(face="bold", size="14"), axis.text.y = theme_text(face="bold", size="14"))
p <- p + xlab("Year") + ylab("# of new connections between hub and new author")
p <- p + aes(ymin=0) + xlim(as.integer(start_year), as.integer(end_year))
summary(p)
ggsave(p, file=nodes.outpath, dpi=72)


q()
