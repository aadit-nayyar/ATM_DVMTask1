import random
import csv
import logging



class ATM:
    
    def __init__(self,data):
        
        self.ID = random.randint(10,99)
        self.user_list = []
        self.data = data
        try:
            data = open(self.data,'r')
            atm_reader = csv.reader(data)
            atm_writer = csv.writer(data)

            data.seek(0)
            for row in atm_reader:
                try:
                    card = Card(row[2],row[3])
                    account = Account(row[1],card,int(row[4]))
                    self.user_list += [User(self,row[0],account)]
                
                except IndexError:
                    pass

            data.close()

        except FileNotFoundError:
            pass

        
    def new_user(self,user_name,pin=1111,balance=10000):

        account_number = 'XX' + str(random.randint(100,999))
        card_number = random.randint(1000,9999)
        card = Card(card_number,pin)
        account = Account(account_number,card,balance)
        user = User(self,user_name,account)
         
        data = open(self.data,'a')
        atm_writer = csv.writer(data)
        atm_writer.writerow([user,account,card,pin,balance])
        data.close()

        logging.info('New user created. U: {}, A: {}, C: {}, B: {}'.format(user,account,card,balance))

        return user

    def update_balance(self,user,change):

        user.account.balance += change
        data = open(self.data,'r')
        atm_reader = csv.reader(data)
        lines = []
        for line in atm_reader:
            try:
                if line[0] == user.user_name:
                    line[4] = int(line[4]) + change
                lines.append(line)
            except IndexError:
                pass
        data.close()
        data = open(self.data, 'w')
        atm_writer = csv.writer(data)
        atm_writer.writerows(lines)
        data.close()
                
    
    def insert_card(self,user_name):

        for user in self.user_list:
            if user.user_name == user_name:
                this_user = user
                break
        else:
            print('Welcome ', user_name,'''!
Creating a new account. Please wait...''',sep='')
            
            pin = int(input("Enter pin: "))
            this_user = self.new_user(user_name,pin)
            
            print('''New account created!
Details:
User Name: ''', this_user,'''
Account Number: ''',this_user.account,'''
Card Number: ''',this_user.card,'''
Pin: ''',this_user.card.pin,'''
Balance: ''',this_user.account.balance,'''
Redirecting to Home Page...
****************************************************************************''')

        '''for card in self.card_list:
            if card.card_number == card_number:
                this_card = card
                break
        else:
            print("Card could not be found in database")
            return None'''

        print('Welcome ', user_name, '''!

****************************************************************************
       
To proceed, enter pin:''',end = '',sep='')

        number_of_attempts = 4
        pin=int(input())
        while this_user.card.pin != pin:
            pin = int(input("Invalid pin! Please try again: "))
            print("****************************************************************************")
            number_of_attempts -=1
            if number_of_attempts<1:
                print("Authentication error! Please try again later.")
                logging.info('Unsuccesful login to account of user: {}, A: {}, C: {}'.format(this_user,this_user.account,this_user.card))
                return None
        print('''Card authenticated succesfully! 
****************************************************************************''')
        logging.info('Successful login. U: {}, A: {}, C: {}'.format(this_user,this_user.account,this_user.card))

        while True:
            print('''MENU:
1: Withdraw Money
2: Deposit Money
3: View Account Balance
0: Exit''')
            cont = int(input("Enter option number: "))

            if cont == 1:

                prev=this_user.account.balance
                print('''Current account balance: Rs.''',prev)
                amount = int(input("Enter the amount you wish to withdraw: "))

                if amount>int(this_user.account.balance):
                    print('''Withdrawal amount is greater than account balance.
Transaction could not be completed...
Returnng to Home Screen...
****************************************************************************''')

                else:
                    self.update_balance(this_user,(-1)*amount)

                    logging.info('C: {} Prev Balance: {}, Amount withdrawn: {} Updated Balance: {}'.format(this_user.card,prev,amount,this_user.account.balance))

                    print('''Transaction completed!
Final account balance: Rs.''',this_user.account.balance,'''
Retruning to Home Screen...
****************************************************************************''')


            elif cont == 2:

                prev=this_user.account.balance
                print('''Current account balance: Rs.''',prev)
                amount=int(input("Enter the amount you wish to deposit: "))
                print('Insert cash')

                self.update_balance(this_user,amount)
                
                logging.info('C: {} Prev Balance: {}, Amount deposited: {} Updated Balance: {}'.format(this_user.card,prev,amount,this_user.account.balance))

                print('''Transaction completed!
Final account balance: Rs.''', this_user.account.balance,'''
Returning to Home Screen...
****************************************************************************''')

            elif cont == 3:
                
                print('''Current account balance: ''',this_user.account.balance,'''
Returning to Home Screen...
****************************************************************************''')

                logging.info('C: {}, Balance checked'.format(this_user.card))

            elif cont == 0:
                print('''Thank you for visiting!
****************************************************************************''')
                return None

        

class User():

    def __init__(self,atm,user_name,account):

        self.atm = atm
        self.account = account
        self.card = account.card
        self.user_name = user_name

    def __str__(self):
        
        return self.user_name

    __repr__ = __str__

    


class Account():

    def __init__(self,account_number,card,balance):

        self.account_number = account_number
        self.card = card
        self.balance = balance
        ##user.account_list += [self]
        ##user.card_list += card_list
        ##self.atm.card_list += card_list
        ##atm.user_list += [user]
     
    def __str__(self):
        return self.account_number

    __repr__ = __str__

    def new_card(self,pin = 1111):

        card_number = random.randint(1000,9999)
        card = Card(self,card_number,pin)
        
        print('''New Card created!
Details:
User Name:''',card.account.user.user_name,'''
Account Number:''', card.account.account_number, '''
Card Number:''', card.card_number)

        return card

class Card():

    def __init__(self,card_number,pin):

        ##self.account = account
        self.card_number = card_number
        self.pin = int(pin)
        ##self.user = account.user
        ##self.atm = account.atm
        ##account.card_list += [self]
        ##self.user.card_list += [self]
        ##self.atm.card_list += [self]

    def __str__(self):
        
        return str(self.card_number)
       
    __repr__ = __str__

    def __eq__(self,other):

        if other.isinstance(Card):
            return self.card_number == other.card_number

        return self.card_number == other


    def check_pin(self,other):

        return self.pin == int(other)

    

logging.basicConfig(filename = 'ATMlog.log', level = logging.DEBUG)

atm = ATM('atm.csv')

user_name = input("Enter username: ")
atm.insert_card(user_name)

