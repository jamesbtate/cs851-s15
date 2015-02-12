#brewer.pal(8, "Set1")
#barplot(stuff, col=colors)
#hist(stuff, col=colors)

library(RColorBrewer)

myData <- read.table("http_status_codes.stats")
fullData = rep(myData[,1], myData[,2])
#print(myData)
#print(myData[,1])
#print(myData[,2])

colors <- c("green", "yellow", "orange", "red")
breaks <- c(200,300,400,500,600)
title <- "Frequency of HTTP Status Codes"
xlab <- "Status Code"

#extend margin
# default: c(5,4,4,2) + 0.1
# bottom, left, top, right
#par(mar=c(10,4,4,2) + 0.1)

pdf("http_status_codes.pdf", height=4.0, width=3.5)

mp <- hist(fullData, col=colors, breaks=breaks, main=title, xlab=xlab, labels=TRUE, right=FALSE, ylim=c(0,21000))
#axis(2)
#axis(1, at=mp, line=2, tick=FALSE, xpd=TRUE, labels=labels)
