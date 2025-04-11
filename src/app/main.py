from flask import app, Flask
from getpass import getpass
from mysql.connector import connect, Error
import mysql

import mysql.connector
import mysql.connector.errorcode
import mysql.vendor

import mysql.vendor.plugin


"""
TODO: 
- Set Up DB // Done
- Set Up CLI Account System
- Set Up Flask 
- Transfer CLI To Full Stack App with UI
"""

# Constants
ACCOUNTS_QUERY = """CREATE TABLE IF NOT EXISTS accounts (
id INT PRIMARY KEY AUTO_INCREMENT UNIQUE NOT NULL,
username VARCHAR(80) UNIQUE NOT NULL,
password VARCHAR(80) NOT NULL,
pin TINYINT(5) UNSIGNED,
balance DECIMAL(65, 2) DEFAULT 0
)
"""




def initDB():
    connection = connect(
    host="localhost",
    # user=input("Enter username: "),
    # password=getpass("Enter password: ")
    user = 'root', # REMEMBER to change to user input later
    password = "LeoSQLDB#123", # REMEMBER to change to get pass later
    database = "bank"
        )
    cursor = connection.cursor()
    # cursor.execute("CREATE DATABASE IF NOT EXISTS bank")
    cursor.execute(ACCOUNTS_QUERY)
    # cursor.execute("DESCRIBE accounts")
    connection.commit()
    cursor.close()
    return connection




def getAccount(connection, id): 
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM accounts WHERE id = {id}")
    account = cursor.fetchone()
    cursor.close()
    return {  
    "ID": account[0],
    "Username" : account[1],
    "Password" : account[2],
    "Pin" : account[3],
    "Balance" : account[4]       
        }

# REMEMBER to add input sanitization 
def register(connection): # change to "createAccount" later 
    try:

        cursor = connection.cursor()
        username = input("Register Username: ")
        password = input("Register Password: ")
        cursor.execute("INSERT INTO accounts (username, password) VALUES (%s, %s)", (username, password))
        connection.commit()
        # cursor.execute("SELECT * FROM accounts")
        cursor.close()
        print(f"Registed {username}")
    except Error as err:
        
        if err.errno == 1062:
            print("Sorry, this username is taken. Please try a new one.")
            register(connection)
        print(err)

def unregister(connection, id): # change to "deleteAccount" later
    account = getAccount(connection, id)
    confirm = str.lower(input(f"Are you sure you want to delete {account["Username"]}"))
    if confirm == "yes":
        cursor = connection.cursor()
        cursor.execute("DELETE FROM accounts WHERE id = %s", (account["ID"],))
        connection.commit()
        cursor.close()
        print(f"Unregistered {account["Username"]}")
        



def login(connection):
    cursor = connection.cursor()
    try:
        username = input("Enter Username: ")
        password = input("Enter Password: ")
        cursor.execute("SELECT * FROM accounts WHERE username = %s AND password = %s", (username, password))
        account = cursor.fetchone()
        cursor.close()
        
        if account:
            print(f"Successfully logged In! Hello {account[1]}")
            return account[0]
        else:
            print("Incorrect credentials. Please try again.")
            login(connection)
    except Error as err:
        print("Incorrect credentials. Please try again.")
        print(err)
        login(connection)
        



def deposit(connection, id):
    cursor = connection.cursor()
    account = getAccount(connection, id)
    try:
        amount = float(input("How much would you like to deposit?"))
        cursor.execute("UPDATE accounts SET balance = balance + %s WHERE id = %s", (amount, account["ID"]))
        connection.commit()
        cursor.close()
        account = getAccount(connection, id)
        print(f"Deposited {amount}. Your new balance is {account["Balance"]}.")
    except ValueError as err:
        print("Please Enter a valid amount")
        deposit(connection, id)

def withdraw(connection, id):
    cursor = connection.cursor()
    account = getAccount(connection, id)
    try:
        amount = float(input("How much would you like to withdraw?"))
        if amount > account["Balance"]:
            print(f"You only have {account["Balance"]}. You can't withdraw {amount}!")
            return
        cursor.execute("UPDATE accounts SET balance = balance - %s WHERE id = %s", (amount, account["ID"]))
        connection.commit()
        cursor.close()
        account = getAccount(connection, id)
        print(f"Withdrew {amount}. Your new balance is {account["Balance"]}.")
    except ValueError as err:
        print("Please Enter a valid amount")

def modify(connection, id):
    cursor = connection.cursor()
    account = getAccount(connection, id)
    mod = str.lower(input("What would you like the modify"))
    match mod:
        case "username":
            username = input("What would you like your new username to be? ")
            cursor.execute("UPDATE accounts SET username = %s WHERE id = %s", (username, account["ID"] ))
            print("Username changed")
        case "password":
            password = input("What would you like your new password to be? ")
            cursor.execute("UPDATE accounts SET password = %s WHERE id = %s", (password, account["ID"]))
            print("Password changed")
        case _:
            print("Invalid Answer")

def checkBalance(connection, id):
    account = getAccount(connection, id)
    print(f"Your balance is: {account["Balance"]}.")


def printCursor(connection):
    cursor = connection.cursor()
    for i in cursor:
        print(i)
    cursor.close()



def main():
    try:
        
        connection = initDB()
        id = None
        while True:
            action = str.lower(input("What would you like to do?"))
            match action:
                case "register":
                    register(connection)
                case "unregister":
                    unregister(connection, id)
                case "login":
                    id = login(connection)
                case "deposit":
                    deposit(connection, id)
                case "check":
                    checkBalance(connection, id)
                case "withdraw":
                    withdraw(connection, id)
                case _:
                    print("Invalid Answer")
                

    except Error as e:
        print(e)

if __name__ == "__main__":
   main()

    