from flask import app, Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from getpass import getpass 
from mysql.connector import connect, Error
from flask_bcrypt import Bcrypt

from decimal import Decimal

"""
TODO: 
- Set Up DB // Done
- Set Up CLI Account System
- Set Up Flask 
- Transfer CLI To Full Stack App with UI
"""

#// CONSTANTS
# Create accounts table query
ACCOUNTS_QUERY = """CREATE TABLE IF NOT EXISTS accounts (
id INT PRIMARY KEY AUTO_INCREMENT UNIQUE NOT NULL,
username VARCHAR(80) UNIQUE NOT NULL,
password VARCHAR(80) NOT NULL,
balance DECIMAL(65, 2) DEFAULT 0
)
"""


# Init app
loginManager = LoginManager()

app = Flask(__name__, template_folder= "../pages/templates", static_folder= "../pages/static")
app.config['SECRET_KEY'] = 'testkey'

CORS(app)
bcrypt = Bcrypt(app) 
loginManager.init_app(app)


# Maybe change DB to connection?

#// HELPER FUNCTIONS
# Create DB connection, this will be used to connect to the database 
def initDB():
    connection = connect(
    host="localhost",
    user = 'root',
    password = "LeoSQLDB#123", 
    database = "bank"
        )
    cursor = connection.cursor()
    # cursor.execute("CREATE DATABASE IF NOT EXISTS bank")
    cursor.execute(ACCOUNTS_QUERY) # Delete later
    connection.commit()
    cursor.close()
    return connection

# Only closes connections
def closeDB(connection):
    connection.cursor().close()
    connection.close()

# Commits changes to the database and closes the connection
def commitDB(connection):
    connection.commit()
    closeDB(connection)


# User data model 
class User(UserMixin):
    def __init__(self, id, username, password, balance):
        self.id = id
        self.username = username
        self.password = password
        self.balance = balance
    def get_id(self):
        return str(self.id)
        

# Home Page
@app.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    return redirect(url_for("register"))


# remember to add input sanitization 
@app.route("/register", methods = ["POST", "GET"])
def register():
    print(request.method)
    if request.method == "GET":
        return render_template("register.html")
    try:
        data = request.get_json()
        # Make sure data is valid (incase of js editing)
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({'error': 'Missing required fields'}), 400
        connection = initDB()
        username = data['username']
        password = data['password']

        cursor = connection.cursor()
        cursor.execute("INSERT INTO accounts (username, password) VALUES (%s, %s)", (username, password))
        commitDB(connection)

        return jsonify({'message': f'Successfully registered {username}'}), 201

    except Error as err:
        print(err)
        # Special error for username already taken
        if err.errno == 1062:
            return jsonify({"message": "Username Already Taken, Please Pick A New One"}), 409    
        return jsonify({"message": str(err.msg)}, err.errno)
        

