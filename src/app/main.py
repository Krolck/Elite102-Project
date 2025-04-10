from flask import app, Flask
from getpass import getpass
from mysql.connector import connect, Error


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
    cursor.execute("CREATE DATABASE IF NOT EXISTS bank")
    cursor.execute(ACCOUNTS_QUERY)
    # cursor.execute("DESCRIBE accounts")
    connection.commit()
    cursor.close()
    return connection




def getAccount(connection, id):
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM accounts WHERE id = {id}")
    account = cursor.fetchone()
    return {  
    "ID": account[0],
    "Username" : account[1],
    "Password" : account[2],
    "Pin" : account[3],
    "Balance" : account[4]       
        }

# REMEMBER to add input sanitization 
def register(connection):
    try:
        cursor = connection.cursor()
        username = input("Register Username: ")
        password = input("Register Password: ")
        cursor.execute(f"INSERT INTO accounts ({username}, {password})")
        connection.commit()
        # cursor.execute("SELECT * FROM accounts")
        cursor.close()
    except Error as e:
        print("Please Enter Valid Credentials")
        print(e)
        register(connection)

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
    except Error as e:
        print("Incorrect credentials. Please try again.")
        print(e)
        login(connection)
        

def deposit(connection, id):
    cursor = connection.cursor()
    account = getAccount(connection, id)
    try:
        amount = float(input("How much would you like to deposit?"))
        cursor.execute(f"UPDATE accounts SET balance = balance + {amount} WHERE id = {account["ID"]}")
        connection.commit()
        cursor.close()
        account = getAccount(connection, id)
        print(f"Deposited {amount}. Your new balance is {account["Balance"]}.")
    except ValueError as e:
        print("Please Enter a valid amount")
        deposit(connection, id)

def checkBalance(connection, id):
    cursor = connection.cursor()
    account = getAccount(connection, id)
    print(account["Balance"])


def printCursor(connection):
    cursor = connection.cursor()
    for i in cursor:
        print(i)
    cursor.close()

def main():
    try:
        
        connection = initDB()

        # register(connection)

        id = login(connection)

        deposit(connection, id)
        checkBalance(connection, id)


    except Error as e:
        print(e)

if __name__ == "__main__":
   main()

    