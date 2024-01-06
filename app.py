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


if __name__ == '__main__':
    app.run(debug = True, port = 7000)



