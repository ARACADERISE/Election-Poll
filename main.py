from flask import Flask, render_template, redirect, url_for, request, make_response
from flask_socketio import SocketIO
import os, json
from PythonStructs.main import CreateStruct
from PythonStructs.PythonStructAutomations._automations_ import StructConnect, EntitleDb

from better_profanity import profanity
profanity.load_censor_words()


# This is a library I developed to make working with data easier!
StructDb = CreateStruct(['ServerShutdowns']) # creates the initial "Struct"

from replit import db

# LIST OF INAPPROPRIATE NAMES

app = Flask(__name__)
app.config['SECRET_KEY'] = 'atguijikiliop22'
socket = SocketIO(app)

loggin = None
signup = None
server_shutdown = False # set to False to start running the server

@app.route('/')
def default_render():
    if server_shutdown == False:
        res = make_response(render_template('temp.html', WELCOME_MSG = 'Welcome to Election Poll, 2020!!!!'))
        return res
    else:
        if os.path.isfile('information.json'):
            op = json.loads(open('information.json','r').read())
            al = []
            for i in op:
                al.append(i)
            
            if 'ServerShutdowns' in al:
                total = op['ServerShutdowns']
                if isinstance(total,list):
                  total = total[0]+1
                StructDb.AddInfo('ServerShutdowns',total)
                StructDb._save_()
        else:
            StructDb.AddInfo('ServerShutdowns',1)
            StructDb._save_()
        try:
            _user = request.cookies.get('username')

            if _user == None:
                _user = "Unknown"
            return render_template('server_down.html', MSG = 'Election Poll, 2020: Server Down', MINI = f'Check back shortly, {_user}')
        except:
            return render_template('server_down.html', MSG = 'Election Poll, 2020: Server Down')

@socket.on('send_comment')
def retrieve(json, methods = ['POST','GET']):
    return socket.emit('sent_response',json,callback = "Comment Sent")
@app.route('/talk', methods = ['POST','GET'])
def _talk_():
    _user = request.cookies.get('username')
    return render_template('comment_sections.html', USERNAME = _user)

@app.route('/update_about_you', methods = ['POST','GET'])
def _update_():
    _user = request.cookies.get('username')

    if 'AboutUser' in db[_user]:
        return render_template('update_about_you.html', USERNAME = _user, CURR_ABOUT = db[_user]['AboutUser'])
    else:
        return render_template('update_about_you.html', USERNAME = _user)
@app.route('/check_new_info', methods = ['POST','GET'])
def _update__():

    try:
        _user_info = request.form['new_user_info']

        _user = request.cookies.get('username')
        _pass = request.cookies.get('password')
        _person = request.cookies.get('person')
        _reason = request.cookies.get('reason')

        if _user in db:
            db[_user] = {'Password':_pass,'VotesFor':_person,'Reason':_reason,'AboutUser':_user_info}

            return redirect(url_for('_home_'))
        else:
            return 'here'
    except:
        return 'ok'

@app.route('/admin/<ideal>', methods = ["POST",'GET'])
def _ADMIN_(ideal):
    if ideal == 'home':
        return render_template('temp.html',WELCOME_MSG = 'Welcome to Election Poll, 2020', admin = True)
    if ideal == 'login':
        return render_template('login.html', admin = True)
    if ideal == 'signup':
        return render_template('signup.html', admin = True)
    if ideal == 'homepage':
        if server_shutdown == True:
            return render_template('error.html', information = "Cannot access homepage without logging in", additional = "The Server Is Down")
        else:
            return render_template('error.html', information = "Cannot access homepage without logging in")

@app.route('/homescreen', methods = ['POST', 'GET'])
@app.route('/home', methods = ['POST', 'GET'])
def _homescreen_():
    if server_shutdown == False:
        res = make_response(render_template('temp.html', WELCOME_MSG = 'Welcome to Election Poll, 2020'))
        res.delete_cookie('username')
        res.delete_cookie('password')
        return res
    else:
        try:
            _user = request.cookies.get('username')
            return render_template('server_down.html', MSG = 'Election Poll, 2020: Server Down', MINI = f'Check back shortly, {_user}')
        except:
            return render_template('server_down.html', MSG = 'Election Poll, 2020: Server Down')

