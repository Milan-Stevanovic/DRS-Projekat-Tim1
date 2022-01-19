from email import header
from sqlite3 import Date
from flask import Flask, render_template, request, json, session, jsonify
from flask.helpers import url_for
import requests
import string
import random
from werkzeug.utils import redirect
from urllib.request import Request, urlopen

currency_dictionary = {}
converted_balance = ""
sortDate = ""
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.secret_key = '98aw3qj3eq2390dq239'

@app.before_first_request
def getCurrencyList():
    global currency_dictionary 
    currency_dictionary = refreshCurrencyList('RSD')
    global sortDate
    sortDate = 'ASC'

@app.route('/')
def index():
    if 'user' in session:
        if session['user']['verified'] != 0: #verifikovan
            # uzmi karticu
            print(session['user'])
            headers = {'Content-type' : 'application/json', 'Accept': 'text/plain'}
            body = json.dumps({'cardNum': session['user']['cardNum']})
            req = requests.get("http://127.0.0.1:5001/api/getUserCardFromDB", data = body, headers = headers)
            card = (req.json())
            transaction_history = getTransactionHistory()
            return render_template('index.html', user = session['user'], 
                                                 card = card, 
                                                 currency_dictionary = currency_dictionary, 
                                                 converted_balance = converted_balance,
                                                 transaction_history = transaction_history)
        else:
            return render_template('index.html', user = session['user'])
    return render_template('index.html', user = '')

