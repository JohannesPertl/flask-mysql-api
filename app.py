import functools

import pymysql
from flask import Flask
from flask import jsonify
from flaskext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'USERNAME'
app.config['MYSQL_DATABASE_PASSWORD'] = 'PASSWORD'
app.config['MYSQL_DATABASE_DB'] = 'DB_NAME'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql.init_app(app)


def access_database(func):
    """Decorator for database access"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            return func(cursor, *args, **kwargs)
        except Exception as e:
            print(e)
        finally:
            conn.close()
            cursor.close()

    return wrapper


@app.route('/')
def hello_world():
    return 'Hello World!'


# READ
@app.route('/get', methods=['GET'])
@access_database
def get(db):
    db.execute('''SELECT * FROM table_name ''')
    data = db.fetchall()
    return jsonify(data)


@app.route('/get/<name>', methods=['GET'])
@access_database
def get_by_name(db, name):
    db.execute('''SELECT * FROM table_name WHERE name=%s''', name)
    data = db.fetchall()
    return jsonify(data)


if __name__ == '__main__':
    app.run()
