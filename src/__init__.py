from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = '9606b9e7f779b7c914207dd9df676e3f818c9fbaa54d7f0fcbbe03338666f730'

from src import routes
