from flask import *
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

from chat import chat
app.register_blueprint(chat)

@app.route('/')
def hello_world():
    return 'Hello from Mikail!'

if __name__ == '__main__':
    socketio.run(app, debug=True)
