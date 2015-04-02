#!/bin/bash
FILE=hw3_report
PDF="pdflatex $FILE"
BIB="bibtex $FILE"

$PDF
$BIB
$PDF
$PDF
