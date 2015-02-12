#brewer.pal(8, "Set1")
#barplot(stuff, col=colors)
#hist(stuff, col=colors)

library(RColorBrewer)

myData <- read.table("unique_and_dupe.stats", skip=1)
labels <- c("Number of\nunique\nt.co URIs", "Number of\nunique\nfinal URIs", "Number of\nt.co URIs\n present\nmultiple times", "Number of\nfinal URIs\npresent\nmultiple times")

colors <- brewer.pal(length(labels), "Set1")

#extend margin
# default: c(5,4,4,2) + 0.1
# bottom, left, top, right
par(mar=c(10,4,4,2) + 0.1)

pdf("unique_and_dupe.pdf")

mp <- barplot(unlist(myData), col=colors, names.arg=c("","","",""), axes=FALSE)
axis(2)
axis(1, at=mp, line=2, tick=FALSE, xpd=TRUE, labels=labels)
