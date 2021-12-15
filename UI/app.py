from flask import Flask, render_template, request, json, session, jsonify
import requests



app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

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

        # response = (req.json())["message"]     
        # return json.dumps({'html': '<span>'+ response + '</span>'})
        _message = (req.json())["message"]     
        return render_template('register.html', message = _message)



@app.route('/login')
def login():
    return render_template('login.html')




app.run(port=5000)