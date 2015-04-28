library(RColorBrewer)

myData <- read.table("memento_counts.stats")
fullData = rep(myData[,1])

title <- "CDF of Number of Mementos per URI"
xlab <- "Number of Mementos"
ylab <- "Probability"

pdf("memento_counts.pdf", height=4.0, width=4.5)

#extend margin
# default: c(5,4,4,2) + 0.1
# bottom, left, top, right
par(mar=c(4,4,2.5,2) + 0.1)

set.seed(1)
mp <- plot(fullData, 1:length(fullData), type="l", col="red", main=title, xlab=xlab, ylab=ylab, yaxt="n")
#mp <- plot(fullData, type="l", col="red", main=title, xlab=NA, ylab=NA, xaxt='n', yaxt='n')
#mtext(side=1, xlab, line=0.5)
axis(side=2, at=seq(1,2735,length.out=5), labels=seq(0.2,1,by=0.2))
