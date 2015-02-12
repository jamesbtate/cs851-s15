#brewer.pal(8, "Set1")
#barplot(stuff, col=colors)
#hist(stuff, col=colors)

library(RColorBrewer)

myData <- read.table("uris_per_tweet.stats")
fullData = rep(myData[,1], myData[,2])
#print(myData)
#print(myData[,1])
#print(myData[,2])

colors <- brewer.pal(5, "Set2")
colors <- c("brown", "lightblue", "lightgreen", "brown", "brown")
breaks <- c(1,2,3,4,5,6)
title <- "Frequency of URIs-per-Tweet Quantity"
xlab <- "Quantity of URIs in Tweet"
ylab <- "Frequency of Tweets with this many URIs"

#extend margin
# default: c(5,4,4,2) + 0.1
# bottom, left, top, right
#par(mar=c(10,4,4,2) + 0.1)

pdf("uris_per_tweet.pdf", height=4.0, width=4.1)

mp <- hist(fullData, col=colors, breaks=breaks, main=title, xlab=xlab, ylab=ylab, labels=TRUE, right=FALSE, ylim=c(0,10000))
#axis(2)
#axis(1, at=mp, line=2, tick=FALSE, xpd=TRUE, labels=labels)
