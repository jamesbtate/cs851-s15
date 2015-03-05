#brewer.pal(8, "Set1")
#barplot(stuff, col=colors)
#hist(stuff, col=colors)

library(RColorBrewer)

myData <- read.table("frequency_final_uri_multiplicity.stats")
fullData = rep(myData[,1], myData[,2])
#print(myData)
#print(myData[,1])
#print(myData[,2])

colors <- brewer.pal(8, "Dark2")
#colors <- c("brown", "lightblue", "lightgreen", "brown", "brown")
#breaks <- c(0,1,2,3,4,5)
title <- "Frequency of Final URI Multiplicity"
xlab <- "Multiplicity of URI in Sample Data"
ylab <- "Frequency of URIs with this Multiplicity"

#extend margin
# default: c(5,4,4,2) + 0.1
# bottom, left, top, right
#par(mar=c(10,4,4,2) + 0.1)

pdf("frequency_final_uri_multiplicity.pdf", height=3.8, width=6.0)

mp <- hist(fullData, col=colors, breaks=200, xlim=c(1,14.5), ylim=c(0,5200), main=title, xlab=xlab, ylab=ylab, labels=TRUE)
#axis(2)
#axis(1, at=mp, line=2, tick=FALSE, xpd=TRUE, labels=labels)
