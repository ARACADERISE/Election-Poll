from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

"""

    To keep everything simple with templates(or blocks), lets just not do it!

    It is way too confusing tbh. I have never used them. I have only ever used shortcuts.

    To me, templates will get into too much of a hassle and will end up screwing up the .html files(by using mutliple different properties from each file)

    To, to prevent the errors of extending files and using block content from different html files, lets just write pure html with not template shortcuts
"""
@app.route('/')
@app.route('/default', methods = ['POST','GET'])
def default_render():
    return render_template('temp.html', WELCOME_MSG = 'Welcome to Election Poll, 2020')

@app.route('/homepage',methods = ['POST','GET'])
def _home_():
    return render_template('homepage.html', TITLE = "Election Poll App, 2020", INFORMATION = "Yes, the one poll election app!")

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