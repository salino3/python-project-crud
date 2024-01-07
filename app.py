# pip install psycopg2
# pip install python-dotenv
# pip install cryptography

# virtual enviroment -> source venv/Scripts/activate



from flask import Flask, request, jsonify
from psycopg2 import connect, extras
from dotenv import load_dotenv
from cryptography.fernet import Fernet
import os

load_dotenv()

app = Flask(__name__)
Fernet.generate_key()

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
   conn = get_connection()
   cur = conn.cursor(cursor_factory=extras.RealDictCursor)

   cur.execute('SELECT * FROM users')
   users = cur.fetchall()
   cur.close()
   conn.close()
   return jsonify(users)


@app.post('/api/users')
def create_user():
   new_user = request.get_json()
   username = new_user["username"]
   email = new_user["email"]
   password = Fernet(Fernet.generate_key()).encrypt(bytes(new_user["password"], 'utf-8'))
   conn = get_connection()
   cur = conn.cursor(cursor_factory=extras.RealDictCursor)

   cur.execute('INSERT INTO users (username, email, password) VALUES (%s, %s, %s) RETURNING *',
                (username, email, password))
   new_created_user = cur.fetchone()
   print(new_created_user)
   conn.commit()
   cur.close()
   conn.close()
   return jsonify(new_created_user)


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



