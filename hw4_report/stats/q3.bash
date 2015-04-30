#!/bin/bash
j=0
for i in $(awk '{print $1}' ../../hw4_q3_ids)
do
    j=$(( $j + 1 ))
    echo -ne "\r$j"
    Rscript q3_template.R $i
done
echo -ne "\r"
