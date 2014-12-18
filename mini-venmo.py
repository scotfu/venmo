#!/usr/bin/env python
import sys
import os


from utils import *
from settings import *
    
if __name__ == '__main__':
    """
    entry point
    If a file name is serverd, run in file mode,
    else enter into intercative mode, take input from stdin
    """
    if len(sys.argv) == 2:
        file_name = sys.argv[1]
        if os.path.isfile(file_name):
            with open(file_name) as f:
                for line in f:
                    msg = process(line)
                    if msg:
                        print msg
        else:
            print ERROR_MSG['NO_FILE']
    else:
        while True:
            msg = process(sys.stdin.readline())
            if msg:
                print msg
        
    