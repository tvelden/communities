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
nodes.outpath <- paste(outpath, field, run, "NEW_NODES_FROM_PUREMIXED_COMPONENTS_plot.png", sep="")
nodes.title <- paste("Percent of new nodes from Pure vs Mixed Components", field, run, sep=" ")
#Make new data frames
pure <- data.frame(data.df$YEAR, data.df$newFromPure, data.df$totalNodes)
pure$TYPE <- rep("pure", nrow(pure))
names(pure) <- c("YEAR", "nodes", "totalNodes", "TYPE")
mixed <- data.frame(data.df$YEAR, data.df$newFromMixed, data.df$totalNodes)
mixed$TYPE <- rep("mixed", nrow(mixed))
names(mixed) <- c("YEAR", "nodes", "totalNodes", "TYPE")
newFromPureMixed <- rbind(pure, mixed)
#create plot from csv data
p <- ggplot(newFromPureMixed, aes(x=YEAR, y=(nodes/totalNodes)*100, group=TYPE, shape=TYPE, colour=TYPE)) + geom_line() + geom_point()
#add annotation and save
p <- p  + opts(title = nodes.title)
p <- p + opts(axis.text.x = theme_text(face="bold", size="14"), axis.text.y = theme_text(face="bold", size="14"))
p <- p + xlab("Year") + ylab("% new nodes from total network")
p <- p + ylim(0,100) + xlim(as.integer(start_year), as.integer(end_year))
summary(p)
ggsave(p, file=nodes.outpath, dpi=72)

# 2. create Old to New Authors plot using real numbers for all both inside and outside large component
nodes.outpath <- paste(outpath, field, run, "OLD_NODES_FROM_PUREMIXED_COMPONENTS_plot.png", sep="")
nodes.title <- paste("Percent of old nodes from Pure vs. Mixed Components", field, run, sep=" ")
#Make new data frames
pure <- data.frame(data.df$YEAR, data.df$oldFromPure, data.df$totalNodes)
pure$TYPE <- rep("pure", nrow(pure))
names(pure) <- c("YEAR", "nodes", "totalNodes", "TYPE")
mixed <- data.frame(data.df$YEAR, data.df$oldFromMixed, data.df$totalNodes)
mixed$TYPE <- rep("mixed", nrow(mixed))
names(mixed) <- c("YEAR", "nodes", "totalNodes", "TYPE")
newFromPureMixed <- rbind(pure, mixed)

#create plot from csv data
p <- ggplot(newFromPureMixed, aes(x=YEAR, y=(nodes/totalNodes)*100, group=TYPE, shape=TYPE, colour=TYPE)) + geom_line() + geom_point()
#add annotation and save
p <- p  + opts(title = nodes.title)
p <- p + opts(axis.text.x = theme_text(face="bold", size="14"), axis.text.y = theme_text(face="bold", size="14"))
p <- p + xlab("Year") + ylab("% OLD nodes from total network")
p <- p + ylim(0,100) + xlim(as.integer(start_year), as.integer(end_year))
summary(p)
ggsave(p, file=nodes.outpath, dpi=72)

