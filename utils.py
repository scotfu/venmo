#!/usr/bin/env python
import re

def clean_user_name(user_name):
    """take a string as input, then determine if it is a valid user name"""
    length = len(user_name)
    if 3 < length < 17:
        match = re.search('^[a-zA-Z\-_]*$', user_name)
        if match:
            return match.group(0)
    return None


def clean_card_number(card_number):
    """take a string of numbers as input, then determine if it is a
       valid credit card number
    """
    if 1 < len(card_number) < 20:
        if luhn(card_number):
            return card_number
    return None    

def clean_amount(amount):
    if amount:
        if amount[0] == '$':
            amount = int(float(amount[1:])*100)
            return amount
    return None



def luhn(number):
    
    partial = number[:-1]
    check_digit = number[-1]
    
    even_digits = partial[-2::-2]
    odd_digits = partial[-1::-2]

    check_sum = 0
    check_sum += sum(map(int,even_digits))
    
    for digit in odd_digits:
        check_sum += sum(map(int,str(int(digit)*2)))
#    print check_sum,even_digits,odd_digits, check_sum * 9 % 10, check_digit    
    if check_sum * 9 % 10 == int(check_digit):
        return True
    return False




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