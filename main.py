from flask import Flask, render_template, redirect, url_for, request
import os, json

app = Flask(__name__)

loggin = None
signup = None

"""

    To keep everything simple with templates(or blocks), lets just not do it!

    It is way too confusing tbh. I have never used them. I have only ever used shortcuts.

    To me, templates will get into too much of a hassle and will end up screwing up the .html files(by using mutliple different properties from each file)

    To, to prevent the errors of extending files and using block content from different html files, lets just write pure html with not template shortcuts
"""
@app.route('/')
def default_render():
    return render_template('temp.html', WELCOME_MSG = 'Welcome to Election Poll, 2020')

@app.route('/login', methods = ['POST','GET'])
def _login_page_():
    return render_template('login.html')

@app.route('/signup', methods = ['POST','GET'])
def _signup_page_():
    return render_template('signup.html')

@app.route('/homepage',methods = ['POST','GET'])
def _home_():

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
                    return render_template('homepage.html', TITLE = "Election Poll App, 2020", INFORMATION = f"Welcome to the Election Poll App, 2020. We are glad to see you, {username_login}")
                else:
                    #username_login = None
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
                
                return render_template('homepage.html', TITLE = "Election Poll App, 2020", INFORMATION = f"Welcome to the Election Poll App, 2020. We are glad to see you, {username_signup}")
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
                
                return render_template('homepage.html', TITLE = "Election Poll App, 2020", INFORMATION = f"Welcome to the Election Poll App, 2020. We are glad to see you, {username_signup}")
    except:pass

    return render_template('error.html', information = "An error has occured.")

# _figure_it_out_ will probably be for users specific requests to certain spots of the website

@app.route('/<ideal>', methods = ['POST','GET'])
def _figure_it_out_(ideal):

    if ideal == "homepage":
        return redirect(url_for('_home_'))
    else:
        return render_template('error.html', ErrTitle = "URL Not Found", information = "The URL %s does not exist :(" % ideal, TITLE = "URL Not Found")

if __name__ == '__main__':
    app.run(debug = True, port = 8080, host = '0.0.0.0')
    # hey you put it on the wrong IP lol
else:
    raise Exception('\nCannot execute without __main__\n')