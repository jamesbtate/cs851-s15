#!/usr/bin/env python3
from library import *
import threading
import requests
import operator
import json
import time
import sys
import os

if __name__=='__main__':
    counts = {}   
    with open('memento_list', 'r') as mementosFile:
        for line in mementosFile:
            line = line.strip()
            addOrIncrementDict(counts, line[10:28])
    printDict(counts)
