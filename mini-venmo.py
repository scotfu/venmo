#!/usr/bin/env python
import sys
sys.path.append('.')
from models import User
from storage import Storage

if __name__ == '__main__':
    while True:
        input = sys.stdin.readline().strip().split(' ')
        if 'user' == input[0]:
            u = User(input[1])
            u.save()
            all_user = User.all()
            print type(all_user)
            print all_user
        elif 'add' == input[0]:
            pass
        elif 'pay' == input[0]:
            pass
        elif 'feed' == input[0]:
            pass
        elif 'balance' == input[0]:
            pass
        else:
            print 'ERROR: command not recognized'
        