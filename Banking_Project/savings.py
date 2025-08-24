"""Program for Project 11
Written James D. Rodgers 7/20/2025

This file defines the SavingsAccount class - inherits from the class Account.
Savings accounts earn interest based on the balance and an interest rate.
"""

from account import Account
from decimal import Decimal

class SavingsAccount(Account):
    """
    A savings account that earns interest.
    Inherits from the Account class.
    """

    def __init__(self, name, balance, interest_rate):
        """
        Initializes a savings account with name, balance, and interest rate (Decimal).
        """
        super().__init__(name, balance) #can also utilize Account().__init__
        self.__interest_rate = Decimal(str(interest_rate))  # utilizes decimal method

    @property
    def interest_rate(self):
        """
         method to get the interest rate.
        """
        return self.__interest_rate

    def calculate_interest(self):
        """
        Returns the interest earned based on the current balance.
        """
        return Decimal(str(self.balance)) * self.__interest_rate

    def __str__(self):
        """
        Returns a formatted string with account info and interest rate.
        """
        return f"Savings Account - Name: {self.name}, Balance: ${self.balance:.2f}, Interest Rate: {self.__interest_rate:.2%}"
