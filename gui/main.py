from flask import Flask
from flask_cors import *
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
CORS(app, supports_credentials=True)

socketio = SocketIO(app, cors_allowed_origins='*')
