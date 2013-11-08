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

cat.df <- read.csv(catCsv)
print(cat.df)

# 1. Evolution of Category Numbers over Time
hub.title <- paste("Evolution of Category Numbers Over Time -", field, run, sep=" ")
hub.outpath <- paste(outpath, field, run, "_Category_Metrics.png", sep="")
p <- ggplot(cat.df, aes(x=YEAR, y=NUMBER, group=Category, colour=Category)) + geom_line() + geom_point()
p <- p  + opts(title = hub.title)
p <- p + opts(axis.text.x = theme_text(face="bold", size="14"), axis.text.y = theme_text(face="bold", size="14"))
p <- p + xlab("YEAR") + ylab("# Authors in Category")
p <- p + aes(ymin=0) + xlim(as.integer(start_year), as.integer(end_year))
summary(p)
ggsave(p, file=hub.outpath, dpi=72)

scen.df <- read.csv(scenCsv)
print(scen.df)

# 2. Evolution of Scenario Numbers over Time
hub.title <- paste("Evolution of Scenario Numbers Over Time -", field, run, sep=" ")
hub.outpath <- paste(outpath, field, run, "_Scenario_Metrics.png", sep="")
p <- ggplot(scen.df, aes(x=YEAR, y=NUMBER, group=Scenario, colour=Scenario, shape=Scenario)) + geom_line() + geom_point(size=7)
p <- p  + opts(title = hub.title)
p <- p + opts(axis.text.x = theme_text(face="bold", size="14"), axis.text.y = theme_text(face="bold", size="14"))
p <- p + xlab("YEAR") + ylab("# Authors in Scenario")
p <- p + aes(ymin=0) + xlim(as.integer(start_year), as.integer(end_year))
summary(p)
ggsave(p, file=hub.outpath, dpi=72)

catPerc.df <- read.csv(catPercCsv)
print(catPerc.df)
# 3. Evolution of Category Numbers over Time
hub.title <- paste("Evolution of Category Numbers Over Time -", field, run, sep=" ")
hub.outpath <- paste(outpath, field, run, "_Category_Metrics_Percent.png", sep="")
p <- ggplot(catPerc.df, aes(x=YEAR, y=(NUMBER/TOTAL)*100, group=Category, colour=Category)) + geom_line() + geom_point()
p <- p  + opts(title = hub.title)
p <- p + opts(axis.text.x = theme_text(face="bold", size="14"), axis.text.y = theme_text(face="bold", size="14"))
p <- p + xlab("YEAR") + ylab("% of New Authors")
p <- p + aes(ymin=0) + xlim(as.integer(start_year), as.integer(end_year))
summary(p)
ggsave(p, file=hub.outpath, dpi=72)

scenPerc.df <- read.csv(scenPercCsv)
print(scenPerc.df)

# 4. Evolution of Scenario Numbers over Time
#hub.title <- paste("Evolution of Scenario Numbers Over Time -", field, run, sep=" ")
hub.outpath <- paste(outpath, field, run, "_Scenario_Metrics_Percent.png", sep="")
p <- ggplot(scenPerc.df, aes(x=YEAR, y=(NUMBER/TOTALNEW)*100, group=Scenario, colour=Scenario, shape=Scenario)) + geom_line() + geom_point(size=7)
#p <- p + scale_colour_manual(values=c("#111111", "#333333", "#555555", "#777777"), breaks=c("One","Two","Three", "Four"))
#p <- p + geom_line(colours=c("#111111", "#333333", "#555555", "#777777")) + geom_point(size=7)
p <- p + scale_colour_manual(values=c("grey30", "grey40", "grey50", "black"), breaks=c("One","Two","Three", "Four"))
#p <- p + geom_line() + geom_point(size=7)
#p <- p  + opts(title = hub.title)
p <- p + scale_shape_manual(values=c(18,19,6,0), breaks=c("One","Two","Three", "Four"))
p <- p + opts(axis.title.x = theme_text(face="bold", size=18), axis.title.y = theme_text(angle=90, face="bold", size=18), axis.text.x = theme_text(face="bold", size=18), axis.text.y = theme_text(face="bold", size=23), legend.title = theme_text(size=25), legend.text = theme_text(size=20))
p <- p + xlab("YEAR") + ylab("% of New Authors")
p <- p + aes(ymin=0) + xlim(as.integer(start_year), as.integer(end_year))
summary(p)
ggsave(p, file=hub.outpath, dpi=72)