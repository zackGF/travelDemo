from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import *
from App.config import config

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    CORS(app, supports_credentials=True)
    app.config.from_object(config[config_name])
    db.init_app(app)

    from App.views.home import home
    app.register_blueprint(home)
    from App.views.admin import admin
    app.register_blueprint(admin,url_prefix='/root')
    return app

from App.models import *
