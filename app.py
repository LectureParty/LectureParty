from flask import *
from flask_socketio import SocketIO
import pickle
import random
db={}
users,rooms,rbu,ubr=None,None,None,None
try:
    db=pickle.load(open('data.pkl','rb'))
    users=db['users']
    rooms=db['rooms']
    rbu=db['rooms_by_user']
    ubr=db['users_by_room']
except:
    db={'users': dict(),'rooms':dict(),'rooms_by_user':dict(),'users_by_room':dict()}
    users=db['users']
    rooms=db['rooms']
    rbu=db['rooms_by_user']
    ubr=db['users_by_room']


app = Flask(__name__, static_url_path='/static', template_folder='templates')
app.secret_key='aj34$&8@j!#PO!G@#$'
socketio = SocketIO(app)


from chat import chat
app.register_blueprint(chat)

@app.route('/')
def index():
    if 'username' in session:
        tmp=list()
        for roomid in rbu[session['username']]:
            tmp.append({'name':rooms[roomid],'code':roomid})
        return render_template('my-parties.html',**{'username':session['username'],'rooms':tmp})
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
    if u in users:
        if users[u]==p:
            session['username']=u
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login',error=True))
    
@app.route('/update_password',methods=['POST'])
def update_pw():
    p=request.form['password'] 
    users[session['username']]=p
    pickle.dump(db,open('data.pkl','wb'))
    return redirect(url_for('index'))

@app.route('/create_account')
def create_account():
    return render_template('create-account.html')

@app.route('/create',methods=['POST'])
def create():
    u=request.form['username']
    p=request.form['password'] 
    if u in users:
        return redirect(url_for('create_account',error=True))
    else:
        users[u]=p
        rbu[u]=list()
        session['username']=u
        pickle.dump(db,open('data.pkl','wb'))
        return redirect(url_for('index'))
    
@app.route('/new_party',methods=['POST'])
def new_party():
    name=request.form['create-name']
    room_id=random.randint(10**9,9*(10**9))
    rbu[session['username']].append(room_id)
    ubr[room_id]=list()
    ubr[room_id].append(session['username'])
    rooms[room_id]=name
    pickle.dump(db,open('data.pkl','wb'))
    return redirect(url_for('party',party_id=room_id))

@app.route('/join_party',methods=['POST'])
def join_party():
    try: 
        code=int(request.form['join-code'])
    except:
        return 'Code must be a number'
    
    if code in rooms:
        if code not in rbu[session['username']]:
            rbu[session['username']].append(code)
            ubr[code].append(session['username'])
            pickle.dump(db,open('data.pkl','wb'))
        return redirect(url_for('party',party_id=code))
    else:
        return 'Code not found'

@app.route('/party/<int:party_id>')
def party(party_id):
    if party_id in rooms:
        return render_template('lecture-info.html',**{'name': rooms[party_id], 'code': party_id,'participants':ubr[party_id]})
    else:
        return 'Room not found.'

@app.route('/partymeet/<int:party_id>')
def partymeet(party_id):
    return render_template('party.html',**{'roomnumber':party_id, 'username': session['username']})

@app.route('/log_out')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    socketio.run(app, debug=True)
