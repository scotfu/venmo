#!/usr/bin/env python
import sys
from models import User, CreditCard, Transaction, Feed
from utils import luhn, clean_user_name, clean_amount

def add_user():
    pass

def is_user_existed(user_name):
    if user_name in [u.name for u in User.all()]:
        return True
    return False

def is_card_existed(card_number):
    if card_number in [card.card_number for card in CreditCard.all()]:
        return True
    return False

def get_user_by_name(user_name):
    for u in User.all():
        if u.name == user_name:
            return u
    return None
        
def get_feed_by_user(user):
    return filter(lambda f: f.user == user,Feed.all())


def process():
    while True:
        input = sys.stdin.readline().strip().split(' ')
        length = len(input)
        if 'user' == input[0] and length == 2:
            user_name = clean_user_name(input[1])
            if user_name:
                if is_user_existed(user_name):
                    print 'ERROR: User %s existed'% user_name
                else:
                    u = User(user_name)
                    u.save()
            else:
                print 'ERROR: invalid arguments'
        elif 'add' == input[0] and length == 3:
            user = input[1]
            card_number = input[2]
            if is_user_existed(user):
                if luhn(card_number):
                    if is_card_existed(card_number):
                        print 'Error:that card has already been added by another user, reported for fraud!'                        
                    else:
                        user = get_user_by_name(user)
                        card = CreditCard(user, card_number)
                        card.save()
                else:
                    print 'Error:this card is invalid'
            else:
                print "Error: user not exist"
        elif 'pay' == input[0]:
            if length > 4:
                actor = get_user_by_name(input[1])
                target = get_user_by_name(input[2])
                amount = input[3]
                note = ' '.join(input[4:])
                if actor and target:
                    amount = clean_amount(amount)
                    if amount:
                        t = Transaction(actor, target, amount, note)
                        t.save()
                    else:
                        print 'Error: invalid amount'
                else:
                    print 'Error: user(s) not exist'
            else:
                print 'ERROR: invalid arguments' 
        elif 'feed' == input[0]:
            if length == 2:
                user = get_user_by_name(input[1])
                if user:
                    for f in get_feed_by_user(user):
                        print f.message
        elif 'balance' == input[0]:
            if length == 2:
                user = get_user_by_name(input[1])
                if user:
                    print user.balance
        else:
            print 'ERROR: command not recognized'
            
    
if __name__ == '__main__':
    process()