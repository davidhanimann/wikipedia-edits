from flask import Flask
from flask import request
from flask_cors import CORS
import db

app = Flask(__name__)
CORS(app)


# export FLASK_APP=main.py
# export FLASK_ENV=development
# flask run

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/graph')
def get_graph():
    title = request.args.get('title')
    return db.get(title)
