#!/usr/bin/env python
import re

from settings import *
from models import User, CreditCard, Transaction, Feed

"""
Utils functions

"""


def clean_user_name(user_name):
    """
    take a string as input, then determine if it is a valid user name
    return a valid user name string or None 
    """
    length = len(user_name)
    if 3 < length < 16:
        match = re.search('^[a-zA-Z\-_]*$', user_name)
        if match:
            return match.group(0)
    return None


def clean_card_number(card_number):
    """
    take a string as input, then determine if it contains a
    valid credit card number,return a string of that card number or None
    """
    if 1 < len(card_number) < 20:
        if re.search('^[0-9]*$', card_number):
            if luhn(card_number):
                return card_number
    return None    

def clean_amount(amount):
    """
    take a string as input, then determine if it is a valid amount
    digits after the second right to . will be ignored.
    return a int number in cents
    """
    if amount:
        if amount[0] == CURRENCY:
            try:
                amount = int(float(amount[1:])*100)
            except Exception,e:
                amount = None
            return amount
    return None

def format_balance(user):
    """reformat balance to float-like string """
    balance = str(user.balance)
    pre = balance[:-2] if balance[:-2] else '0'
    balance = pre + '.' + balance[-2:]
    return '$%s'%balance


def luhn(number):
    """luhn validation"""
    partial = number[:-1]
    check_digit = number[-1]
    
    even_digits = partial[-2::-2]
    odd_digits = partial[-1::-2]

    check_sum = 0
    check_sum += sum(map(int,even_digits))
    
    for digit in odd_digits:
        check_sum += sum(map(int,str(int(digit)*2)))

    if check_sum * 9 % 10 == int(check_digit):
        return True
    return False


def add_user(line):
    """Logic add a user"""
    msg  = 0
    if len(line) == 2:
        user_name = clean_user_name(line[1])
        if user_name:#valid user name
            user = User.get_by_name(user_name)
            if user:#already has a user with this name
                msg = ERROR_MSG['U_EXISTED']% user_name
            else:
                u = User(user_name)
                u.save()
        else:
            msg = ERROR_MSG['INVALID_NAME']
    else:
        msg = ERROR_MSG['INVALID_ARS']
    return msg

    
def add_card(line):
    """Logic add a card"""
    msg = 0
    if len(line) == 3:
        user_name = line[1]
        card_number = line[2]
        user = User.get_by_name(user_name)
        card1 = CreditCard.get_by_user(user)#already have a card?
        if not card1:
            card2 = CreditCard.get_by_number(card_number)#fraud card?            
            if not card2:
                if user:
                    if clean_card_number(card_number):
                        card = CreditCard(user, card_number)
                        card.save()
                    else:
                        msg = ERROR_MSG['INVALID_CARD']
                else:
                    msg = ERROR_MSG['U_NOT_EXISTED']
            else:
                msg = ERROR_MSG['FRAUD_CARD']
        else:
            msg = ERROR_MSG['U_HAS_CARD']
    else:
        msg = ERROR_MSG['INVALID_ARS']
    return msg

    
def pay(line):
    """Logic new payment"""
    msg = 0
    if len(line) > 4:
        actor = User.get_by_name(line[1])
        target = User.get_by_name(line[2])
        amount = line[3]
        note = ' '.join(line[4:])
        actor_card = CreditCard.get_by_user(actor)
        if actor_card:# actor has a card
            if actor and target:#both existed
                if actor != target:#not paying self
                    amount = clean_amount(amount)
                    if amount:#valid amount
                        t = Transaction(actor, target, amount, note)
                        t.save()
                    else:
                        msg = ERROR_MSG['INVLIAD_AMOUNT']
                else:
                    msg = ERROR_MSG['PAY_SELF']
            else:
                msg = ERROR_MSG['U_NOT_EXISTED']
        else:
            msg = ERROR_MSG['U_HAS_NO_CARD']
                
    else:
        msg = ERROR_MSG['INVALID_ARS']

    return msg

    
def feed(line):
    """Logic feed"""
    msg = 0
    if len(line) == 2:
        user = User.get_by_name(line[1])
        if user:#valid user
            msg = []
            for f in Feed.filter_by_user(user):
                msg.append(f.message)
        else:
            msg = ERROR_MSG['U_NOT_EXISTED']
    else:
        msg = ERROR_MSG['INVALID_ARS']
    if isinstance(msg,list):
        msg = '\n'.join(msg)
    return msg

    
def check_balance(line):
    msg = 0
    """Logic balance"""
    if len(line) == 2:
        user = User.get_by_name(line[1])
        if user:#valid user
            msg = format_balance(user)
        else:
            msg = ERROR_MSG['U_NOT_EXISTED']
    else:
        msg = ERROR_MSG['INVALID_ARS']          
    
    return msg

    
def process(line):
    msg = 0
    """Flow control, process one line of commands"""
    line = line.strip().split(' ')
    #print line
    if COMMAND['ADD_USER'] == line[0]:
        msg = add_user(line)
    elif COMMAND['ADD_CARD'] == line[0]:
        msg = add_card(line)
    elif COMMAND['NEW_PAYMENT'] == line[0]:
        msg = pay(line)
    elif COMMAND['FEED'] == line[0]:
        msg = feed(line)
    elif COMMAND['CHECK_BALANCE'] == line[0]:
        msg = check_balance(line)
    else:
        msg = ERROR_MSG['NOT_REC']
        
    return msg



def test_user_name():
    print clean_user_name('hi')
    print clean_user_name('hisadasd')
    print clean_user_name('hisadasdaioji-qwe-_')
    print clean_user_name('--ji-qwe-_')


def test_card_number():
    print luhn('123423423434')
    print luhn('79927398711')
    print luhn('1321232131234')
    print luhn('132123213123')    
    print luhn('79927398713')    
    
if __name__ == '__main__':
    test_card_number()