# 3. Create plot of % of all nodes coming from pure components vs. mixed components with dotted lines for old vs. new nodes
nodes.outpath <- paste(outpath, field, run, "PUREMIXED_COMPONENTS_COMPREHENSIVEplot.png", sep="")
nodes.title <- paste("Old and New Nodes from Pure vs. Mixed Components", field, run, sep=" ")
#make data frames
pureComp <- data.frame(data.df$YEAR, ((data.df$newFromPure + data.df$oldFromPure)/data.df$totalNodes)*100)
pureComp$TYPE <- rep("Pure Component", nrow(data.df))
names(pureComp) <- c("YEAR", "percent", "TYPE")
mixedComp <- data.frame(data.df$YEAR, ((data.df$newFromMixed + data.df$oldFromMixed)*100/data.df$totalNodes))
mixedComp$TYPE <- rep("Mixed Component", nrow(data.df))
names(mixedComp) <- c("YEAR", "percent", "TYPE")
newPure <- data.frame(data.df$YEAR, (data.df$newFromPure*100/data.df$totalNodes))
newPure$TYPE <- rep ("New From Pure", nrow(data.df))
names(newPure) <- c("YEAR", "percent", "TYPE")
oldPure <- data.frame(data.df$YEAR, (data.df$oldFromPure*100/data.df$totalNodes))
oldPure$TYPE <- rep ("Old From Pure", nrow(data.df))
names(oldPure) <- c("YEAR", "percent", "TYPE")
newMixed <- data.frame(data.df$YEAR, (data.df$newFromMixed*100/data.df$totalNodes))
newMixed$TYPE <- rep("New From Mixed", nrow(data.df))
names(newMixed) <- c("YEAR", "percent", "TYPE")
oldMixed <- data.frame(data.df$YEAR, (data.df$oldFromMixed*100/data.df$totalNodes))
oldMixed$TYPE <- rep("Old From Mixed", nrow(data.df))
names(oldMixed) <- c("YEAR", "percent", "TYPE")
oldNewFromPureMixed <- rbind(pureComp, mixedComp)
oldNewFromPureMixed <- rbind(oldNewFromPureMixed, newPure)
oldNewFromPureMixed <- rbind(oldNewFromPureMixed, oldPure)
oldNewFromPureMixed <- rbind(oldNewFromPureMixed, newMixed)
oldNewFromPureMixed <- rbind(oldNewFromPureMixed, oldMixed)
#create plot from csv data
p <- ggplot(oldNewFromPureMixed, aes(x=YEAR, y=percent, group=TYPE, shape=TYPE)) + geom_line(aes(linetype=TYPE, colour=TYPE)) + geom_point() + scale_linetype_manual(values=c("solid", "dashed", "dashed", "dashed","dashed","solid"))
#add annotation and save
p <- p  + opts(title = nodes.title)
p <- p + opts(axis.text.x = theme_text(face="bold", size="14"), axis.text.y = theme_text(face="bold", size="14"))
p <- p + xlab("Year") + ylab("% nodes from total network")
p <- p + ylim(0,100) + xlim(as.integer(start_year), as.integer(end_year))
summary(p)
ggsave(p, file=nodes.outpath, dpi=72)

# 4. Create plot of % of all nodes that connected to at least 1 Hub that is new in the network
nodes.outpath <- paste(outpath, field, run, "NEW_NODES_CONNECTED_TO_HUBplot.png", sep="")
nodes.title <- paste("Percent of New Nodes Connected To New or Old Hubs", field, run, sep=" ")
#make data frames
hubsTotal <- data.frame(data.df$YEAR, ((data.df$nodesToNewHubs + data.df$nodesToOldHubs)*100/ data.df$totalNew))
hubsTotal$TYPE <- rep("Total Hubs", nrow(data.df))
names(hubsTotal) <- c("YEAR", "percent", "TYPE")
hubsNew <- data.frame(data.df$YEAR, ((data.df$nodesToNewHubs)*100/ data.df$totalNew))
hubsNew$TYPE <- rep("New Hubs", nrow(data.df))
names(hubsNew) <- c("YEAR", "percent", "TYPE")
hubsOld <- data.frame(data.df$YEAR, ((data.df$nodesToOldHubs)*100/ data.df$totalNew))
hubsOld$TYPE <- rep("Old Hubs", nrow(data.df))
names(hubsOld) <- c("YEAR", "percent", "TYPE")
hubsOldNew <- rbind(hubsTotal, hubsNew)
hubsOldNew <- rbind(hubsOldNew, hubsOld)
#create plot from csv data
p <- ggplot(hubsOldNew, aes(x=YEAR, y=percent, shape=TYPE)) + geom_line(aes(linetype=TYPE, colour=TYPE)) + geom_point() + scale_linetype_manual(values=c("dashed", "dashed", "solid"))
#add annotation and save
p <- p  + opts(title = nodes.title)
p <- p + opts(axis.text.x = theme_text(face="bold", size="14"), axis.text.y = theme_text(face="bold", size="14"))
p <- p + xlab("Year") + ylab("% nodes from total network")
p <- p + ylim(0,100) + xlim(as.integer(start_year), as.integer(end_year))
summary(p)
ggsave(p, file=nodes.outpath, dpi=72)

