from flask import *
from flask_socketio import SocketIO
import pickle

db=pickle.load(open('data.pkl','rb'))
app = Flask(__name__, static_url_path='/static', template_folder='templates')
app.secret_key='aj34$&8@j!#PO!@#$'
socketio = SocketIO(app)


from chat import chat
app.register_blueprint(chat)

@app.route('/')
def index():
    if 'username' in session:
        return render_template('lecture-info.html')
    else:
        return render_template('login.html')

@app.route('/test/<path:path>')
def test(path):
    return render_template(path)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/auth',methods=['POST'])
def auth():
    u=request.form['username']
    p=request.form['password'] 
    if u in db:
        if db[u]=p:
            session['username']=u

@app.route('/create_account')
def create_account():
    return render_template('create-account.html')

@app.route('/create',methods=['POST'])
def create():
    u=request.form['username']
    p=request.form['password'] 
    if u in db:
        return redirect(url_for('create_account',exists=True))
    else:
        db[u]=p
        session['username']=u
        pickle.dump(db,open('data.pkl','wb'))
        return redirect(url_for('index'))

if __name__ == '__main__':
    socketio.run(app, debug=True)
