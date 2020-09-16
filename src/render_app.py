from flask import Flask

app = Flask(__name__)

# I just got this going to get it going
    

@app.route('/')
def _HOMEPAGE_():
    return '<h1>Hello World</h1'

def _RUN_():
    app.run(debug=True)