from flask import *
from flask_socketio import SocketIO
import pickle
import random
from datetime import datetime
from collections import Counter

db={}
users,rooms,rbu,ubr,lectures,lec_times=None,None,None,None,None,None
try:
    db=pickle.load(open('data.pkl','rb'))
    users=db['users']
    rooms=db['rooms']
    rbu=db['rooms_by_user']
    ubr=db['users_by_room']
    lectures=db['lectures']
    lec_times=db['ltimes']
except:
    db={'users': dict(),'rooms':dict(),'rooms_by_user':dict(),'users_by_room':dict(), 'lectures':dict(),'ltimes':dict()}
    users=db['users']
    rooms=db['rooms']
    rbu=db['rooms_by_user']
    ubr=db['users_by_room']
    lectures=db['lectures']
    lec_times=db['ltimes']

# lectures[roomID] = (start_time, [(timestamp, message, screenshot)])

app = Flask(__name__, static_url_path='/static', template_folder='templates')
app.secret_key='aj34$&8@j!#PO!Gw#$'
socketio = SocketIO(app)


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
    lec_times[room_id]=Counter()
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
        if len(lec_times[party_id].most_common())>0:
            date,time=lec_times[party_id].most_common(1)[0][0]
            print('Showing time immediately')
            return render_template('lecture-info.html',**{'name': rooms[party_id], 'code': party_id,'participants':ubr[party_id],'date':date,'time':time})
        else:
            print('not showing time')
            return render_template('lecture-info.html',**{'name': rooms[party_id], 'code': party_id,'participants':ubr[party_id]})
    else:
        return 'Room not found.'

@app.route('/partymeet/<int:party_id>')
def partymeet(party_id):
    return render_template('party.html',**{'roomnumber':party_id, 'username': session['username'],'name':rooms[party_id]})

@app.route('/addScreenshot', methods=['POST'])
def add_sc():
    image_data = request.form.get('img')
    roomID = int(request.form.get('roomID'))
    message = request.form.get('message')
    current_time = datetime.now()

    if roomID in db['lectures']:
        start_time, messages = db['lectures'][roomID]

        timediff = (current_time - start_time).seconds
        hours = timediff // 3600
        minutes = (timediff % 3600) // 60
        seconds = timediff % 60
        if seconds < 10:
            seconds = '0' + str(seconds)
        if minutes < 10:
            minutes = '0' + str(minutes)
        timestamp = f"{hours}:{minutes}:{seconds}"
        messages.append((timestamp, message, image_data))
    pickle.dump(db,open('data.pkl','wb'))
    print('message received')
    return '200'

@app.route('/meetingStart', methods=['POST'])
def set_meeting_start():
    roomID = int(request.form.get('roomID'))
    start_time = datetime.now()
    if roomID not in db['lectures']:
        db['lectures'][roomID] = (start_time, [])
    pickle.dump(db,open('data.pkl','wb'))
    print('recording start')
    return '200'

@app.route('/date_info', methods=['POST'])
def date_info():
    content=request.get_json()
    room=content['room']
    arr=content['arr']
    cnt=lec_times[room]
    lec_times[room]=scheduler(arr,cnt)
    pickle.dump(db,open('data.pkl','wb'))
    return str(list(cnt.most_common(1)[0][0]))
    
@app.route('/log_out')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/review_lecture/<int:roomnumber>')
def review_lecture(roomnumber):
    messages = db['lectures'][roomnumber][1]
    roomname = db['rooms'][roomnumber]
    pickle.dump(db,open('data.pkl','wb'))
    return render_template('review_lecture.html', **{'roomname':roomname, 'messages':messages,'room':roomnumber})

def scheduler(bigArray, cnt=None):
    if cnt == None:
        cnt = Counter()
    for i in range(len(bigArray)):
        if bigArray[i] != 0:
            for j in range(len(bigArray[i])):
                if bigArray[i][j]==1:
                    cnt[(i, j)] += 1
    print(cnt)
    print(bigArray)
    return cnt

if __name__ == '__main__':
    socketio.run(app, debug=True)
