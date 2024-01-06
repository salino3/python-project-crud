# pip install psycopg2
# pip install python-dotenv


from flask import Flask
from psycopg2 import connect

host = 'localhost'
port = 3307
dbname =

connect()

app = Flask(__name__)

@app.get('/')
def home():
    return '<h1>Hello World!</h1>'


if __name__ == '__main__':
    app.run(debug = True, port = 7000)



