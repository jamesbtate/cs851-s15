#!/bin/bash
FILE=hw4_report
PDF="pdflatex $FILE"
BIB="bibtex $FILE"

$PDF
$BIB
$PDF
$PDF
