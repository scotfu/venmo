#!/usr/bin/evn python
from storage import put, get_all
from settings import *
"""
Model layer

Base class has provided a couple methods that talk to the storage layer to save and query instances.

Class User, CreditCard, Transaction, Feed are all based on the Base class

"""


class Base(object):

    def __int__(self, name):
        self.name = name

    def save(self):
        Base.__save(self)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    @staticmethod
    def __save(instance):
        """save an instance"""
        put(instance)
        
    @classmethod
    def all(kls):
        """get all instances of this class, return a list"""
        return get_all(kls)

    @classmethod
    def query(kls, field_name, value):
        """filter instances by one field value, return a list"""
        result = []
        queryset = get_all(kls)
        try:
            result = filter(lambda instance: getattr(instance, field_name) == value, queryset)
        except AttributeError:
            print 'No such field'
            
        return result

class User(Base):
    """
    Abstrantion of users.
    This is about money, so balance is a cent based int number to avoid precision problem of float. 
    """
    def __init__(self, name, balance=0):
        self.name = name
        self.balance = balance


    @staticmethod
    def get_by_name(name):
        """Get a user by name, return a user instance or None"""
        try:
            user = User.query('name', name)[0]
        except IndexError:
            user = None
        return user

        


class CreditCard(Base):
    """Abstration of credit cards"""
    def __init__(self, user, number):
        self.user = user
        self.number = number

    def __str__(self):
        return self.number

    def __repr__(self):
        return self.number

    @staticmethod
    def get_by_number(card_number):
        """Get a card by number, return a card instance or None"""
        try:
            card = CreditCard.query('number', card_number)[0]
        except IndexError:
            card = None
        return card
        
    @staticmethod
    def get_by_user(user):
        """Get a card by user, return a card instance or None"""        
        try:
            card = CreditCard.query('user', user)[0]
        except IndexError:
            card = None
        return card
        

class Feed(Base):
    """Abstration of feeds"""
    def __init__(self, user, message):
        self.user = user
        self.message = message

    def __str__(self):
        return self.message

    def __repr__(self):
        return self.message
        
    @staticmethod
    def filter_by_user(user):
        """Get feeds of a user, return a list"""
        return Feed.query('user', user)

class Transaction(Base):
    """Abstration of transactions"""
    def __init__(self, actor, target, amount, note):
        self.actor = actor
        self.target = target
        self.amount = amount
        self.note = note

    def __str__(self):
        return self.note

    def __repr__(self):
        return self.note

    def save(self):
        """After creating a transaction, also add two feeds"""
        super(Transaction, self).save()
        self.target.balance += self.amount
        f1 = Feed(self.actor,  FEED_MSG['payer']%(self.target, self.amount/100.0, self.note))
        f2 = Feed(self.target, FEED_MSG['payee']%(self.actor, self.amount/100.0, self.note))
        f1.save()
        f2.save()


if __name__ == '__main__':
    u1 = User('fushancong', 10001)
    u2 = User('test', 10)
    u1.save()
    u2.save()
    c1 = CreditCard(u1, '18')
    c2 = CreditCard(u2, '26')
    t1 = Transaction(u1, u2, 100, 'this a test')
    t1.save()

    