#brewer.pal(8, "Set1")
#barplot(stuff, col=colors)
#hist(stuff, col=colors)

library(RColorBrewer)

myData <- read.table("num_redirects.stats")
fullData = rep(myData[,1], myData[,2])
#print(myData)
#print(myData[,1])
#print(myData[,2])

#colors <- c("green", "yellow", "orange", "red")
#breaks <- c(200,300,400,500,600)
title <- "Frequency of Number of Redirects to Final URI"
xlab <- "Number of Redirects"

#extend margin
# default: c(5,4,4,2) + 0.1
# bottom, left, top, right
#par(mar=c(10,4,4,2) + 0.1)

pdf("num_redirects.pdf", height=3.5, width=6.8)

mp <- hist(fullData, col=heat.colors(6), main=title, xlab=xlab, labels=TRUE, right=FALSE, ylim=c(0,6000))
#axis(2)
#axis(1, at=mp, line=2, tick=FALSE, xpd=TRUE, labels=labels)
