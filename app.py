from flask import *
from flask_socketio import SocketIO

app = Flask(__name__, static_url_path='/static', template_folder='templates')
socketio = SocketIO(app)

from chat import chat
app.register_blueprint(chat)

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/test/<path:path>')
def test(path):
    return render_template(path)

if __name__ == '__main__':
    socketio.run(app, debug=True)
