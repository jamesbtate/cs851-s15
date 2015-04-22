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

