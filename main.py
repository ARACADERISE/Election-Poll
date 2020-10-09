from flask import Flask, render_template, redirect, url_for, request, make_response
import os, json
from PythonStructs.main import CreateStruct
from PythonStructs.PythonStructAutomations._automations_ import StructConnect, EntitleDb

# This is a library I developed to make working with data easier!
StructDb = CreateStruct(['ServerShutdowns']) # creates the initial "Struct"

from replit import db

db["admin_user"] = "ADMIN"
db["admin_pass"] = "POLL_ADMIN_"

app = Flask(__name__)

loggin = None
signup = None
server_shutdown = False # set to False to start running the server

@app.route('/')
def default_render():
    if server_shutdown == False:
        return render_template('temp.html', WELCOME_MSG = 'Welcome to Election Poll, 2020')
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
def _homescreen_():
    if server_shutdown == False:
        return render_template('temp.html', WELCOME_MSG = 'Welcome to Election Poll, 2020')
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
            return 'yes'
        else:
            return render_template('error.html', information = 'Something Went Wrong')

    except:
        return redirect(url_for('default_render'))
@app.route('/success', methods = ['POST','GET'])
def _success_():
    pass
    
@app.route('/vote_form', methods = ['POST','GET'])
def _vote_form_():

    try:
        username = request.form['username']

        return render_template('vote_form.html', MSG = f"Who are YOU voting for, {username}?")
    except:
        try:
            username = request.form['username_signup']
            
            return render_template('vote_form.html', MSG = f"Who are YOU voting for, {username}?")
        except: return redirect(url_for('_home_'))

@app.route('/redirect', methods = ['GET','POST'])
def redirect_():
    try:
        person = request.form['Search_user']

        if person in db:
            if not person == request.cookies.get('username'):
                return f'Votes For:{db[person]["VotesFor"]}, Reason: {db[person]["Reason"]}'
            else:
                return redirect(url_for('_home_'))
        else:
            return render_template('error.html', information = 'User does not exist')
        
    except: return 'no'

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

        res = make_response(render_template('homepage.html',USERNAME = _user, PERSON = _person, REASON = _reason))
        res.set_cookie('username',_user,max_age=600*600*240*365*20)
        res.set_cookie('password',_pass,max_age=600*600*240*365*20)
        res.set_cookie('person',_person,max_age=600*600*240*365*20)
        res.set_cookie('reason',_reason,max_age=600*600*240*365*20)

        if _user in db:
            return render_template('error.html', signup_redirect = f'Login as {_user} to stayed logged in!')
        else:
            db[_user] = {'Password':_pass,'VotesFor':_person,'Reason':_reason}

        return res
    except:

        try:
            _user = request.form['username']
            _pass = request.form['password']

            if _user in db:
                if db[_user]['Password'] == _pass:

                    _person = db[_user]['VotesFor']
                    _reason = db[_user]['Reason']
                    res = make_response(render_template('homepage.html',USERNAME = _user, PERSON = _person, REASON = _reason))
                    res.set_cookie('username',_user,max_age=600*600*240*365*20)
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
                return render_template('homepage.html', USERNAME = _user, PERSON = _person, REASON = _reason)
            return 'NO'
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
    app.run(debug = True, port = 8080, host = '0.0.0.0')
    # hey you put it on the wrong IP lol
else:
    raise Exception('\nCannot execute without __main__\n') 
