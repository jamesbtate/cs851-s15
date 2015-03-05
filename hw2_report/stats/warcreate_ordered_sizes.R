library(RColorBrewer)

myData <- read.table("warcreate_ordered_sizes.stats")
fullData = rep(myData[,1])

title <- "Size of Successive WARCreate WARC Files"
xlab <- "Successive WARC Files"
ylab <- "Size in KB"

pdf("warcreate_ordered_sizes.pdf", height=4.0, width=4.5)

#extend margin
# default: c(5,4,4,2) + 0.1
# bottom, left, top, right
par(mar=c(2,2,3.0,2) + 0.1)

mp <- plot(fullData, type="l", col="blue", main=title, xlab=NA, ylab=NA, xaxt='n', yaxt='n')
mtext(side=1, xlab, line=0.5)
mtext(side=2, ylab, line=0.5)