@app.route('/login', methods = ['POST','GET'])
def _login_page_():
    if server_shutdown == False:
        return render_template('login.html')
    else:
        try:
            _user = request.cookies.get('username')
            return render_template('server_down.html', MSG = 'Election Poll, 2020: Server Down', MINI = f'Check back shortly, {_user}')
        except:
            return render_template('server_down.html', MSG = 'Election Poll, 2020: Server Down')

@app.route('/signup', methods = ['POST','GET'])
def _signup_page_():
    if server_shutdown == False:
        return render_template('signup.html')
    else:
        try:
            _user = request.cookies.get('username')
            return render_template('server_down.html', MSG = 'Election Poll, 2020: Server Down', MINI = f'Check back shortly, {_user}')
        except:
            return render_template('server_down.html', MSG = 'Election Poll, 2020: Server Down')
    
@app.route('/delete', methods = ['POST','GET'])
def ADMIN_DELETE():
    return render_template('login.html', special_admission = True)

@app.route('/delete_user', methods = ['POST','GET'])
def ADMIN_DELETE_():

    try:
        admin_login_value = request.form['password']
        admin_username_value = request.form['username']

        if admin_login_value == db["admin_pass"] and admin_username_value == db["admin_user"]:
            return render_template('remove_user.html')
        else:
            return render_template('error.html', information = 'Something Went Wrong')

    except:
        return redirect(url_for('default_render'))

@app.route('/success', methods = ['POST','GET'])
def _success_():
    
    try:
        USER = request.form['USER']
        REASON = request.form['REASON']

        if USER in db and not 'Deleted' in db[USER]:
            db[USER] = {'Deleted':True, 'banned_due_to':REASON}
            return f'User {USER} has been removed, {db[USER]}'
        else:
            return redirect(url_for('default_render'))
    except:
        return redirect(url_for('default_render'))

@app.route('/dev_notes', methods = ['POST','GET'])
def dev_notes():
    return render_template('dev_notes.html')

@app.route('/vote_form', methods = ['POST','GET'])
def _vote_form_():

    try:
        username = request.form['username']

        return render_template('vote_form.html', MSG = f"Who are YOU voting for, {profanity.censor(username)}?")
    except:
        try:
            username = request.form['username_signup']
            
            return render_template('vote_form.html', MSG = f"Who are YOU voting for, {profanity.censor(username)}?")
        except: return redirect(url_for('_home_'))

@app.route('/redirect', methods = ['GET','POST'])
def redirect_():
    try:
        person = request.form['Search_user']

        #for i in bad_names:
        #    if i in person.lower():
        #        _user = request.cookies.get('username')
        #        _person = request.cookies.get('person')
        #        _reason = request.cookies.get('reason')
        #        return render_template('homepage.html', USERNAME = _user, PERSON = _person, REASON = _reason, err_msg = "Usernames do not include bad words!")

        if person in db:
            if person == request.cookies.get('username'):
                return redirect(url_for('_home_'))
            if 'AboutUser' in db[person]:
                return render_template('visitor_view.html', USERNAME =profanity.censor(person), ABOUT = db[person]['AboutUser'])
            else:
                return render_template('visitor_view.html', USERNAME = profanity.censor(person))
        else:
            return redirect(url_for('_home_'))
        
    except: 
        _user = request.cookies.get('username')
        _person = request.cookies.get('person')
        _reason = request.cookies.get('reason')
        return render_template('homepage.html', USERNAME = profanity.censor(_user), PERSON = _person, REASON = _reason)
    
@app.route('/change_password', methods = ['POST','GET'])
def _change_pass_():
    return render_template('change_password.html')
