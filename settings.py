#!/usr/bin/env python
"""Settings"""


ERROR_MSG = {
'U_EXISTED': 'ERROR: User %s existed',
'U_NOT_EXISTED':'ERROR: user(s) not exist',
'INVALID_ARS': 'ERROR: invalid arguments',
'INVALID_CARD':'ERROR: this card is invalid',
'U_HAS_CARD': 'ERROR: this user already has a valid credit card',
'U_HAS_NO_CARD': 'ERROR: this user does not have a credit card',
'FRAUD_CARD': 'ERROR: that card has already been added by another user, reported for fraud!',
'INVLIAD_AMOUNT': 'ERROR: invalid amount',
'PAY_SELF': "ERROR: users cannot pay themselves",
'NOT_REC': 'ERROR: command not recognized',
'NO_FILE': 'ERROR: the file not exist',        
}

COMMAND = {
'ADD_USER' : 'user',
'ADD_CARD' : 'add',
'NEW_PAYMENT' : 'pay',
'FEED': 'feed',
'CHECK_BALANCE' : 'balance' ,

}


CURRENCY = '$'

FEED_MSG = {
    'payer' : "You paid %s $%.2f for %s ",
    'payee' : '%s paid you $%.2f for %s ',
    
}