@app.route("/login", methods = ["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    try:
        data = request.get_json()

        if not data or 'username' not in data or 'password' not in data:
            return jsonify({ "message": 'Missing required fields'}), 400

        username = data['username']
        password = data['password']

        connection = initDB()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM accounts WHERE username = %s AND password = %s", (username, password))
        account = cursor.fetchone() 
        closeDB(connection)
        
        # if credentials are valid, create a user object and log in
        if account:
            user = loadUser(account[0])
            login_user(user)
            return jsonify({'message': f'Successfully Logged in'}), 200
        else:
            return jsonify({ "message": f'Invalid Credentials. Please Try Again.'}), 401
            
    except Error as err:
        print(err)
        return jsonify({'message' : f"{err.errno} : {err.msg}"})
    

# Runs when the user is logged in
@loginManager.user_loader
def loadUser(id):
    connection = initDB()
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM accounts WHERE id = {id}")
    account = cursor.fetchone()
    user = User(id, account[1],  account[2], account[3])
    return user

# Runs when the user is not logged in and tries to access a protected route (return unique page later)
@loginManager.unauthorized_handler
def unauthorized():
    return jsonify({'message': "Unauthorized"}), 401

@app.route("/logout", methods = ["POST"])
@login_required
def logout():
    logout_user()
    return "Logout"

@app.route("/dashboard", methods = ["GET"])
@login_required
def dashboard():
    return render_template("dashboard.html", username = current_user.username, balance = current_user.balance)


@app.route("/unregister", methods = ["POST"])
@login_required
def unregister():
    connection = initDB()
    cursor = connection.cursor()
    # Remove user from db AND logs them out
    cursor.execute("DELETE FROM accounts WHERE id = %s", (current_user.id,))
    commitDB(connection)
    logout_user()
    return "Unregistered"
        

@app.route("/deposit", methods = ["POST"])
@login_required
def deposit():
    try:
        data = request.get_json()
        amount = Decimal("{:.2f}".format(float(data['amount'])))
        connection = initDB()
        cursor = connection.cursor()
        cursor.execute("UPDATE accounts SET balance = balance + %s WHERE id = %s", (amount, current_user.id))
        commitDB(connection)
        return jsonify({'message' : f"Deposited ${amount}.", 'balance' : amount + current_user.balance})
    except ValueError as err:
        print(err)
        return jsonify({'message' : "Please Enter a valid amount."})
    
@login_required
@app.route("/transfer", methods = ["POST"])
def transfer():
    try:
        data = request.get_json()
        print(data['username'])
        if not data or 'username' not in data or 'amount' not in data:
            return jsonify({'message': 'User does not exist', 'balance' : current_user.balance }), 400
        connection = initDB()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM accounts WHERE username = %s", (data['username'],))
        account = cursor.fetchone() 
        # Fix nesting later
        if account:
            amount = Decimal("{:.2f}".format(float(data['amount'])))
            if amount > current_user.balance:
                return jsonify({'message' : f"You only have {current_user.balance}. You can't transfer {amount}!",'balance' : current_user.balance })
            # Update balances
            cursor.execute("UPDATE accounts SET balance = balance - %s WHERE id = %s", (amount, current_user.id))
            cursor.execute("UPDATE accounts SET balance = balance + %s WHERE id = %s", (amount, account[0]))
            commitDB(connection)
            return jsonify({'message' : f"Transferred ${amount} to {data['username']}. Your new balance is ${current_user.balance - amount}.", 'balance' :  current_user.balance - amount})
        else:
            return jsonify({ "message": f'Invalid Credentials. Please Try Again.'}), 401        
    except Error as err:
        print(err)
        return jsonify({'message' : f"{err.errno} : {err.msg}"})


    
@app.route("/withdraw", methods = ["POST"])
@login_required
def withdraw():
    connection = initDB()
    cursor = connection.cursor()
    try:
        data = request.get_json()
        # Makes decimal to 2 decimal places
        amount = Decimal("{:.2f}".format(float(data['amount'])))
        if amount > current_user.balance:
            return jsonify({'message' : f"You only have {current_user.balance}. You can't withdraw {amount}!",'balance' : current_user.balance })
        cursor.execute("UPDATE accounts SET balance = balance - %s WHERE id = %s", (amount, current_user.id))
        closeDB(connection)
        return jsonify({'message' : f"Withdrew ${amount}. Your new balance is ${current_user.balance}.", 'balance' :  current_user.balance - amount})
    except ValueError as err:
        jsonify({'message' : "Please Enter a valid amount"})

# change username and password
@app.route("/username", methods = ["POST"])
@login_required
def changeUsername():
    try:
        data = request.get_json()
        print(data)
        connection = initDB()
        cursor = connection.cursor()
        cursor.execute("UPDATE accounts SET username = %s WHERE id = %s", (data['value'], current_user.id))
        commitDB(connection)
        return jsonify({'message' : f"Username changed to {data['value']}"})
    except Exception as err:
        print(err)
        if err.errno == 1062:
            return jsonify({"message": "Username Already Taken, Please Pick A New One"}), 409
        return jsonify({'message' : f"{err.errno} : {err.msg}"})

@app.route("/password", methods = ["POST"])
@login_required
def changePassword():
    try:
        data = request.get_json()
        connection = initDB()
        cursor = connection.cursor()
        cursor.execute("UPDATE accounts SET password = %s WHERE id = %s", (data['value'], current_user.id))
        commitDB(connection)
        return jsonify({'message' : f"Password changed to {data['value']}"})
    except Error as err:
        print(err)
        return jsonify({'message' : f"{err.errno} : {err.msg}"})

# maybe production server later?
# Main Entry Point 
if __name__ == "__main__":
    try:
        app.run(debug=True)
    except Error as e:
        print(e)

    