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

# 1. histogram with y-axis as # of authors and x-axis as # of years since first entering the network
#    to being distinguished as a hub
hub.title <- paste("Number of Years Since Joining The Field to Being Distinguished As A Hub", field, run, sep=" ")
hub.outpath <- paste(outpath, field, run, "Number_Year_In_Network_To_Hub_Distinction.png", sep="")
ySince <- data.frame(data.df$yearsSinceFirstPub)
names(ySince) <- "yearsSinceFirstPub"
print(ySince)
p <- ggplot(ySince, aes(x=yearsSinceFirstPub)) + geom_histogram(binwidth=1, colour="black", fill="white")
p <- p  + opts(title = hub.title)
p <- p + opts(axis.text.x = theme_text(face="bold", size="14"), axis.text.y = theme_text(face="bold", size="14"))
p <- p + xlab("# of Years Since First Publication") + ylab("# of Authors")
p <- p + aes(ymin=0) + xlim(0,20)
summary(p)
ggsave(p, file=hub.outpath, dpi=72)

# 2. histogram with y-axis as # of authors and x-axis as # of years active since entering the network
#    to being distinguished as a hub
hub.title <- paste("Number of Active Years Since Joining The Field to Being Distinguished As A Hub", field, run, sep=" ")
hub.outpath <- paste(outpath, field, run, "Number_ActiveYears_In_Network_To_Hub_Distinction.png", sep="")
p <- ggplot(data.df, aes(x=activeYears)) + geom_histogram(binwidth=1, colour="black", fill="white")
p <- p  + opts(title = hub.title)
p <- p + opts(axis.text.x = theme_text(face="bold", size="14"), axis.text.y = theme_text(face="bold", size="14"))
p <- p + xlab("# of Active Years In Field") + ylab("# of Authors")
p <- p + aes(ymin=0) + xlim(0,20)
summary(p)
ggsave(p, file=hub.outpath, dpi=72)

# 3. histogram with y-axis as # of authors and x-axis as # of publications since entering the network
hub.title <- paste("Number of Publications Since Joining The Field to Being Distinguished As A Hub", field, run, sep=" ")
hub.outpath <- paste(outpath, field, run, "Number_Publications_In_Network_To_Hub_Distinction.png", sep="")
p <- ggplot(data.df, aes(x=numPublished)) + geom_histogram(binwidth=1, colour="black", fill="white")
p <- p  + opts(title = hub.title)
p <- p + opts(axis.text.x = theme_text(face="bold", size="14"), axis.text.y = theme_text(face="bold", size="14"))
p <- p + xlab("# of Publications In Field") + ylab("# of Authors")
p <- p + aes(ymin=0) + xlim(0,20)
summary(p)
ggsave(p, file=hub.outpath, dpi=72)

