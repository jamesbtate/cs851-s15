#brewer.pal(8, "Set1")
#barplot(stuff, col=colors)
#hist(stuff, col=colors)

library(RColorBrewer)

myData <- read.table("frequency_initial_uri_multiplicity.stats")
fullData = rep(myData[,1], myData[,2])
#print(myData)
#print(myData[,1])
#print(myData[,2])

colors <- brewer.pal(8, "Pastel1")
#colors <- c("brown", "lightblue", "lightgreen", "brown", "brown")
breaks <- c(0,1,2,5,10,20,50,100,200)
title <- "Frequency of Initial URI Multiplicity"
xlab <- "Multiplicity of URI in Sample Data"
ylab <- "Frequency of URIs with this Multiplicity"

#extend margin
# default: c(5,4,4,2) + 0.1
# bottom, left, top, right
par(mar=c(10,4,4,2) + 0.1)

pdf("frequency_initial_uri_multiplicity.pdf")

mp <- hist(fullData, col=colors, main=title, breaks=200, xlim=c(1,15), xlab=xlab, ylab=ylab, labels=TRUE)
#axis(2)
#axis(1, at=mp, line=2, tick=FALSE, xpd=TRUE, labels=labels)
