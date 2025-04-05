from flask import app, Flask
from getpass import getpass
from mysql.connector import connect, Error


"""
TODO: 
- Set Up Account Registration
"""


if __name__ == "__main__":
    try:
        with connect(
            host="localhost",
            # user=input("Enter username: "),
            # password=getpass("Enter password: "),
             user = 'root', # Remember to change
             password = "LeoSQLDB#123", # Remember to change
             database="accounts",
        ) as connection:
            initDBQuery = "CREATE DATABASE accounts"
            with connection.cursor() as cursor:
                cursor.execute(initDBQuery)
                for db in cursor:
                    print(db)
    except Error as e:
        print(e)