@app.route('/check_new_pass', methods = ['POST', 'GET'])
def transmit_new_pass():
    try:
        new_pass = request.form['new_pass']
        _user = request.cookies.get('username')
        _person = request.cookies.get('person')
        _reason = request.cookies.get('reason')
        db_ = db[_user]
        
        if new_pass == db_['Password']:
            return render_template('change_password.html',err = 'Password Must Be Different Than Current Password')
        
        res = make_response(render_template('homepage.html', USERNAME = profanity.censor(_user), PERSON = _person, REASON =_reason))
        
        if 'AboutUser' in db_:
            db[_user] = {'Password':new_pass,'VotesFor':_person, 'Reason':_reason, 'AboutUser':db_['AboutUser']}
        else:
            db[_user] = {'Password':new_pass,'VotesFor':_person, 'Reason':_reason}
        
        res.set_cookie('password',new_pass,max_age=600*600*240*365*20)
        return res
    except: return 'uh oh'

@app.route('/create_new_room', methods = ['POST','GET'])
def create_debate_room():
    _user = request.cookies.get('username')
    return render_template('create_new_room.html', USERNAME = _user)
@app.route('/new_room', methods = ['POST','GET'])
def _create_new_room_():
    try:
        _new_room = request.form['new_room_name']
        _new_room_details = request.form['new_room_details']

        _user = request.cookies.get('username')
        if 'DebateRooms' in db:
            db_ = db['DebateRooms']
            db_.append({_user:_new_room,'Details':_new_room_details})
            db['DebateRooms'] = db_
        else:
            db['DebateRooms'] = [{'RoomName':_new_room,'Details':_new_room_details,'RoomOwner':_user}]

        _person = request.cookies.get('person')
        _reason = request.cookies.get('reason')
        #_password = request.cookies.get('password')

        res = make_response(render_template('homepage.html', USERNAME = profanity.censor(_user), PERSON = _person, REASON = _reason))
        
        return res

    except: return 'nah'
@app.route('/debate_rooms', methods = ['POST', 'GET'])
def debate_rooms():
    _user = request.cookies.get('username')

    try:
        debate_rooms = db['DebateRooms']
        return render_template('debate_rooms.html', USERNAME = _user, DEBATE_ROOMS = profanity.censor(debate_rooms))
    except:
        return redirect(url_for('_home_'))

