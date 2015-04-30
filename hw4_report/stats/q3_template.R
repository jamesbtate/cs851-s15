library(RColorBrewer)

args <- commandArgs(trailingOnly = TRUE)
tweetID = args[1]
inputPath <- paste("q3/", tweetID, ".stats", sep="")
outputPath <- paste("q3/", tweetID, ".pdf", sep="")
lastChar <- substr(tweetID, nchar(tweetID), nchar(tweetID))
colors <- c("blue", "red", "green", "yellow", "orange", "darkmagenta", "brown", "aquamarine2", "deeppink", "lightgreen")
index <- strtoi(lastChar)
index <- index + 1
color <- colors[index]

myData <- read.table(inputPath, sep=" ", colClasses=c("POSIXct", "numeric"))

title <- "Change in Jaccard Distance over Time"
xlab <- "Date"
ylab <- "Jaccard Distance"

pdf(outputPath, height=4.0, width=4.5)

#extend margin
# default: c(5,4,4,2) + 0.1
# bottom, left, top, right
par(mar=c(4,4,2.5,2) + 0.1)

set.seed(1)

mp <- plot(myData, type="o", col=color, main=title, xlab=xlab, ylab=ylab, xaxt="n", ylim=c(0,1))

axis.POSIXct(side=1, myData$V1, format="%Y-%m-%d")
