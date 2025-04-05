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
id INT PRIMARY KEY AUTO_INCREMENT,
username VARCHAR(80),
password VARCHAR(80),
pin TINYINT(5) UNSIGNED,
balance DECIMAL(65, 2)
)
"""




def initDB():
    bankdb = connect(
    host="localhost",
    # user=input("Enter username: "),
    # password=getpass("Enter password: ")
    user = 'root', # REMEMBER to change
    password = "LeoSQLDB#123", # REMEMBER to change
    database = "bank"
        ) 
    cursor = bankdb.cursor
    cursor.execute(ACCOUNTS_QUERY)
    cursor.execute("DESCRIBE accounts")
    return bankdb


database = initDB()
cursor = initDB.cursor()


# REMEMBER to add input sanitization 
def register():
    username = input("Enter Username: ")
    password = input("Enter Password: ")
    cursor.execute("INSERT INTO accounts (username, password) VALUES (%s, %s)", (username, password))
    database.commit()
    cursor.execute("SELECT * FROM accounts")

def login():
    username = input("Enter Username: ")
    password = input("Enter Password: ")
    cursor.execute("SELECT * FROM accounts WHERE username = %s AND password = %s", (username, password,))
    account = cursor.fetchone()

    if account:   
        return True, f"Successfully logged In! Hello {account.username}"
    else:
        return False, f"Incorrect Credentials. Please try again." 


def printCursor():
    for i in cursor:
        print(i)

def main():
    try:
        bankdb = initDB()
        cursor = bankdb.cursor()
        
        
        
        # register(cursor)
        while not result:
            result, output = login(cursor)
            print(output)


    except Error as e:
        print(e)

if __name__ == "__main__":
   main()

    