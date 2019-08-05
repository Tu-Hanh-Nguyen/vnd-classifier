"""
This module is the main flask application
"""

from flask import Flask

from blueprints import *

app = Flask(__name__)
app.secret_key = b'Secret Key'

app.register_blueprint(homepage)
app.register_blueprint(classifier)

if __name__ == '__main__':
    app.run(debug=True)
