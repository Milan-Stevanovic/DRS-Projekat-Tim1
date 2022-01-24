import multiprocessing
from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'bank'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'  # da nam baza vraca dictionary sa header-ima iz baze podataka
 
mysql = MySQL(app)

from blueprints.users import user_blueprint
from blueprints.transactions import transaction_blueprint, transactionProcess, queue

process = multiprocessing.Process(target=transactionProcess, args=[queue])

if __name__ == "__main__":
    app.register_blueprint(user_blueprint, url_prefix = '/api')
    app.register_blueprint(transaction_blueprint, url_prefix = '/api')
    process.start()
    app.run(port=5001)