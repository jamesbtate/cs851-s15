#brewer.pal(8, "Set1")
#barplot(stuff, col=colors)
#hist(stuff, col=colors)

library(RColorBrewer)

myData <- read.table("time_deltas.stats")
#divide first column by 86400 to changes seconds->days
data1 <- myData[,1] / 86400.0
fullData = rep(data1, myData[,2])

colors <- brewer.pal(5, "Set3")
breaks <- 9
title <- "Frequency of URL Age"
xlab <- "URL Age in Days"
#ylab <- "s"

#extend margin
# default: c(5,4,4,2) + 0.1
# bottom, left, top, right
#par(mar=c(10,4,4,2) + 0.1)

pdf("time_deltas.pdf", height=4.0, width=4.5)

mp <- hist(fullData, breaks=breaks, col=colors, main=title, xlab=xlab, labels=TRUE, ylim=c(0,10000))
#axis(2)
#axis(1, at=mp, line=2, tick=FALSE, xpd=TRUE, labels=labels)
