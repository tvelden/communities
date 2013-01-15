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
p <- ggplot(scen.df, aes(x=YEAR, y=NUMBER, group=Scenario, colour=Scenario)) + geom_line() + geom_point()
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
p <- p + xlab("YEAR") + ylab("% Authors Of Total Network In Category")
p <- p + aes(ymin=0) + xlim(as.integer(start_year), as.integer(end_year))
summary(p)
ggsave(p, file=hub.outpath, dpi=72)

scenPerc.df <- read.csv(scenPercCsv)
print(scenPerc.df)

# 4. Evolution of Scenario Numbers over Time
hub.title <- paste("Evolution of Scenario Numbers Over Time -", field, run, sep=" ")
hub.outpath <- paste(outpath, field, run, "_Scenario_Metrics_Percent.png", sep="")
p <- ggplot(scenPerc.df, aes(x=YEAR, y=(NUMBER/TOTALNEW)*100, group=Scenario, colour=Scenario)) + geom_line() + geom_point()
p <- p  + opts(title = hub.title)
p <- p + opts(axis.text.x = theme_text(face="bold", size="14"), axis.text.y = theme_text(face="bold", size="14"))
p <- p + xlab("YEAR") + ylab("% Authors Of Total Network In Scenario")
p <- p + aes(ymin=0) + xlim(as.integer(start_year), as.integer(end_year))
summary(p)
ggsave(p, file=hub.outpath, dpi=72)