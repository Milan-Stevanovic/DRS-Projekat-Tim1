import re
from flask import Flask, render_template, request, json, session, jsonify
from flask.helpers import url_for
import requests,flask
from werkzeug.utils import redirect


app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.secret_key = '98aw3qj3eq2390dq239'

@app.route('/')
def index():
    if 'email' in session:
        headers = {'Content-type' : 'application/json','Accept': 'text/plain'}
        body = json.dumps({'email': session['email']})
        req = requests.get("http://127.0.0.1:5001/api/getUserFromDB", data = body, headers = headers)
        user = (req.json())
        return render_template('index.html', user = user)
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
        _verified = "False"
        _cardNum = "-1"

        headers = {'Content-type' : 'application/json','Accept': 'text/plain'}
        body = json.dumps({'name': _name,'lastname':_lastname,'email':_email,'password':_password,'address':_address,'city':_city,'country':_country,'phoneNum':_phoneNum,'balance':_balance,'verified':_verified,"cardNum":_cardNum})
        req = requests.post("http://127.0.0.1:5001/api/register",data = body,headers = headers)

        response = (req.json())
        _message = response['message']
        _code = req.status_code
        if _code == 200:
            session['email'] = _email
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
            session['email'] = _email
            return redirect(url_for('index'))
        else:
            session['email'] = None
            return render_template('login.html', message = _message)

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))

@app.route('/linkCard', methods=['POST'])
def linkCard():
    _cardNum = request.form['cardNum']
    _owner = request.form['owner']
    _month = request.form['month']
    _year = request.form['year']
    _expDate = _month + '/' + _year
    _securityCode = request.form['securityCode']

    headers = {'Content-type' : 'application/json','Accept': 'text/plain'}
    body = json.dumps({ 'email': session['email'], 'cardNum' : _cardNum, 'owner' : _owner, 'expDate' : _expDate, 'securityCode' : _securityCode })
    req = requests.post("http://127.0.0.1:5001/api/linkCard", data = body, headers = headers)
    response = (req.json())

    return redirect(url_for('index'))

@app.route('/profile',methods = ['GET'])
def changeProfileInfo():
    #ako je get metod onda ispisujemo informacije korisnika
     headers = {'Content-type' : 'application/json','Accept': 'text/plain'}
     body = json.dumps({ 'email': session['email']})
     req = requests.post("http://127.0.0.1:5001/api/profile", data = body, headers = headers)
     response = (req.json())
     return render_template('profile.html',korisnik = response)

@app.route('/updateProfile',methods = ['POST','GET'])
def updateProfileInfo():
    if request.method == 'GET':
        headers = {'Content-type' : 'application/json','Accept': 'text/plain'}
        body = json.dumps({ 'email': session['email']})
        req = requests.post("http://127.0.0.1:5001/api/profile", data = body, headers = headers)
        response = (req.json())
        
        return render_template('updateProfile.html',korisnik = response)
    else:
        _name = request.form['name']
        _lastname = request.form['lastname']
        _email = session['email']
        _password = request.form['password']
        _address = request.form['address']
        _city = request.form['city']
        _country = request.form['country']
        _phoneNum = request.form['phonNum']
        #ova 3 polja su zakomentarisana zato sto nisam stavio u formi da mogu da se mijenjaju
        #_balance = request.form['balance'] 
        #_verified = request.form['verified']
        #_cardNum = request.form['cardNum']
        
        headers = {'Content-type' : 'application/json','Accept': 'text/plain'}
        body = json.dumps({'name': _name,'lastname':_lastname,'email':_email,'password':_password,'address':_address,'city':_city,'country':_country,'phoneNum':_phoneNum})
        req = requests.post("http://127.0.0.1:5001/api/updateProfile",data = body,headers = headers)
       
        user = (req.json())
        
        _code = req.status_code
        if _code == 200:
            return redirect(url_for('index'))
        return render_template('profile.html')


app.run(port=5000)