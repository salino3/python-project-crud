# pip install psycopg2
# pip install python-dotenv


from flask import Flask
from psycopg2 import connect
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

host = os.getenv('HOST')
port = int(os.getenv('PORT'))
dbname = os.getenv('DB_NAME')
user = os.getenv('USER')
password = os.getenv('PASSWORD')

def get_connection():
  conn = connect(host=host, port=port, dbname=dbname, user=user, password=password)
  return conn



@app.get('/')
def home():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT 1 + 1")
    result =  cur.fetchone()
    print(result)
    return '<h1>Hello World!</h1>'


@app.get('/api/users')
def get_users():
   return '<p>Getting users</p>'

@app.post('/api/users')
def create_user():
   return '<p>Creating user</p>'

@app.delete('/api/users/<string:id>')
def delete_user(id):
   return '<p>Deleting user</p>'

@app.put('/api/users/<string:id>')
def update_user(id):
    result = int(id) * 10
    return f'<p>Updating user with ID: {result}</p>'

@app.get('/api/users(<string:id>)')
def get_user(id):
   return '<p>Getting user </p>'
   


if __name__ == '__main__':
    app.run(debug = True, port = 7000)



