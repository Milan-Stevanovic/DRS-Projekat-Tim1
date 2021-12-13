from flask import Blueprint, request

user_blueprint = Blueprint('user_blueprint', __name__)
 
from app import mysql

@user_blueprint.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    lastname = request.form['lastname']
    email = request.form['email']
    password = request.form['password']
    address = request.form['address']
    city = request.form['city']
    country = request.form['country']
    phoneNum = request.form['phoneNum']
    balance = "0"
    verified = "False"
    cardNum = "-1"
    
    # TODO: check if user with the same ID/email is already registered
    cursor = mysql.connection.cursor()
    cursor.execute(''' INSERT INTO user VALUES(NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',(name, lastname, email, password, address, city, country, phoneNum, balance, verified, cardNum))
    mysql.connection.commit()
    cursor.close()
    return "USER REGISTERED"
