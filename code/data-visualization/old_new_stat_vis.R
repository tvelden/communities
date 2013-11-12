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

data.df <- read.csv(csv)
print(data.df)
#calculate percentages and append to dataframe, data.df
data.df$OLDTOTALPERC <- (data.df$OLD / data.df$SIZE) * 100
data.df$NEWTOTALPERC <- (data.df$NEW / data.df$SIZE) * 100
data.df$OLDinLCPERC <- (data.df$OLDIN / data.df$inLC) * 100
data.df$NEWinLCPERC <- (data.df$NEWIN / data.df$inLC) * 100
data.df$OLDoutLCPERC <- (data.df$OLDOUT / data.df$outLC) * 100
data.df$NEWoutLCPERC <- (data.df$NEWOUT / data.df$outLC) * 100
data.df$OLDinPERC <- (data.df$OLDIN / data.df$SIZE) * 100
data.df$NEWinPERC <- (data.df$NEWIN / data.df$SIZE) * 100
data.df$OLDoutPERC <- (data.df$OLDOUT / data.df$SIZE) * 100
data.df$NEWoutPERC <- (data.df$NEWOUT / data.df$SIZE) * 100

# 1. create Old to New Authors plot using real numbers for all both inside and outside large component
nodes.outpath <- paste(outpath, field, run, "OLDNEW-INOUT_plot.png", sep="")
nodes.title <- paste("Connections between Old/New Authors and Large Component Members", field, run, sep=" ")
#create plot from csv data
p <- ggplot(data.df, aes(YEAR)) + geom_line(aes(y=OLDIN, colour="OLDIN")) + geom_line(aes(y=NEWIN, colour="NEWIN"))
p <-  p + geom_line(aes(y=OLDOUT, colour="OLDOUT")) + geom_line(aes(y=NEWOUT, colour="NEWOUT"))
#add annotation and save
p <- p  + opts(title = nodes.title)
p <- p + opts(axis.text.x = theme_text(face="bold", size="14"), axis.text.y = theme_text(face="bold", size="14"))
p <- p + xlab("Year") + ylab("# of Authors")
p <- p + aes(ymin=0) + xlim(as.integer(start_year), as.integer(end_year))
summary(p)
ggsave(p, file=nodes.outpath, dpi=72)

# 2. create Old to New Author plot using real numbers just for inside large component
nodes.outpath <- paste(outpath, field, run, "OLDNEW-IN_plot.png", sep="")
nodes.title <- paste("Connections between Old/New Authors in Large Component Only", field, run, sep=" ")
#create plot from csv data
q <- ggplot(data.df, aes(YEAR)) + geom_line(aes(y=OLDIN, colour="OLDIN")) + geom_line(aes(y=NEWIN, colour="NEWIN"))
# add annotation and save
q <- q  + opts(title = nodes.title)
q <- q + opts(axis.text.x = theme_text(face="bold", size="14"), axis.text.y = theme_text(face="bold", size="14"))
q <- q + xlab("Year") + ylab("# of Authors")
q <- q + aes(ymin=0) + xlim(as.integer(start_year), as.integer(end_year))
summary(q)
ggsave(q, file=nodes.outpath, dpi=72)

# 3. create Old to New Author plot using real numbers just for nodes outside large component
nodes.outpath <- paste(outpath, field, run, "OLDNEW-OUT_plot.png", sep="")
nodes.title <- paste("Connections between Old/New Authors outside Large Component Only", field, run, sep=" ")
#create plot from csv data
k <-  ggplot(data.df, aes(YEAR)) + geom_line(aes(y=OLDOUT, colour="OLDOUT")) + geom_line(aes(y=NEWOUT, colour="NEWOUT"))
# add annotation and save
k <- k  + opts(title = nodes.title)
k <- k + opts(axis.text.x = theme_text(face="bold", size="14"), axis.text.y = theme_text(face="bold", size="14"))
k <- k + xlab("Year") + ylab("# of Authors")
k <- k + aes(ymin=0) + xlim(as.integer(start_year), as.integer(end_year))
summary(k)
ggsave(k, file=nodes.outpath, dpi=72)

