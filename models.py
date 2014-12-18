#!/usr/bin/evn python
from storage import put, get_all
from settings import *

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
        put(instance)
        
    @classmethod
    def all(kls):
        return get_all(kls)

    @classmethod
    def query(kls, field_name, value):
        if field_name in kls.__dict__:
            queryset = get_all(kls)
            result = filter(lambda instance: getattr(instance, field_name) == value, queryset)
            return result
        else:
            raise 'No such field'


class User(Base):
    def __init__(self, name, balance=0):
        self.name = name
        self.balance = balance

    def get_banlance(self):
        return CURRENCY + str(self.balance / 100.0)

    @staticmethod
    def get_by_name(user_name):
        for u in User.all():
            if u.name == user_name:
                return u
        return None

        


class CreditCard(Base):
    def __init__(self, user, number):
        self.user = user
        self.number = number

    @staticmethod
    def get_by_number(card_number):
        for c in CreditCard.all():
            if c.number == card_number:
                return c
        return None
        

    @staticmethod
    def query():
        pass


class Feed(Base):
    def __init__(self, user, message):
        self.user = user
        self.message = message
        
    @staticmethod
    def get_by_user(user):
        return filter(lambda f: f.user == user,Feed.all())

class Transaction(Base):
    def __init__(self, actor, target, amount, note):
        self.actor = actor
        self.target = target
        self.amount = amount
        self.note = note

    def save(self):
        super(Transaction, self).save()
        self.target.balance += self.amount
        f1 = Feed(self.actor,  FEED_MSG['payer']%(self.target, self.amount/100.0, self.note))
        f2 = Feed(self.target, FEED_MSG['payee']%(self.actor, self.amount/100.0, self.note))
        f1.save()
        f2.save()