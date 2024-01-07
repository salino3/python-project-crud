# pip install psycopg2
# pip install python-dotenv
# pip install cryptography

# virtual enviroment -> source venv/Scripts/activate



from flask import Flask, request, jsonify, send_file
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


# 
@app.get('/api/users')
def get_users():
   conn = get_connection()
   cur = conn.cursor(cursor_factory=extras.RealDictCursor)

   cur.execute('SELECT * FROM users')
   users = cur.fetchall()
   cur.close()
   conn.close()
   return jsonify(users)

# 
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


# 
@app.delete('/api/users/<string:id>')
def delete_user(id):
   conn = get_connection()
   cur = conn.cursor(cursor_factory=extras.RealDictCursor)

   cur.execute('DELETE FROM users WHERE ID = %s RETURNING *', (id,))
   user = cur.fetchone()

   conn.commit()
   conn.close()
   cur.close()

   if user is None:
      return jsonify({"message": "User not found"}), 404
   
   return jsonify(user)


#
@app.put('/api/users/<string:id>')
def update_user(id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    
    cur.execute('SELECT * FROM users WHERE id = %s', (id,))
    existing_user = cur.fetchone()
    
    if existing_user is None:
        return jsonify({"message": "User not found"}), 404

    updated_data = request.get_json()

    for key, value in updated_data.items():
        existing_user[key] = value

    if 'password' in updated_data:
        existing_user['password'] = Fernet(Fernet.generate_key()).encrypt(bytes(updated_data['password'], 'utf-8'))

    cur.execute('UPDATE users SET username = %s, email = %s, password = %s WHERE id = %s RETURNING *',
                (existing_user['username'], existing_user['email'], existing_user['password'], id))
    updated_user = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()

    if updated_user is None:
        return jsonify({"message": "User not found"}), 404

    return jsonify(updated_user)


# 
@app.get('/api/users/<string:id>')
def get_user(id):
   conn = get_connection()
   cur = conn.cursor(cursor_factory=extras.RealDictCursor)
# Important: comma at the end of value for query if is one value, for define tuple
   cur.execute('SELECT * FROM  users WHERE id = %s', (id,))
   user = cur.fetchone()
   
   if user is None:
      return jsonify({"message": "User not found"}), 404
   
   return jsonify(user)
   


# 
@app.get('/')
def home():
    return send_file('static/index.html')


 
if __name__ == '__main__':
    app.run(debug = True, port = 7000)