# 4. create plot of Old and New Authors as percentage of total network 
nodes.outpath <- paste(outpath, field, run, "OLDNEW-totalPERC_plot.png", sep="")
nodes.title <- paste("Old and New Authors as a percentage of the total network", field, run, sep=" ")
#create plot from csv data
a <-  ggplot(data.df, aes(YEAR)) + geom_line(aes(y=OLDTOTALPERC, colour="OLDTOTALPERC")) + geom_line(aes(y=NEWTOTALPERC, colour="NEWTOTALPERC"))
# add annotation and save
a <- a + opts(title = nodes.title)
a <- a + opts(axis.text.x = theme_text(face="bold", size="14"), axis.text.y = theme_text(face="bold", size="14"))
a <- a + xlab("Year") + ylab("% of Authors")
a <- a + aes(ymin=0, ymax=100) + xlim(as.integer(start_year), as.integer(end_year))
summary(a)
ggsave(a, file=nodes.outpath, dpi=72)

# 5. create plot of Old and New authors outside large component as percentage of total outside large component
nodes.outpath <- paste(outpath, field, run, "OLDNEW-outLCPERC_plot.png", sep="")
nodes.title <- paste("Old and New Authors outside LC as percentage of total outside LC", field, run, sep=" ")
#create plot from csv data
b <-  ggplot(data.df, aes(YEAR)) + geom_line(aes(y=OLDoutLCPERC, colour="OLDoutLCPERC")) + geom_line(aes(y=NEWoutLCPERC, colour="NEW_outLCPERC"))
# add annotation and save
b <- b + opts(title = nodes.title)
b <- b + opts(axis.text.x = theme_text(face="bold", size="14"), axis.text.y = theme_text(face="bold", size="14"))
b <- b + xlab("Year") + ylab("% of Authors")
b <- b + aes(ymin=0, ymax=100) + xlim(as.integer(start_year), as.integer(end_year))
summary(b)
ggsave(b, file=nodes.outpath, dpi=72)

# 6. create plot of Old and New authors inside large component as percentage of total outside large component
nodes.outpath <- paste(outpath, field, run, "OLDNEW-inLCPERC_plot.png", sep="")
nodes.title <- paste("Old and New Authors outside LC as percentage of total outside LC", field, run, sep=" ")
#create plot from csv data
b <-  ggplot(data.df, aes(YEAR)) + geom_line(aes(y=OLDinLCPERC, colour="OLDinLCPERC")) + geom_line(aes(y=NEWinLCPERC, colour="NEW_inLCPERC"))
# add annotation and save
b <- b + opts(title = nodes.title)
b <- b + opts(axis.text.x = theme_text(face="bold", size="14"), axis.text.y = theme_text(face="bold", size="14"))
b <- b + xlab("Year") + ylab("% of Authors")
b <- b + aes(ymin=0, ymax=100) + xlim(as.integer(start_year), as.integer(end_year))
summary(b)
ggsave(b, file=nodes.outpath, dpi=72)

# 7.
nodes.outpath <- paste(outpath, field, run, "OLDNEW-OUTINPERC_plot.png", sep="")
nodes.title <- paste("Old and New Authors inside and outside LC as percentage of total network size", field, run, sep=" ")
#create plot from csv data
c <-  ggplot(data.df, aes(YEAR)) + geom_line(aes(y=OLDinPERC, colour="OLDinPERC")) + geom_line(aes(y=NEWinPERC, colour="NEWinPERC"))
c <-  c + geom_line(aes(y=OLDoutPERC, colour="OLDoutPERC")) + geom_line(aes(y=NEWoutPERC, colour="NEWoutPERC"))

# add annotation and save
c <- c + opts(title = nodes.title)
c <- c + opts(axis.text.x = theme_text(face="bold", size="14"), axis.text.y = theme_text(face="bold", size="14"))
c <- c + xlab("Year") + ylab("% of Authors")
c <- c + aes(ymin=0, ymax=100) + xlim(as.integer(start_year), as.integer(end_year))
summary(c)
ggsave(c, file=nodes.outpath, dpi=72)










#p <- p  + opts(title = nodes.title)
#p <- p + opts(axis.text.x = theme_text(face="bold", size="14"), axis.text.y = theme_text(face="bold", size="14"))
#p <- p + xlab("Year") + ylab("# of Authors")
#p <- p + aes(ymin=0) + xlim(as.integer(start_year), as.integer(end_year))
#summary(p)
#ggsave(p, file=nodes.outpath, dpi=72)



q()
