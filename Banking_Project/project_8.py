"""
Project 11
James D. Rodgers 7/20/2025

This file defines the main function for project 11. 
"""
from account import Account
from savings_account import SavingsAccount
from checking_account import CheckingAccount


def main():
  # Test Account
  account1 = Account("Rip Van Winkle", 1000)
  print("--- Account ---")
  print(f"Initial Account: {account1}")
  print(f"Account Name: {account1.name}") # Access name property directly
  account1.deposit(500)
  print(f"Balance after $500 deposit: {account1}")
  account1.withdraw(200)
  print(f"Balance after $200 withdraw: {account1}")
  print("-" * 27)

  # Test SavingsAccount
  savings_account1 = SavingsAccount("Louis Armstrong", 2000, 0.06)
  print("--- SavingsAccount Class ---")
  print(f"Initial Savings Account: {savings_account1}")
  interest_earned = savings_account1.calculate_interest()
  print(f"Interest: ${interest_earned:.2f}")
  savings_account1.deposit(interest_earned)
  print(f"After adding interest: {savings_account1}")
  print("-" * 30)

  # Test CheckingAccount
  checking_account1 = CheckingAccount("Charlie Brown", 500, 0.25)
  print("--- CheckingAccount Class ---")
  print(f"Initial Checking Account: {checking_account1}")
  checking_account1.deposit(100)
  print(f"After deposit of 100: {checking_account1}")
  checking_account1.withdraw(50)
  print(f"After withdrawal of 50: {checking_account1}")
  print("-" * 31)
  checking_account1.deposit(3000)
  print(f"After deposit of 3000: {checking_account1}")
  checking_account1.withdraw(1000)
  print(f"After withdrawal of 1000: {checking_account1}")

# ------------Call Main Function
main()

'''---------------SAMPLE RUN-----------------------
-- Account ---
Initial Account: Name: Rip Van Winkle
Balance: $1000.00
Account Name: Rip Van Winkle
Balance after $500 deposit: Name: Rip Van Winkle
Balance: $1500.00
Balance after $200 withdraw: Name: Rip Van Winkle
Balance: $1300.00
---------------------------
--- SavingsAccount Class ---
Initial Savings Account: Savings Account - Name: Louis Armstrong, Balance: $2000.00, Interest Rate: 6.00%
Interest: $120.00
After adding interest: Savings Account - Name: Louis Armstrong, Balance: $2120.00, Interest Rate: 6.00%
------------------------------
--- CheckingAccount Class ---
Initial Checking Account: Checking Account - Name: Charlie Brown, Balance: $500.00, Fee per Transaction: $0.25
After deposit of 100: Checking Account - Name: Charlie Brown, Balance: $599.75, Fee per Transaction: $0.25
After withdrawal of 50: Checking Account - Name: Charlie Brown, Balance: $549.50, Fee per Transaction: $0.25
-------------------------------
After deposit of 3000: Checking Account - Name: Charlie Brown, Balance: $3549.25, Fee per Transaction: $0.25
After withdrawal of 1000: Checking Account - Name: Charlie Brown, Balance: $2549.00, Fee per Transaction: $0.25

'''