@app.route('/homepage',methods = ['POST','GET'])
def _home_():

    if server_shutdown == False:
        PEOPLE = ['trump','biden']
    
    try:
        _user = request.form['username_signup']
        _pass = request.form['password_signup']
        _person = request.form['person']
        _reason = request.form['reason']

        if not _person.lower() in PEOPLE:
            return render_template('error.html',signup_redirect="You can only vote for Biden or Trump")
        
        #for i in bad_names:
        #    if i in _user.lower() or i in _pass.lower():
        #        _user = request.cookies.get('username')
        #        _person = request.cookies.get('person')
        #        _reason = request.cookies.get('reason')
        #        return render_template('error.html', signup_redirect = "Usernames/Passwords do not include bad words!")

        #return f'{_user}{db[_user]}'

        if _user in db:
            if 'Deleted' in db[_user]:
                db_ = db[_user]
                return render_template('error.html', signup_redirect = f'banned due to {db_["banned_due_to"]}')
                #return render_template('erorr.html', signup_redirect = f"Cannot sign up as {_user}. Account was banned for {db_['banned_due_to']}")
            else:
                return render_template('error.html', sigup_redirect = 'User already exists')

        if not _user in db:
            if len(_user) >= 20:
                return render_template('error.html',signup_redirect = 'Username too long. Must be under 20 characters')
            
            if _user == 'MocaCDeveloper' or _user == 'Coder100':
                db[_user] = {'Password':_pass,'VotesFor':_person,'Reason':_reason,'Entitled':'Mod'}
            else:
                db[_user] = {'Password':_pass,'VotesFor':_person,'Reason':_reason}
        
        if 'Entitled' in db[_user]:
            res = make_response(render_template('homepage.html',USERNAME = profanity.censor(_user), PERSON = _person, REASON = _reason, MOD = 'Website Moderator'))
        else:
            res = make_response(render_template('homepage.html',USERNAME = profanity.censor(_user), PERSON = _person, REASON = _reason))
        res.set_cookie('username',_user,max_age=600*600*240*365*20)
        res.set_cookie('password',_pass,max_age=600*600*240*365*20)
        res.set_cookie('person',_person,max_age=600*600*240*365*20)
        res.set_cookie('reason',_reason,max_age=600*600*240*365*20)

        return res
    except:

        try:
            _user = request.form['username']
            _pass = request.form['password']

            #for i in bad_names:
            #    if i in _user.lower() or i in _pass.lower():
            #         _user = request.cookies.get('username')
            #        _person = request.cookies.get('person')
            #        _reason = request.cookies.get('reason')
            #        return render_template('error.html', login_redirect = "Usernames/Passwords do not include bad words!")

            if _user in db:
                if 'Deleted' in db[_user]:
                    return render_template('error.html', login_redirect = f"You're account was removed by the developers for {db[_user]['banned_due_to']}")
                if db[_user]['Password'] == _pass:

                    _person = db[_user]['VotesFor']
                    _reason = db[_user]['Reason']

                    #res = None
                    if 'AboutUser' in db[_user]:
                        if 'Entitled' in db[_user]:
                            res = make_response(render_template('homepage.html',USERNAME = profanity.censor(_user), PERSON = _person, REASON = _reason, ABOUT = db[_user]['AboutUser'], MOD = 'Website Moderator'))
                        else:
                            res = make_response(render_template('homepage.html',USERNAME = profanity.censor(_user), PERSON = _person, REASON = _reason, ABOUT = db[_user]['AboutUser']))
                    else:
                        if 'Entitled' in db[_user]:
                            res = make_response(render_template('homepage.html',USERNAME = profanity.censor(_user), PERSON = _person, REASON = _reason, MOD = 'Website Moderator'))
                        else:
                            res = make_response(render_template('homepage.html',USERNAME = profanity.censor(_user), PERSON = _person, REASON = _reason))
                    res.set_cookie('username',profanity.censor(_user),max_age=600*600*240*365*20)
                    res.set_cookie('password',_pass,max_age=600*600*240*365*20)
                    res.set_cookie('person',_person,max_age=600*600*240*365*20)
                    res.set_cookie('reason',_reason,max_age=600*600*240*365*20)

                    return res
                else:
                    return render_template('error.html',login_redirect = "Incorrect Password")
            else:
                return render_template('error.html', login_redirect = "Username doesn't exist")
        except:

            _user = request.cookies.get('username')
            _pass = request.cookies.get('password')
            _person = request.cookies.get('person')
            _reason = request.cookies.get('reason')

            if _user in db:
                if 'AboutUser' in db[_user]:
                    if 'Entitled' in db[_user]:
                        return render_template('homepage.html', USERNAME = profanity.censor(_user), PERSON = _person, REASON = _reason, ABOUT = db[_user]['AboutUser'],MOD = 'Website Moderator')
                    else:
                        return render_template('homepage.html', USERNAME = profanity.censor(_user), PERSON = _person, REASON = _reason, ABOUT = db[_user]['AboutUser'])
                else:
                    if 'Entitled' in db[_user]:
                        return render_template('homepage.html', USERNAME = profanity.censor(_user), PERSON = _person, REASON = _reason,MOD = 'Website Moderator')
                    else:
                        return render_template('homepage.html', USERNAME = profanity.censor(_user), PERSON = _person, REASON = _reason)

            else:
                return render_template('error.html', login_redirect = "Logged Out")
# _figure_it_out_ will probably be for users specific requests to certain spots of the website

@app.route('/<ideal>', methods = ['POST','GET'])
def _figure_it_out_(ideal):
    if server_shutdown == False:
        if ideal == "homepage":
            return redirect(url_for('_home_'))
        else:
            return render_template('error.html', ErrTitle = "URL Not Found", information = "The URL %s does not exist :(" % ideal, TITLE = "URL Not Found")
    else:
        try:
            _user = request.cookies.get('username')
            return render_template('server_down.html', MSG = 'Election Poll, 2020: Server Down', MINI = f'Check back shortly, {_user}')
        except:
            return render_template('server_down.html', MSG = 'Election Poll, 2020: Server Down')

if __name__ == '__main__': 
    socket.run(app,debug = True, port = 8080, host = '0.0.0.0')
    # hey you put it on the wrong IP lol
else:
    raise Exception('\nCannot execute without __main__\n') 
