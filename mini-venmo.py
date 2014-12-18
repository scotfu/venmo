#!/usr/bin/env python
import sys
import os

from models import User, CreditCard, Transaction, Feed
from utils import luhn, clean_user_name, clean_amount, display_balance
from settings import *

def add_user(line):
    """Logic add a user"""
    if len(line) == 2:
        user_name = clean_user_name(line[1])
        user = User.get_by_name(user_name)
        if user:
            print ERROR_MSG['U_EXISTED']% user_name
        else:
            u = User(user_name)
            u.save()
    else:
        print ERROR_MSG['INVALID_ARS']
    

def add_card(line):
    """Logic add a card"""    
    if len(line) == 3:
        user_name = line[1]
        card_number = line[2]
        user = User.get_by_name(user_name)
        card1 = CreditCard.get_by_user(user)#already have a card?
        if not card1:
            card2 = CreditCard.get_by_number(card_number)#fraud card?            
            if not card2:
                if user:
                    if luhn(card_number):
                        card = CreditCard(user, card_number)
                        card.save()
                    else:
                        print ERROR_MSG['INVALID_CARD']
                else:
                    print ERROR_MSG['U_NOT_EXISTED']
            else:
                print ERROR_MSG['FRAUD_CARD']
        else:
            print ERROR_MSG['U_HAS_CARD']
    else:
        print ERROR_MSG['INVALID_ARS']
        
def pay(line):
    """Logic new payment"""    
    if len(line) > 4:
        actor = User.get_by_name(line[1])
        target = User.get_by_name(line[2])
        amount = line[3]
        note = ' '.join(line[4:])
        actor_card = CreditCard.get_by_user(actor)
        if actor_card:
            if actor and target:
                if actor != target:
                    amount = clean_amount(amount)
                    if amount:
                        t = Transaction(actor, target, amount, note)
                        t.save()
                    else:
                        print ERROR_MSG['INVLIAD_AMOUNT']
                else:
                    print ERROR_MSG['PAY_SELF']
            else:
                print ERROR_MSG['U_NOT_EXISTED']
        else:
            print ERROR_MSG['U_HAS_NO_CARD']
                
    else:
        print ERROR_MSG['INVALID_ARS']

def feed(line):
    """Logic feed"""
    if len(line) == 2:
        user = User.get_by_name(line[1])
        if user:
            for f in Feed.filter_by_user(user):
                print f.message
        else:
            print ERROR_MSG['U_NOT_EXISTED']
    else:
        print ERROR_MSG['INVALID_ARS']   

def check_balance(line):
    """Logic balance"""
    if len(line) == 2:
        user = User.get_by_name(line[1])
        if user:
            display_balance(user)
        else:
            print ERROR_MSG['U_NOT_EXISTED']
    else:
        print ERROR_MSG['INVALID_ARS']          
    
        
def process(line):
    """Flow control"""
    line = line.strip().split(' ')
    #print line
    if COMMAND['ADD_USER'] == line[0]:
        add_user(line)
    elif COMMAND['ADD_CARD'] == line[0]:
        add_card(line)
    elif COMMAND['NEW_PAYMENT'] == line[0]:
        pay(line)
    elif COMMAND['FEED'] == line[0]:
        feed(line)
    elif COMMAND['CHECK_BALANCE'] == line[0]:
        check_balance(line)
    else:
        print ERROR_MSG['NOT_REC']
            
    
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
                    process(line)
        else:
            print ERROR_MSG['NO_FILE']
    else:
        while True:
            process(sys.stdin.readline())
        
    