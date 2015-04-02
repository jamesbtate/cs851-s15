library(RColorBrewer)

myData <- read.table("original_words.stats")
fullData = rep(myData[,1])

title <- "Original Word Rank vs. Word Frequency"
xlab <- "Word Rank"
ylab <- "Word Frequency"

pdf("original_words.pdf", height=4.0, width=4.5)

#extend margin
# default: c(5,4,4,2) + 0.1
# bottom, left, top, right
par(mar=c(2,2,3.0,2) + 0.1)

mp <- plot(fullData, type="l", col="blue", main=title, xlab=NA, ylab=NA, xaxt='n', yaxt='n')
mtext(side=1, xlab, line=0.5)
mtext(side=2, ylab, line=0.5)
