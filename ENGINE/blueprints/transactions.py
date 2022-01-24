from multiprocessing import Queue
from sqlite3 import Date
import threading
from time import sleep
from flask import Blueprint, jsonify
import flask
import MySQLdb
from app import mysql
from models.transaction import Transaction

queue = Queue()

transaction_blueprint = Blueprint('transaction_blueprint', __name__)

@transaction_blueprint.route('/initTransaction', methods = ['POST'])
def initTransaction():
    content = flask.request.json
    _id = getLastTransactionIndex()
    _sender = content['sender']
    _receiver = content['receiver']
    _amount = content['amount']
    _transactionCurrecny = content['transactionCurrency']
    _date = content['date']
    _state = content['state']
    _rsdEquivalent = content['rsdEquivalent']

    addTransaction(_id, _sender, _receiver, _amount, _date, _transactionCurrecny, _state)

    thread = threading.Thread(target=transactionThread, args=(_id, _sender, _receiver, _amount, _date, _transactionCurrecny, _state, _rsdEquivalent))
    thread.start()

    retVal = {'message' : 'Transaction successfully initialized'}, 200
    return retVal

@transaction_blueprint.route('/getTransactionHistory', methods = ['GET'])
def getTransactionHistory():
    content = flask.request.json
    _email = content['email']
    _accountNum = content['accountNum']
    _sortFilter = content['sortFilter']
    return getTransactionHistoryFromDB(_email, _accountNum, _sortFilter)

# ==========================================================================================================
# ===================================== Functions for dataBase access ====================================== 
# ==========================================================================================================

def addTransaction(id : int, sender : str, receiver : str, amount : float, date : Date, currency : str, state : str):
    cursor = mysql.connection.cursor()
    cursor.execute(''' INSERT INTO transaction VALUES (%s, %s, %s, %s, %s, %s, %s)''', (id, sender, receiver, amount, date, currency, state))
    mysql.connection.commit()
    cursor.close()

def getTransactionHistoryFromDB(email : str, accountNum : str, sortFilter : str) -> list:
    cursor = mysql.connection.cursor()
    if sortFilter != '':
        sortParts = sortFilter.split(' ')
        if sortParts[0] == 'date':
            if sortParts[1] == 'DESC':
                cursor.execute(''' SELECT * FROM transaction WHERE sender = %s OR receiver = %s OR receiver = %s ORDER BY date DESC''', (email, email, accountNum,))
            else:
                cursor.execute(''' SELECT * FROM transaction WHERE sender = %s OR receiver = %s OR receiver = %s ORDER BY date ASC''', (email, email, accountNum,))
        elif sortParts[0] == 'amount':
            if sortParts[1] == 'DESC':
                cursor.execute(''' SELECT * FROM transaction WHERE sender = %s OR receiver = %s OR receiver = %s ORDER BY amount DESC''', (email, email, accountNum,))
            else:
                cursor.execute(''' SELECT * FROM transaction WHERE sender = %s OR receiver = %s OR receiver = %s ORDER BY amount ASC''', (email, email, accountNum,))
        else:
            if sortParts[1] == 'DESC':
                cursor.execute(''' SELECT * FROM transaction WHERE sender = %s OR receiver = %s OR receiver = %s ORDER BY ID DESC''', (email, email, accountNum,))
            else:
                cursor.execute(''' SELECT * FROM transaction WHERE sender = %s OR receiver = %s OR receiver = %s ORDER BY ID ASC''', (email, email, accountNum,))
    else:
        cursor.execute(''' SELECT * FROM transaction WHERE sender = %s OR receiver = %s OR receiver = %s ORDER BY ID ASC''', (email, email, accountNum,))
    histroy = cursor.fetchall()
    cursor.close()
    return jsonify(histroy)

def getLastTransactionIndex(): 
    cursor = mysql.connection.cursor()
    cursor.execute(''' SELECT ID FROM transaction ORDER BY ID DESC ''')
    response = cursor.fetchone()
    cursor.close()
    if response:
        id = response['ID'] + 1
    else:
        id = 0
    return id


def transactionThread(id, sender, receiver, amount, date, transactionCurrecny, state, rsdEquivalent):
    print('Transaction ', id, ' thread started ')
    sleep(120) # zadato zadatkom 120s (2 min)

    transaction = Transaction(id, sender, receiver, amount, date, transactionCurrecny, state, rsdEquivalent)
    queue.put(transaction)
    

def transactionProcess(queue : Queue):
    while(1):
        transaction = queue.get()

        print('Transaction ', transaction.id, ' process started ')

        # otvaranje nove konekcije u threadu
        mydb1 = MySQLdb.connect(host="localhost",
                            user="root",
                            passwd="",
                            db="bank")
        cursor = mydb1.cursor()

        cursor.execute(''' SELECT balance FROM user WHERE email = %s ''', (transaction.sender,))
        response = cursor.fetchone()
        cursor.close()
        senderAccountBalance = float(response[0])

        
        cursor = mydb1.cursor()
        if senderAccountBalance < transaction.rsdEquivalent:
            # Transaction Fail (Has no money)
            cursor.execute(''' UPDATE transaction SET state = %s WHERE ID = %s''', ('FAIL', transaction.id,))
            print('\nTransaction ', transaction.id, 'process Fail')
        else:
            # Transcation Success (Has money)
            cursor.execute(''' UPDATE transaction SET state = %s WHERE ID = %s''', ('SUCCESS', transaction.id,))
            cursor.execute(''' UPDATE user SET balance = balance - %s WHERE email = %s''', (transaction.rsdEquivalent, transaction.sender,))
            cursor.execute(''' UPDATE user SET balance = balance + %s WHERE email = %s OR accountNum = %s''', (transaction.rsdEquivalent, transaction.receiver, transaction.receiver,))
            print('\nTransaction ', transaction.id, 'process Success')
        mydb1.commit()
        cursor.close()