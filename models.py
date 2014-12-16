#!/usr/bin/evn python
import sys
sys.path.append('.')
from storage import Storage

class User:
    storage = Storage()
    def __init__(self, name, balance=0):
        self.name = name
        self.balance = balance

        
    def save(self):
        User.__save(self)
        
    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    @staticmethod
    def __save(instance):
        User.storage.put(instance)
        

        
    @staticmethod
    def all():
        return User.storage.all('User')


class CreditCard:
    storage = Storage()    
    def __int__(self, user, card_number):
        self.user = user
        self.card_number = card_number



    @staticmethod
    def query():
        pass


class Feed:
    storage = Storage()    
    def __init__(self, user, message):
        self.user = user
        self.message = message
        

class Transaction:
    storage = Storage()    
    def __init__(self, actor, target, amount, note):
        self.actor = actor
        self.target = target
        self.amount = amount
        self.note = note