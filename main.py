from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/')
@app.route('/homepage')
def _home_(_error):
    return render_template('index.html', TITLE = "Election Poll App, 2020", INFORMATION = "Yes, the one poll election app!", error = _error)

# _figure_it_out_ will probably be for users specific requests to certain spots of the website
@app.route('/<ideal>')
def _figure_it_out_(ideal):

    if ideal == "homepage":
        return redirect(url_for('_home_'))
    else:
        return _home_('NOO')

if __name__ == '__main__':
    app.run(debug = True, port = 18080, host = '127.0.0.1')
else:
    raise Exception('\nCannot execute without __main__\n')