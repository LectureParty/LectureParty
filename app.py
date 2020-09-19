from flask import *
from flask_socketio import SocketIO
import pickle

db=pickle.load(open('data.pkl','r'))
app = Flask(__name__, static_url_path='/static', template_folder='templates')
app.secret_key='aj34$&8@j!#PO!@#$'
socketio = SocketIO(app)


from chat import chat
app.register_blueprint(chat)

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/test/<path:path>')
def test(path):
    return render_template(path)

@app.route('/auth',methods=['POST'])
def auth():
    return request.form

@app.route('/create_account',methods=['POST'])
def create():
    return request.form

if __name__ == '__main__':
    socketio.run(app, debug=True)
