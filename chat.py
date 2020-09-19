from flask import *
from flask_socketio import SocketIO
from app import socketio

chat = Blueprint('simple_page', __name__, template_folder='templates')

@chat.route('/chattest/test')
def show() -> str:
    return "tasdfest"

@chat.route('/chattest/session')
def sessions():
    return render_template('session.html')

def messageReceived(methods=['GET', 'POST']):
    print('chat was received!!!')

@socketio.on('chat event')
def handle_chat_send(json, methods=['GET', 'POST']):
    socketio.emit('chat response', json, callback=messageReceived)
