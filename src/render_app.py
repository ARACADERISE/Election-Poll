from flask import Flask

app = Flask(__name__)

# I just got this going to get it going

class RenderWebpage:
    def __init__(self): pass # not needed yet

    @app.route("/")
    def _setup_homepage_():
        return '</h1>Homepage</h1'
    
    def _RUN_(self):
        app.run(debug=True)