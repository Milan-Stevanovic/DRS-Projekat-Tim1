from flask import Blueprint, request, json, jsonify, session
import requests, flask
from requests.api import get
from werkzeug.wrappers import response

user_blueprint = Blueprint('user_blueprint', __name__)
 
from app import mysql

@user_blueprint.route('/register', methods=['POST'])
def register():
    content = flask.request.json
    mail =session.get('email')
    user = getUser(mail)

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
    
    if userExists(_email):
       retVal = {'message' : 'User already registered'}, 400
       return retVal
    
    registerUser(_name, _lastname, _email, _password, _address, _city, _country, _phoneNum, _balance, _verified, _cardNum)
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
    linkCardWithUser(_email, _cardNum, _owner, _expDate, _securityCode)
    return {'message' : 'Card linked successfully!'}, 200

@user_blueprint.route('updateProfile',methods=['POST'])
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
    
    #ista prica kao na ui dijelu   
    #_balance = content['balance']
    #_verified = content['verified']
    #_cardNum = content['cardNum']
    
    updateUser(_name, _lastname, _email, _password, _address, _city, _country, _phoneNum)
    retVal = {'message' : 'User info successfully updated'}, 200

    return retVal



# ===================================== Functions for dataBase access ====================================== 
def userExists(email: str) -> bool :
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM user WHERE email = %s", (email,))
    account = cursor.fetchone()
    cursor.close()
    if account:
        return True
    else:
        return False

def registerUser(name, lastname, email, password, address, city, country, phoneNum, balance, verified, cardNum):
    cursor = mysql.connection.cursor()
    cursor.execute(''' INSERT INTO user VALUES(NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',(name, lastname, email, password, address, city, country, phoneNum, balance, verified, cardNum))
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

# TODO KARTICA
def getCard(cardNum : str) -> dict:
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM card WHERE cardNum = %s", (cardNum,))
    card = cursor.fetchone()
    cursor.close()
    return card

def linkCardWithUser(email, cardNum, owner, expDate, securityCode):
    
    #TODO: Proveriti da li kartica sa tim brojem vec postoji u bazi podataka pre dodavanja (obrisati komentar kada je uradjeno)

    cursor = mysql.connection.cursor()
    cursor.execute(''' INSERT INTO card VALUES (%s, %s, %s, %s)''', (cardNum, owner, expDate, securityCode))
    mysql.connection.commit()
    cursor.execute(''' UPDATE user SET cardNum = %s, verified = 1, balance = -1 WHERE email = %s''', (cardNum, email))
    mysql.connection.commit()
    cursor.close()