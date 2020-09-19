from flask import *
from flask_socketio import SocketIO
from app import app

socketio = SocketIO(app)
chat = Blueprint('simple_page', __name__, template_folder='templates')

@chat.route('/chattest/test')
def show() -> str:
    return "tasdfest"

@chat.route('/chattest/session')
def sessions():
    return render_template('session.html')

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on('my event')
def handle_chat_send(json, methods=['GET', 'POST']):
    socketio.emit('my response', json, callback=messageReceived)
