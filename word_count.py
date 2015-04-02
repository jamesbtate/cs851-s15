#!/usr/bin/python3
from library import *
import statistics
import operator
import argparse
import string
import math
import sys
import re

def parseArgs():
    desc = "Count number of instances of each word in input file."
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('inputfile', metavar='input-file', help="File with words to be counted.")
    parser.add_argument('-t', '--top', type=int, metavar="N", help="Only print top N words by frequency. Default: all")
    parser.add_argument('-l', '--letters', action='store_true', help='Exclude all characters except letters and \' or - immediately after a letter.')
    args = parser.parse_args()
    return args

def addOrIncrementDict(d, item):
    try:
        d[item] += 1
    except KeyError:
        d[item] = 1

def printDict(d):
    sortedKeys = sorted(d)
    for key in sortedKeys:
        print(key, d[key])

def sortDictByValue(d, reverse=False):
    sortedDict = sorted(d.items(), key=operator.itemgetter(1), reverse=reverse)
    return sortedDict

def dictValuesToCount(input):
    # takes input dict with some repeated values, and generates output dict
    # with keys the being the values from input and values being the number
    # of occurences of each
    output = {}
    for key in input:
        addOrIncrementDict(output, input[key])
    return output

def extractWords(s):
    valid_characters = string.ascii_letters
    valid_following_character = "'-"
    letters = []
    for letter in s:
        if letter in valid_characters:
            letters.append(letter)
        elif len(letters) > 0 and \
            letter in valid_following_character and \
            letters[-1] in valid_characters:
            letters.append(letter)
        elif len(letters) > 0 and letters[-1] != ' ':
            letters.append(' ')
    return ''.join(letters)

if __name__ == '__main__':
    args = parseArgs()
    inputFile = open(args.inputfile, 'r', encoding='latin-1')
    words = {}
    count = 1
    for line in inputFile:
        sys.stderr.write('\rProcessing line ' + str(count))
        count += 1
        if args.letters: line = extractWords(line)
        terms = line.split()
        for term in terms:
            term = term.lower()
            addOrIncrementDict(words, term)
    stderr("\n" + "Sorting words list...")
    n = 999999999999
    if args.top: n = args.top
    sortedWords = sortDictByValue(words, reverse=True)
    i = 0
    for word in sortedWords:
        print(word[0], word[1])
        i+=1
        if i>= n: break
