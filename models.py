#!/usr/bin/evn python
from storage import put, get_all

class Basic:

    def __int__(self, name):
        self.name = name

    def save(self):
        Basic.__save(self)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    @staticmethod
    def __save(instance):
        put(instance)
        
    @classmethod
    def all(kls):
        return get_all(kls)




class User(Basic):
    def __init__(self, name, balance=0):
        self.name = name
        self.balance = balance


class CreditCard(Basic):
    def __init__(self, user, card_number):
        self.user = user
        self.card_number = card_number


    @staticmethod
    def query():
        pass


class Feed:
    def __init__(self, user, message):
        self.user = user
        self.message = message
        

class Transaction:
    def __init__(self, actor, target, amount, note):
        self.actor = actor
        self.target = target
        self.amount = amount
        self.note = note

    def save(self):
        super(Transaction, self).save(self)
        self.target.balance += amount
        f1 = Feed(self.actor, "You paid %s %f for %s "%(self.target, self.amount, self.note))
        f2 = Feed(self.target, "%s paid you %f for %s "%(self.actor, self.amount, self.note))
        f1.save()
        f2.save()