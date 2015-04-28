import string
import sys

def stderr(*argv):
    first = True
    for arg in argv:
        if not first:
            sys.stderr.write(' ')
        sys.stderr.write(str(arg))
        first = False
    sys.stderr.write('\n')
    sys.stderr.flush()

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

def addOrIncrementDict(d, item):
    try:
        d[item] += 1
    except KeyError:
        d[item] = 1

def printDict(d):
    sortedKeys = sorted(d)
    for key in sortedKeys:
        print(key, d[key])

def dictValuesToCount(input):
    # takes input dict with some repeated values, and generates output dict
    # with keys the being the values from input and values being the number
    # of occurences of each
    output = {}
    for key in input:
        addOrIncrementDict(output, input[key])
    return output

