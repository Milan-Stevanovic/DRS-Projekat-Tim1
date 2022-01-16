from flask import Flask, render_template, request, json, session, jsonify
from flask.helpers import url_for
import requests
import string
import random
from werkzeug.utils import redirect
from urllib.request import Request, urlopen

currency_dictionary = []
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.secret_key = '98aw3qj3eq2390dq239'

@app.route('/')
def index():
    if 'user' in session:
        if session['user']['verified'] != 0: #verifikovan
            # uzmi karticu
            headers = {'Content-type' : 'application/json', 'Accept': 'text/plain'}
            body = json.dumps({'cardNum': session['user']['cardNum']})
            req = requests.get("http://127.0.0.1:5001/api/getUserCardFromDB", data = body, headers = headers)
            card = (req.json())
            return render_template('index.html', user = session['user'], card = card)
        else:
            return render_template('index.html', user = session['user'])
    return render_template('login.html')

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
        _currency = 'USD'
        _accountNum = ''.join(random.choices(string.digits, k = 18))
        print(_accountNum)


        headers = {'Content-type' : 'application/json','Accept': 'text/plain'}
        body = json.dumps({'name': _name, 'lastname':_lastname, 'email':_email, 'password':_password, 'address':_address, 
                           'city':_city, 'country':_country, 'phoneNum':_phoneNum, 'balance':_balance, 'verified':_verified,
                           'cardNum':_cardNum, 'currency': _currency, 'accountNum' : _accountNum})
        req = requests.post("http://127.0.0.1:5001/api/register", data = body, headers = headers)

        response = (req.json())
        _message = response['message']
        _code = req.status_code
        if _code == 200:
            headers = {'Content-type' : 'application/json', 'Accept': 'text/plain'}
            body = json.dumps({'email': _email})
            req = requests.get("http://127.0.0.1:5001/api/getUserFromDB", data = body, headers = headers)
            session['user'] = (req.json())
            
            return redirect(url_for('index'))
        return render_template('register.html', message = _message)

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
            headers = {'Content-type' : 'application/json', 'Accept': 'text/plain'}
            body = json.dumps({'email': _email})
            req = requests.get("http://127.0.0.1:5001/api/getUserFromDB", data = body, headers = headers)
            session['user'] = (req.json())
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
    body = json.dumps({ 'email': session['user']['email'], 'cardNum' : _cardNum, 'owner' : _owner, 'expDate' : _expDate, 'securityCode' : _securityCode })
    requests.post("http://127.0.0.1:5001/api/linkCard", data = body, headers = headers)

    # User changed, update user in session
    headers = {'Content-type' : 'application/json', 'Accept': 'text/plain'}
    body = json.dumps({'email': session['user']['email']})
    req = requests.get("http://127.0.0.1:5001/api/getUserFromDB", data = body, headers = headers)
    session['user'] = (req.json())

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
        _phoneNum = request.form['phonNum']
        #ova 3 polja su zakomentarisana zato sto nisam stavio u formi da mogu da se mijenjaju
        #_balance = request.form['balance'] 
        #_verified = request.form['verified']
        #_cardNum = request.form['cardNum']
        
        headers = {'Content-type' : 'application/json', 'Accept' : 'text/plain'}
        body = json.dumps({'name' : _name, 'lastname' : _lastname, 'email' : _email, 'password' : _password, 'address' : _address, 'city' : _city, 'country' : _country, 'phoneNum' : _phoneNum})
        req = requests.post("http://127.0.0.1:5001/api/updateProfile", data = body, headers = headers)

        # Get updated user and put it in session['user']
        headers = {'Content-type' : 'application/json', 'Accept': 'text/plain'}
        body = json.dumps({'email': _email})
        req = requests.get("http://127.0.0.1:5001/api/getUserFromDB", data = body, headers = headers)
        session['user'] = (req.json())

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


def updateUserInSession(email):
    # Get updated user and put it in session['user']
    headers = {'Content-type' : 'application/json', 'Accept': 'text/plain'}
    body = json.dumps({'email': email})
    req = requests.get("http://127.0.0.1:5001/api/getUserFromDB", data = body, headers = headers)
    session['user'] = (req.json())

def refreshCurrencyList(currency_dictionary : dict, base_currency : str):
    # base currency is RSD
    req = requests.get("https://freecurrencyapi.net/api/v2/latest?apikey=57fbaed0-7177-11ec-a390-0d2dac4cb175&base_currency=" + base_currency)
    currency_dictionary = (req.json())['data']

app.run(port=5000, debug=True)