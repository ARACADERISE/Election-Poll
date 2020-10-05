from flask import Flask, render_template, redirect, url_for, request, make_response
import os, json
from PythonStructs.main import CreateStruct
from PythonStructs.PythonStructAutomations._automations_ import StructConnect, EntitleDb

# This is a library I developed to make working with data easier!
StructDb = CreateStruct(['ServerShutdowns']) # creates the initial "Struct"

app = Flask(__name__)

loggin = None
signup = None
server_shutdown = False

"""
    @Coder100: I added in our own login/sign up pages.
    They are fully functional and they actually work!
"""
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
    admin_login_value = request.form['password']
    admin_username_value = request.form['username']

    if admin_login_value == 'abcdefg' and admin_username_value == 'WebAdminController':
        return 'yes'
    if os.path.isfile('user_info.json'):
        
        users = json.loads(open('user_info.json').read())

        all_ = []
        for i in users:
            all_.append(i)
        if user_to_delete in all_:
            del(users[user_to_delete])
            users.update({'Deleted':user_to_delete})

            with open('user_info.json','w') as file:
                file.write(json.dumps(
                    users,
                    indent=2,
                    sort_keys=False
                ))
                file.close()

                return '<h1>User deleted</h1>'
    else:
        return render_template('error.html', information = 'Deletion failed')
    
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

        info = json.loads(open('user_info.json','r').read())

        if person in info:
            if not person == request.cookies.get('username'):
                return f'Votes For:{info[person]["VotesFor"]}, Reason: {info[person]["Reason"]}'
            else:
                return redirect(url_for('_home_'))
        else:
            return render_template('error.html', information = 'User does not exist')
        
    except: return 'no'

"""@app.route('/homepage',methods = ['POST','GET'])
def _home_():

    if server_shutdown == False:
        global username_login, username_signup, password_login, password_signup

        try:
            username_login = request.form['username']
            password_login = request.form['password']

            if username_login:
                if not os.path.isfile('user_info.json'):
                    return render_template('error.html', login_redirect = "Username/Password is incorrect")
                else:
                    information = json.loads(open('user_info.json','r').read())

                    all_ = []
                    for i in information:
                        all_.append(i)
                    
                    if 'Deleted' in information and username_login == information['Deleted']:
                        return render_template('error.html', login_redirect = "You're account was deleted by an admin")

                    if username_login in all_ and information[username_login]['Password'] == password_login:
                        return render_template('homepage.html', USERNAME = username_login, PERSON = information[username_login]['VotesFor'], REASON = information[username_login]['Reason'])
                    else:
                        #username_login = None
                        if 'Deleted' in information:
                            if username_login == information['Deleted']:
                                return render_template('error.html', login_redirect = "You're account was deleted by an admin")
                        if username_login in all_:
                            return render_template('error.html', login_redirect = "Incorrect password")
                        else:
                            return render_template('error.html', login_redirect = "Incorrect Username/password")
        except: pass
        
        try:
            username_signup = request.form['username_signup']
            password_signup = request.form['password_signup']
            person = request.form['person']
            reason = request.form['reason']

            if username_signup:

                old_info = {}
                if not os.path.isfile('user_info.json'):
                    information = {username_signup:{'Password': password_signup,'VotesFor':person,'Reason':reason}}

                    with open('user_info.json','w') as file:
                        file.write(json.dumps(
                            information,
                            indent=2,
                            sort_keys=False
                        ))
                        file.close()
                    return render_template('login.html', login_from_signup = True, EX = "Login to confirm signup credentials")
                else:
                    information = json.loads(open('user_info.json','r').read())

                    if 'Deleted' in information and username_signup == information['Deleted']:
                        return render_template('error.html', login_redirect = "You're account was deleted by an admin")
                    
                    if username_signup in information:
                        #signup = False
                        return render_template('login.html', login_from_signup = True, EX = 'Confirmation login')

                    information.update({username_signup:{'Password': password_signup,'VotesFor':person,'Reason':reason}})
                    with open('user_info.json','w') as file:

                        file.write(json.dumps(
                            information,
                            indent=2,
                            sort_keys=False
                        ))
                        file.close()
                    
                    return render_template('homepage.html', TITLE = "Election Poll App, 2020", USERNAME = username_signup)
        except:pass

        return render_template('error.html', information = "Cannot access homepage, logged out")
    else:
        return render_template('server_down.html', MSG = 'Election Poll, 2020: Server Down')
"""
@app.route('/homepage',methods = ['POST','GET'])
def _home_():

    if server_shutdown == False:
        try:
            _user = request.form['username_signup']
            _pass = request.form['password_signup']
            _person = request.form['person']
            _reason = request.form['reason']

            res = make_response(render_template('homepage.html',USERNAME = _user, PERSON = _person, REASON = _reason))
            res.set_cookie('username',_user,max_age=600*600*240*365*20)
            res.set_cookie('password',_pass,max_age=600*600*240*365*20)
            res.set_cookie('person',_person,max_age=600*600*240*365*20)
            res.set_cookie('reason',_reason,max_age=600*600*240*365*20)

            if not os.path.isfile('user_info.json'):
                info = {_user:{'Password':_pass,'VotesFor':_person,'Reason':_reason}}

                with open('use_info.json','w') as file:
                    file.write(json.dumps(
                        info,
                        indent=2,
                        sort_keys=False
                    ))
                    file.close()
            else:
                info = json.loads(open('user_info.json','r').read())

                if _user in info:
                    return render_template('error.html', signup_redirect = f'Login as {_user} to stayed logged in!')
                else:
                    info.update({_user:{'Password':_pass,'VotesFor':_person,'Reason':_reason}})

                    with open('user_info.json','w') as file:
                        file.write(json.dumps(
                            info,
                            indent=2,
                            sort_keys=False
                        ))
                        file.close()

            return res
        except:
            try:
                _user = request.form['username']
                _pass = request.form['password']

                info = json.loads(open('user_info.json','r').read())

                if _user in info:
                    if _pass == info[_user]:
                        return render_template('homepage.html', USERNAME = _user, PERSON = _person, REASON = _reason)
                    elif not _pass == info[_user]:
                        return render_template('error.html',login_redirect = "Password was incorrect")
                    else:
                        return render_template('error.html',login_redirect = "Incorrect username/password")
                else:
                    return render_template('error.html', login_redirect = "User doesn't exist")
            except:
                _user = request.cookies.get('username')
                _pass = request.cookies.get('password')
                _person = request.cookies.get('person')
                _reason = request.cookies.get('reason')

                if _person:
                    return render_template('homepage.html', USERNAME = _user, PERSON = _person, REASON = _reason)
                else:
                    return render_template('signup.html')
    else:
        try:
            _user = request.cookies.get('username')
            return render_template('server_down.html', MSG = 'Election Poll, 2020: Server Down', MINI = f'Check back shortly, {_user}')
        except:
            return render_template('server_down.html', MSG = 'Election Poll, 2020: Server Down')
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
