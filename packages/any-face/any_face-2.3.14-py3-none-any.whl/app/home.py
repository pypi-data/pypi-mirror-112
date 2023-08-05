
from app import flask_app
from flask import render_template
from app import helpers

flask_app.config['UPLOADS'] = '/static/img/'
@flask_app.route('/')
def home():
    return render_template("default/home.html")