@app.route('/register',methods = ['POST','GET'])
def register():
    if request.method == 'GET':
        return render_template('register.html',message = "")
    else:
        _name = request.form['name']
        _lastname = request.form['lastname']
        _email = request.form['email']
        _password = request.form['password']
        _address = request.form['address']
        _city = request.form['city']
        _country = request.form['country']
        _phoneNum = request.form['phoneNum']
        _balance = "0"
        _verified = 'False'
        _cardNum = "-1"
        _currency = 'RSD'

        headers = {'Content-type' : 'application/json','Accept': 'text/plain'}
        body = json.dumps({'name': _name, 'lastname':_lastname, 'email':_email, 'password':_password, 'address':_address, 
                           'city':_city, 'country':_country, 'phoneNum':_phoneNum, 'balance':_balance, 'verified':_verified,
                           'cardNum':_cardNum, 'currency': _currency})
        req = requests.post("http://127.0.0.1:5001/api/register", data = body, headers = headers)

        response = (req.json())
        _message = response['message']
        _code = req.status_code
        if _code == 200:
            updateUserInSession(_email)
            
            return redirect(url_for('index'))
        return render_template('index.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        _email = request.form['email']
        _password = request.form['password']

        headers = {'Content-type' : 'application/json','Accept': 'text/plain'}
        body = json.dumps({'email':_email,'password':_password })
        req = requests.post("http://127.0.0.1:5001/api/login",data = body,headers = headers)

        response = (req.json())
        _message = response['message']
        _code = req.status_code
        if _code == 200:
            updateUserInSession(_email)
            return redirect(url_for('index'))
        else:
            session['user'] = None
            return render_template('login.html', message = _message)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/linkCard', methods=['POST'])
def linkCard():
    _newBalance = currency_dictionary['USD']*(-1)
    _cardNum = request.form['cardNum']
    _owner = request.form['owner']
    _month = request.form['month']
    _year = request.form['year']
    _expDate = _month + '/' + _year
    _securityCode = request.form['securityCode']

    # Check if card with same cardNum is already registered
    headers = {'Content-type' : 'application/json','Accept': 'text/plain'}
    body = json.dumps({ 'cardNum' : _cardNum })
    req = requests.post("http://127.0.0.1:5001/api/checkCard", data = body, headers = headers)
    response = (req.json())
    _message = response['message']
    _code = req.status_code
    if _code == 400:
        return render_template('index.html', user = session['user'], message = _message)

    # Update cardNum in 'user' table and insert new row in 'card' table
    headers = {'Content-type' : 'application/json','Accept': 'text/plain'}
    body = json.dumps({ 'email': session['user']['email'], 'cardNum' : _cardNum, 'owner' : _owner, 'expDate' : _expDate, 'securityCode' : _securityCode, 'balance' : _newBalance })
    requests.post("http://127.0.0.1:5001/api/linkCard", data = body, headers = headers)

    # User changed, update user in session
    updateUserInSession(session['user']['email'])

    return redirect(url_for('index'))

@app.route('/profile',methods = ['GET'])
def changeProfileInfo():
    # ako je get metod onda ispisujemo informacije korisnika
    return render_template('profile.html', user = session['user'])

@app.route('/updateProfile', methods = ['POST','GET'])
def updateProfileInfo():
    if request.method == 'GET':
       return render_template('updateProfile.html', user = session['user'])
    else:
        _name = request.form['name']
        _lastname = request.form['lastname']
        _email = session['user']['email']
        _password = request.form['password']
        _address = request.form['address']
        _city = request.form['city']
        _country = request.form['country']
        _phoneNum = request.form['phoneNum']
        #ova 3 polja su zakomentarisana zato sto nisam stavio u formi da mogu da se mijenjaju
        #_balance = request.form['balance'] 
        #_verified = request.form['verified']
        #_cardNum = request.form['cardNum']
        
        headers = {'Content-type' : 'application/json', 'Accept' : 'text/plain'}
        body = json.dumps({'name' : _name, 'lastname' : _lastname, 'email' : _email, 'password' : _password, 'address' : _address, 'city' : _city, 'country' : _country, 'phoneNum' : _phoneNum})
        req = requests.post("http://127.0.0.1:5001/api/updateProfile", data = body, headers = headers)

        # Get updated user and put it in session['user']
        updateUserInSession(session['user']['email'])

        _code = req.status_code
        if _code == 200:
            return redirect(url_for('index'))
        return render_template('profile.html')

@app.route('/addFunds', methods = ['POST'])
def addFunds():
    _amount = request.form['amount']

    _new_balance = float(_amount) + float(session['user']['balance'])

    headers = {'Content-type' : 'application/json', 'Accept' : 'text/plain'}
    body = json.dumps({'email' : session['user']['email'], 'new balance' : _new_balance, 'currency' : 'RSD'})
    req = requests.post("http://127.0.0.1:5001/api/addFunds", data = body, headers = headers)

    updateUserInSession(session['user']['email'])

    return redirect(url_for('index'))


@app.route('/initTransaction', methods = ['POST'])
def initTransaction():
    _sender = session['user']['email']
    _receiver = request.form['receiver']
    _amount = request.form['amount']
    _transactionCurrecny = request.form['transactionCurrency']
    _date = Date.today().strftime("%y-%m-%d")
    _state = "PROCESSING"

    headers = {'Content-type' : 'application/json', 'Accept': 'text/plain'}
    body = json.dumps({'sender' : _sender, 'receiver' : _receiver, 'amount' : _amount, 'transactionCurrency' : _transactionCurrecny, "date" : _date, "state" : _state})
    req = requests.post("http://127.0.0.1:5001/api/initTransaction", data = body, headers = headers)
   
    return redirect(url_for('index'))

@app.route('/convert', methods = ['POST'])
def convert():
    _convertCurrency = request.form['convertCurrency']
    global converted_balance
    converted_balance = str(session['user']['balance'] / currency_dictionary[_convertCurrency]) + " " + _convertCurrency
    return redirect(url_for('index'))

@app.route('/sortByDateAsc', methods = ['GET'])
def sortByDateAsc():
    global sortDate
    sortDate = 'ASC'
    print('method call')
    print(sortDate)
    return redirect(url_for('index'))

@app.route('/sortByDateDesc', methods = ['GET'])
def sortByDateDesc():
    global sortDate
    sortDate = 'DESC'
    print('method call')
    print(sortDate)
    return redirect(url_for('index'))

#============================================================ REGULAR FUNCTIONS ============================================================ 

def updateUserInSession(email):
    # Get updated user and put it in session['user']
    headers = {'Content-type' : 'application/json', 'Accept': 'text/plain'}
    body = json.dumps({'email': email})
    req = requests.get("http://127.0.0.1:5001/api/getUserFromDB", data = body, headers = headers)
    session['user'] = (req.json())

def refreshCurrencyList(base_currency : str):
    # base currency is RSD in our case
    req = requests.get("https://freecurrencyapi.net/api/v2/latest?apikey=57fbaed0-7177-11ec-a390-0d2dac4cb175&base_currency=" + base_currency)
    currency_dict = (req.json())['data']

    # Converts every other currency in base currecy value
    for key, value in currency_dict.items():
        currency_dict[key] = 1 / value

    return currency_dict

def getTransactionHistory():
    headers = {'Content-type' : 'application/json', 'Accept': 'text/plain'}
    global sortDate
    print('\n\n\n\n\n\n\n\n TEST')
    print(sortDate)
    print('\n\n\n\n\n\n\n\n')
    body = json.dumps({'email': session['user']['email'], 'accountNum' : session['user']['accountNum'], 'sortDate' : sortDate})
    req = requests.get("http://127.0.0.1:5001/api/getTransactionHistory", data = body, headers = headers)
    return req.json()

app.run(port=5000, debug=True)