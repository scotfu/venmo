#!/usr/bin/evn python
import unittest
import random

from utils import *
from models import *
from settings import *
from storage import destory

class UserTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_user_name_numeric(self):
        invalid_names = ['fsc1', 'fsc2-', '123f', '12']
        for name in invalid_names:
            self.assertEqual(clean_user_name(name), None)
            
    def test_user_name_length(self):
        invalid_names = ['', '', 'f-_', '---','-'*17, '_'*16]
        for name in invalid_names:
            self.assertEqual(clean_user_name(name), None)
            
    def test_valid_user_name(self):
        valid_names = ['fusasd','asdasd-','--asdA']
        for name in valid_names:
            self.assertEqual(clean_user_name(name), name)            

    def test_add_user(self):
        command_pre = 'user '
        valid_names = ['fushancong','test-','sdsd']
        commands = [command_pre + name for name in valid_names]

        for i in range(len(commands)):
            line = commands[i].strip().split(' ')
            self.assertEqual(add_user(line), 0)
            self.assertEqual(User.get_by_name(line[1]).name, line[1])
            self.assertEqual(User.get_by_name(line[1]).balance, 0)

        #these users existed    
        for i in range(len(commands)):
            line = commands[i].strip().split(' ')
            self.assertEqual(add_user(line), ERROR_MSG['U_EXISTED']%line[1])

        #invalid names    
        invalid_names = ['fushancong1','st-','-1-a']
        commands = [command_pre + name for name in invalid_names]
        for i in range(len(commands)):
            line = commands[i].strip().split(' ')
            self.assertEqual(add_user(line), ERROR_MSG['INVALID_NAME'])
            
    def tearDown(self):
        destory()

class CardTest(unittest.TestCase):

    def setUp(self):
        """setting up a few users"""
        command_pre = 'user '
        valid_names = ['fushancong','test-','sdsd','testname']
        commands = [command_pre + name for name in valid_names]
        for i in range(len(commands)):
            line = commands[i].strip().split(' ')
            add_user(line)

    def test_card_alpha(self):
        invalid_cards = [' ', '2323f', '17a', 'c22','ac']
        for card in invalid_cards:
            self.assertEqual(clean_card_number(card), None)
            
    def test_card_length(self):
        invalid_cards = ['1','1'*20]
        for card in invalid_cards:
            self.assertEqual(clean_card_number(card), None)

    def test_valid_cards(self):
        valid_cards = ['6011177342413465',
                       '6011712952319295',
                       '6011594835409125',
                       '3096928175041657',
                       '3096824428708855',
                       '3528676549755779',
                       '5595487589761914',
                       '5440406551713064']

        for card in valid_cards:
            self.assertEqual(clean_card_number(card), card)            

    def test_add_card(self):
        command_pre = 'add '
        valid_names = ['fushancong','test-','sdsd']
        valid_cards = ['6011594835409125',
                       '3096928175041657',
                       '3096824428708855',]
        
        for i in range(len(valid_names)):
            line = command_pre + valid_names[i] + ' ' + valid_cards[i]
            line = line.strip().split(' ')            
            self.assertEqual(add_card(line), 0)
            
        #a user can not have more than one card    
        for i in range(len(valid_names)):
            line = command_pre + valid_names[i] + ' ' + valid_cards[-i]
            line = line.strip().split(' ')            
            self.assertEqual(add_card(line), ERROR_MSG['U_HAS_CARD'])


        #card alread added, fraud
        line = command_pre + 'testname' + ' ' + valid_cards[0]
        line = line.strip().split(' ')
        self.assertEqual(add_card(line), ERROR_MSG['FRAUD_CARD'])

    def tearDown(self):
        destory()

class PaymentTest(unittest.TestCase):

    def setUp(self):
        """setting up a few users and cards"""
        command_pre = 'user '
        valid_names = ['fushancong','test-','sdsd','testname']
        commands = [command_pre + name for name in valid_names]
        for i in range(len(commands)):
            line = commands[i].strip().split(' ')
            add_user(line)
        
        command_pre = 'add '
        valid_cards = ['6011594835409125',
                       '3096928175041657',
                       '3096824428708855',]
        for i in range(len(valid_names)-1):
            line = command_pre + valid_names[i] + ' ' + valid_cards[i]
            line = line.strip().split(' ')            
            add_card(line)

    def test_pay_self(self):
        line = 'pay fushancong fushancong $10.01 pay myself hahaha'
        line = line.strip().split(' ')        
        self.assertEqual(pay(line), ERROR_MSG['PAY_SELF'])
        
    def test_pay_without_a_card(self):
        line = 'pay testname fushancong $10.01 pay myself hahaha'
        line = line.strip().split(' ')        
        self.assertEqual(pay(line), ERROR_MSG['U_HAS_NO_CARD'])
        
    def test_amount(self):
        valid_amounts = ['$1000000','$0000000.1','$10.000000001']
        invalid_amounts = ['$1000000a','1$0000000.1','10.000000001']
        self.assertEqual(clean_amount(valid_amounts[0]), 100000000)
        self.assertEqual(clean_amount(valid_amounts[1]), 10)
        self.assertEqual(clean_amount(valid_amounts[2]), 1000)        
        for amount in invalid_amounts:
            self.assertEqual(clean_amount(amount), None)
        
    def test_pay(self):
        valid_names = ['fushancong','test-','sdsd','testname']
        command_pre = 'pay '
        notes =['haha','this is a test', 'pay for subway', 'who is lucas']
        for name in valid_names[1:]:
            line = command_pre + 'fushancong ' + name + ' $10.01 ' + random.sample(notes, 1)[0]
            line = line.strip().split(' ')
            self.assertEqual(pay(line), 0)

    def tearDown(self):
        destory()        

class FeedTest(unittest.TestCase):
    def setUp(self):
        """setting up a few users and cards, then make a few payments """
        command_pre = 'user '
        valid_names = ['fushancong','test-','sdsd','testname']
        commands = [command_pre + name for name in valid_names]
        for i in range(len(commands)):
            line = commands[i].strip().split(' ')
            add_user(line)
        
        command_pre = 'add '
        valid_cards = ['6011594835409125',
                       '3096928175041657',
                       '3096824428708855',]
        for i in range(len(valid_names)-1):
            line = command_pre + valid_names[i] + ' ' + valid_cards[i]
            line = line.strip().split(' ')            
            add_card(line)
        
        command_pre = 'pay '
        for name in valid_names:
            line = command_pre + 'fushancong ' + name + ' $10.01 ' + 'test'
            line = line.strip().split(' ')
            pay(line)
        for name in valid_names:
            line = command_pre + 'test- ' + name + ' $0.01 ' + 'who is lucas'
            line = line.strip().split(' ')
            pay(line)


    def test_feed(self):
        valid_names = ['fushancong','test-','sdsd','testname']
        line = 'feed fushancong'
        line = line.strip().split(' ')
        f1 = feed(line).split('\n')
        msg1 = []
        for i in range(1,len(valid_names)):
            msg1.append('You paid %s $10.01 for test'%valid_names[i])
        msg1.append('test- paid you $0.01 for who is lucas')
        f1.sort()
        msg1.sort()
        self.assertEqual(f1, msg1)

    def tearDown(self):
        destory()
        
if __name__ == '__main__':
    unittest.main()