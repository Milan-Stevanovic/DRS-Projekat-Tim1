from flask import Blueprint, request, json, jsonify
import requests, flask

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
    
    if userExists(_email):
       retVal = {'message' : 'User already registered'}
       return retVal
    
    registerUser(_name, _lastname, _email, _password, _address, _city, _country, _phoneNum, _balance, _verified, _cardNum)
    retVal = {'message' : 'User successfully registered'}

    return retVal

def userExists(email: str) -> bool :
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM user WHERE email = %s", (email,))
    account = cursor.fetchone()
    if account:
        cursor.close()
        return True
    else:
        return False

def registerUser(name, lastname, email, password, address, city, country, phoneNum, balance, verified, cardNum):
    cursor = mysql.connection.cursor()
    cursor.execute(''' INSERT INTO user VALUES(NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',(name, lastname, email, password, address, city, country, phoneNum, balance, verified, cardNum))
    mysql.connection.commit()
    cursor.close()
