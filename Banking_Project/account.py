
"""
Project 11
Written James D. Rodgers 7/20/2025

This file defines the SavingsAccount class - inherits from Account.
Savings accounts earn interest based on the balance and an interest rate.
"""
class Account:
    """
    This class creates a bank account with a name and balance.
    """

    def __init__(self, name, balance):
        """
        Initializes the account with a name and a balance.
        """
        if balance < 0:
            raise ValueError("Account overdrawn!")
        self.__name = name
        self.__balance = balance

    @property # read only access 
    def name(self):
        """
       method to get the holder's account name.
        """
        return self.__name

    @property  #read only access
    def balance(self):
        """
        Method to get the current account balance.
        """
        return self.__balance

    def deposit(self, amount):
        """
        Adds money to the account balance.
        """
        if amount <= 0:
            print("Deposit amount must be positive")
        else:
            self.__balance += amount

    def withdraw(self, amount):
        """
        Withdraws money from the account.
        """
        if amount <= 0:
            print("Withdrawal amount must be positive")
        elif amount > self.__balance:
            print("Insufficient funds")
        else:
            self.__balance -= amount

    def __str__(self):
        """
        Returns a formatted string with account name and balance.
        """
        return f"Name: {self.__name}\nBalance: ${self.__balance:.2f}"