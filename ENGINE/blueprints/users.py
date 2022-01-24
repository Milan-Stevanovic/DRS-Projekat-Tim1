import random
from sqlite3 import Date
import string
from time import sleep
from flask import Blueprint, jsonify, session
import flask

user_blueprint = Blueprint('user_blueprint', __name__)
 
from app import mysql

@user_blueprint.route('/register', methods=['POST'])
def register():
    content = flask.request.json
    _name = content['name']
    _lastname = content['lastname']
    _email = content['email']
    _password = content['password']
    _address = content['address']
    _city = content['city']
    _country = content['country']
    _phoneNum = content['phoneNum']
    _balance = content['balance']
    _verified = content['verified']
    _cardNum = content['cardNum']
    _currency = content['currency']
    
    # check if user with same account num exists
    _accountNum = ''.join(random.choices(string.digits, k = 18))
    while(accountNumExists(_accountNum)):
        _accountNum = ''.join(random.choices(string.digits, k = 18))
    
    # check if user with same email exists
    if userExists(_email):
       retVal = {'message' : 'User already registered'}, 400
       return retVal
    
    registerUser(_name, _lastname, _email, _password, _address, _city, _country, _phoneNum, _balance, _verified, _cardNum, _currency, _accountNum)
    retVal = {'message' : 'User successfully registered'}, 200

    return retVal

# Added log in functionality
@user_blueprint.route('/login', methods=['POST'])
def login():
    content = flask.request.json
    _email = content['email']
    _password = content['password']

    user = getUser(_email)

    if user == None:
        retVal = {'message' : 'User with that email does not exist!'}, 400
    elif user['password'] == _password:
        retVal = {'message' : 'Logged in successfull!'}, 200
    else:
        retVal = {'message' : 'Fail: Wrong password'}, 400

    return retVal

@user_blueprint.route('/getUserFromDB', methods=['GET'])
def getUserFromDB():
    content = flask.request.json
    _email = content['email']
    return getUser(_email)

@user_blueprint.route('/getUserCardFromDB', methods=['GET'])
def getUserCardFromDB():
    content = flask.request.json
    _cardNum = content['cardNum']
    return getCard(_cardNum)

@user_blueprint.route('/checkCard', methods=['POST'])
def checkCard():
    content = flask.request.json
    _cardNum = content['cardNum']
    retVal = {'message' : 'Card successfully linked'}, 200
    card = getCard(_cardNum)
    if card is not None:
        retVal = {'message' : 'Card already linked'}, 400
    return retVal

@user_blueprint.route('/linkCard', methods=['POST', 'GET'])
def linkCard():
    content = flask.request.json
    _email = content['email']
    _cardNum = content['cardNum']
    _owner = content['owner']
    _expDate = content['expDate']
    _securityCode = content['securityCode']
    _newBalance = content['balance']
    linkCardWithUser(_email, _cardNum, _owner, _expDate, _securityCode, _newBalance)
    return {'message' : 'Card linked successfully!'}, 200

@user_blueprint.route('/updateProfile', methods = ['POST'])
def updateProfile():
    content = flask.request.json
    _name = content['name']
    _lastname = content['lastname']
    _email = content['email']
    _password = content['password']
    _address = content['address']
    _city = content['city']
    _country = content['country']
    _phoneNum = content['phoneNum']   
    
    updateUser(_name, _lastname, _email, _password, _address, _city, _country, _phoneNum)
    retVal = {'message' : 'User info successfully updated'}, 200

    return retVal

@user_blueprint.route('/addFunds', methods = ['POST'])
def addFunds():
    content = flask.request.json
    _email = content['email']
    _new_balance = content['new balance']
    _currency = content['currency']

    addFunds(_email, _new_balance, _currency)
    retVal = {'message' : 'Funds successfully added'}, 200
    return retVal

    
# ==========================================================================================================
# ===================================== Functions for dataBase access ====================================== 
# ==========================================================================================================

def userExists(email: str) -> bool :
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM user WHERE email = %s", (email,))
    account = cursor.fetchone()
    cursor.close()
    if account:
        return True
    else:
        return False

# Check if user with same account number already exists 
# We do this because account number is randomly generated and must be unique
def accountNumExists(accNum : str) -> bool:
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM user WHERE accountNum = %s", (accNum,))
    account = cursor.fetchone()
    cursor.close()
    if account:
        return True
    else:
        return False

def registerUser(name, lastname, email, password, address, city, country, phoneNum, balance, verified, cardNum, currency, accountNum):
    cursor = mysql.connection.cursor()
    cursor.execute(''' INSERT INTO user VALUES(NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',(name, lastname, email, password, address, city, country, phoneNum, balance, verified, cardNum, currency, accountNum))
    mysql.connection.commit()
    cursor.close()
    
#nisu dodata polje za balance, verified i cardNum jer sam smatrao da to ne treba da moze tako ni da se mijenja
#to cemo u nekim drugim funkcijama raditi
#email takodje korisnik ne moze da mijenja jer to ima smisla jer je ipak to neki unikatan id
def updateUser(name, lastname, email, password, address, city, country, phoneNum):
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE user SET name = %s, lastname = %s, password = %s, address = %s, city = %s, country = %s, phonNum = %s WHERE email = %s ",(name, lastname, password, address, city, country, phoneNum, email))
    mysql.connection.commit()
    cursor.close()

# Dodata funkcija koja vraca user-a na osnovu email-a
def getUser(email : str) -> dict:
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM user WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()
    return user

def getCard(cardNum : str) -> dict:
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM card WHERE cardNum = %s", (cardNum,))
    card = cursor.fetchone()
    cursor.close()
    return card

def linkCardWithUser(email : str, cardNum : str, owner : str, expDate : str, securityCode : str, balance : str):
    cursor = mysql.connection.cursor()
    cursor.execute(''' INSERT INTO card VALUES (%s, %s, %s, %s)''', (cardNum, owner, expDate, securityCode))
    cursor.execute(''' UPDATE user SET cardNum = %s, verified = 1, balance = %s WHERE email = %s''', (cardNum, balance, email))
    mysql.connection.commit()
    cursor.close()

def addFunds(email : str, new_balance : float, currency : str):
    cursor = mysql.connection.cursor()
    cursor.execute(''' UPDATE user SET balance = %s, currency = %s WHERE email = %s''', (new_balance, currency, email))
    mysql.connection.commit()
    cursor.close()
