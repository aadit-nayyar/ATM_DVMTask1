import random
import csv

'''Designing an ATM Interface
Class ATM has attribute card_list which contains the list of all the
cards registered with the service.
The class ATM has a method insert card which is invoked when a card is inserted.
It takes in the card_number and pin as arguments and gives the user an option to
withdraw money, desposit money, check account balance or exit.

The class User(a subclass of ATM) represents an user. It has the following attributes:
 - atm: the ATM service in which the user is registered
 - user_name: the name of the user
 - account_list: the list of accounts owned by the user
 - card_list: the list of cards owned by the user
This class has two methods:
 - __str__/__repr__: displays the user_name
 - new_account: creates a new account and updates the account_list of the instance

The class Account represents an account held by a user. It has the following attributes:
 - user: the user to which the account belongs(an instance of the class User)
 - accont_number: the account_number 
 - balance: the balance in the account
 - card_list: the list of cards under that account
 - atm: the atm the user of the account is registered with
The card_list of the account is also added to the card_list of the user and the atm
The class Account has the following methods:
 - __str__/__repr__: displays the account number
 - new_card: creates a new card by generating a random card number'''


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
)****************************************************************************''')

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
                return None
        print('''Card authenticated succesfully! 
****************************************************************************''')
 
        while True:
            print('''MENU:
1: Withdraw Money
2: Deposit Money
3: View Account Balance
0: Exit''')
            cont = int(input("Enter option number: "))

            if cont == 1:

                print('''Current account balance: Rs.''',this_user.account.balance)
                amount = int(input("Enter the amount you wish to withdraw: "))

                if amount>int(this_user.account.balance):
                    print('''Withdrawal amount is greater than account balance.
Transaction could not be completed...
Returnng to Home Screen...
****************************************************************************''')

                else:
                    self.update_balance(this_user,(-1)*amount)

                    print('''Transaction completed!
Final account balance: Rs.''',this_user.account.balance,'''
Retruning to Home Screen...
****************************************************************************''')


            elif cont == 2:

                print('''Current account balance: Rs.''',this_user.account.balance)
                amount=int(input("Enter the amount you wish to deposit: "))
                print('Insert cash')

                self.update_balance(this_user,amount)
                
                print('''Transaction completed!
Final account balance: Rs.''', this_user.account.balance,'''
Returning to Home Screen...
****************************************************************************''')

            elif cont == 3:
                
                print('''Current account balance: ''',this_user.account.balance,'''
Returning to Home Screen...
****************************************************************************''')

            elif cont == 0:
                print('''Thank you for visiting!
****************************************************************************''')
                return None

        

class User(ATM):

    def __init__(self,atm,user_name,account):

        self.atm = atm
        self.account = account
        self.card = account.card
        self.user_name = user_name

    def __str__(self):
        
        return self.user_name

    __repr__ = __str__

    


class Account(User):

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

class Card(Account):

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

    



atm = ATM('atm.csv')

user_name = input("Enter username: ")
atm.insert_card(user_name)

