from flask import Flask
from flask_mysqldb import MySQL
from blueprints.users import user_blueprint

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'bank'
 
mysql = MySQL(app)

if __name__ == "__main__":
    app.register_blueprint(user_blueprint, url_prefix = '/api')
    app.run(port=5001)