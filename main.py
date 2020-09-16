from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/')
@app.route('/PollHomepage')
def _home_():
    return render_template('index.html', TITLE = "Election Poll App, 2020")

@app.route('/<ideal>')
def _figure_it_out_(ideal):

    if ideal == "all_polls":
        return redirect(url_for('_home_'))

if __name__ == '__main__':
    app.run(debug = True, port = 18080, host = '127.0.0.1')
else:
    raise Exception('\nCannot execute without __main__\n')