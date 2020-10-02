from flask import Flask, render_template, redirect, url_for, request
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
        return render_template('server_down.html', MSG = 'Election Poll, 2020: Server Down')

@app.route('/login', methods = ['POST','GET'])
def _login_page_():
    if server_shutdown == False:
        return render_template('login.html')
    else:
        return render_template('server_down.html', MSG = 'Election Poll, 2020: Server Down')

@app.route('/signup', methods = ['POST','GET'])
def _signup_page_():
    if server_shutdown == False:
        return render_template('signup.html')
    else:
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

@app.route('/homepage',methods = ['POST','GET'])
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

                    if username_login in all_ and information[username_login] == password_login:
                        return render_template('homepage.html', TITLE = "Election Poll App, 2020", USERNAME = username_login)
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

            if username_signup:

                if not os.path.isfile('user_info.json'):
                    information = {username_signup: password_signup}

                    with open('user_info.json','w') as file:
                        file.write(json.dumps(
                            information,
                            indent=2,
                            sort_keys=False
                        ))
                        file.close()
                    return render_template('homepage.html', TITLE = "Election Poll App, 2020", USERNAME = username_signup)
                if os.path.isfile('user_info.json'):
                    information = json.loads(open('user_info.json','r').read())

                    if username_signup in information:
                        #signup = False
                        return render_template('error.html', signup_redirect = f"The username {username_signup} already exists")

                    information.update({username_signup: password_signup})
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

# _figure_it_out_ will probably be for users specific requests to certain spots of the website

@app.route('/<ideal>', methods = ['POST','GET'])
def _figure_it_out_(ideal):
    if server_shutdown == False:
        if ideal == "homepage":
            return redirect(url_for('_home_'))
        else:
            return render_template('error.html', ErrTitle = "URL Not Found", information = "The URL %s does not exist :(" % ideal, TITLE = "URL Not Found")
    else:
        return render_template('server_down.html', MSG = 'Election Poll, 2020: Server Down')

if __name__ == '__main__':
    app.run(debug = True, port = 8080, host = '0.0.0.0')
    # hey you put it on the wrong IP lol
else:
    raise Exception('\nCannot execute without __main__\n')
