#!/bin/bash
#\begin{figure}[H]
#    \centering
#    \includegraphics{stats/memento_counts_nonzero.pdf}
#    \caption{Change in Jaccard Distance over Time for URI
#\end{figure}
for i in $(ls stats/q3/*.pdf)
do
    f=$(basename $i)
    id=${f:0:18}
    string='\\begin{figure}[H]\n    \\centering\n    \\includegraphics{stats/q3/'$id'.pdf}\n    \\caption{Change in Jaccard Distance over Time for URI '$id'}\n\\end{figure}\n'
    echo -e "$string"
done
