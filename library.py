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
