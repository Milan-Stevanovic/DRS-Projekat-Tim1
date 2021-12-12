from flask import Flask
from flask import Flask,render_template, request
from flask_mysqldb import MySQL
 
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'bank'
 
mysql = MySQL(app)
 
@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    lastname = request.form['lastname']
    email = request.form['email']
    password = request.form['password']
    # TODO: add other fields
    # TODO: check if user with the same ID/email is already registered
    cursor = mysql.connection.cursor()
    cursor.execute(''' INSERT INTO user VALUES(NULL,%s,%s,%s,%s)''',(name, lastname, email, password))
    mysql.connection.commit()
    cursor.close()
    return "USER REGISTERED"
 
app.run(port=5001)