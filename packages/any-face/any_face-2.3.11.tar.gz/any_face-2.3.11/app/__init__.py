from flask import Flask

flask_app = Flask(__name__, static_url_path='/static/')

from app import home