# 5. Component view plot of Mixed, Pure, Pure New, and Pure Old components in the network
nodes.outpath <- paste(outpath, field, run, "MIXED_PURE_OLD_NEW_plot.png", sep="")
nodes.title <- paste("Percent of Mixed, Pure Old Author, and Pure New Author Components for ", field, run, sep=" ")
# make data frames
compMixed <- data.frame(data.df$YEAR, (data.df$mixedComps * 100 / data.df$totalComps))
compMixed$TYPE <- rep("Mixed Components", nrow(data.df))
names(compMixed) <- c("YEAR", "percent", "TYPE")
compPure <- data.frame(data.df$YEAR, (data.df$pureComps * 100 / data.df$totalComps))
compPure$TYPE <- rep("Pure Components", nrow(data.df))
names(compPure) <- c("YEAR", "percent", "TYPE")
compPureNew <- data.frame(data.df$YEAR, (data.df$pureNewComps * 100 / data.df$totalComps))
compPureNew$TYPE <- rep("Pure New Components", nrow(data.df))
names(compPureNew) <- c("YEAR", "percent", "TYPE")
compPureOld <- data.frame(data.df$YEAR, (data.df$pureOldComps * 100 / data.df$totalComps))
compPureOld$TYPE <- rep("Pure Old Components", nrow(data.df))
names(compPureOld) <- c("YEAR", "percent", "TYPE")
compPureMixed <- rbind(compMixed, compPure)
compPureMixed <- rbind(compPureMixed, compPureNew)
compPureMixed <- rbind(compPureMixed, compPureOld)

#create plot from csv data
p <- ggplot(compPureMixed, aes(x=YEAR, y=percent, shape=TYPE)) + geom_line(aes(linetype=TYPE, colour=TYPE)) + geom_point() + scale_linetype_manual(values=c("solid", "solid", "dashed", "dashed"))
#add annotation and save
p <- p  + opts(title = nodes.title)
p <- p + opts(axis.text.x = theme_text(face="bold", size="14"), axis.text.y = theme_text(face="bold", size="14"))
p <- p + xlab("Year") + ylab(" % of total components in graph")
p <- p + ylim(0,100) + xlim(as.integer(start_year), as.integer(end_year))
summary(p)
ggsave(p, file=nodes.outpath, dpi=72)

# 6. % of nodes in a given year that are new
nodes.outpath <- paste(outpath, field, run, "NEW_NODES_plot.png", sep="")
nodes.title <- paste("Proportion of New Nodes To Active Nodes Per Year", field, run, sep=" ")
#create plot from csv data
p <- ggplot(data.df, aes(YEAR)) + geom_line(aes(y=(totalNew/totalNodes * 100), colour="New Nodes"))
#add annotation and save
p <- p  + opts(title = nodes.title)
p <- p + opts(axis.text.x = theme_text(face="bold", size="14"), axis.text.y = theme_text(face="bold", size="14"))
p <- p + xlab("Year") + ylab(" % of total active nodes")
p <- p + ylim(0,100) + xlim(as.integer(start_year), as.integer(end_year))
summary(p)
ggsave(p, file=nodes.outpath, dpi=72)

# 7. Number of active authors in a given year
nodes.outpath <- paste(outpath, field, run, "ACTIVE_NODES_plot.png", sep="")
nodes.title <- paste("Number Of Active Nodes", field, run, sep=" ")
#create plot from csv data
p <- ggplot(data.df, aes(YEAR)) + geom_line(aes(y=totalNodes, colour="Total Nodes"))
#add annotation and save
p <- p  + opts(title = nodes.title)
p <- p + opts(axis.text.x = theme_text(face="bold", size="14"), axis.text.y = theme_text(face="bold", size="14"))
p <- p + xlab("Year") + ylab(" % of total active nodes")
p <- p + ylim(0, max(data.df$totalNodes)) + xlim(as.integer(start_year), as.integer(end_year))
summary(p)
ggsave(p, file=nodes.outpath, dpi=72)

# 8. Number of active authors in a given year normalized by maximum active authors
nodes.outpath <- paste(outpath, field, run, "ACTIVE_NODES_NORMALIZED_plot.png", sep="")
nodes.title <- paste("Number Of Active Nodes (Normalized)", field, run, sep=" ")
#create plot from csv data
p <- ggplot(data.df, aes(YEAR)) + geom_line(aes(y=(totalNodes / max(data.df$totalNodes)*100), colour="Total Nodes"))
#add annotation and save
p <- p  + opts(title = nodes.title)
p <- p + opts(axis.text.x = theme_text(face="bold", size="14"), axis.text.y = theme_text(face="bold", size="14"))
p <- p + xlab("Year") + ylab(" % of total active nodes")
p <- p + ylim(0, 100) + xlim(as.integer(start_year), as.integer(end_year))
summary(p)
ggsave(p, file=nodes.outpath, dpi=72)
q()