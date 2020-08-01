import os

basedir = os.path.abspath(os.path.dirname(__name__))
dev_data = "sqlite:///" + os.path.join(basedir, 'dev.sqlite')
base_server = "http://127.0.0.1:5000"

class Config():
    SECRET_KEY = "sdfew;/ewf"
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class DevelopConfig(Config):
    SQLALCHEMY_DATABASE_URI = dev_data
    basedir = os.path.abspath(os.path.dirname(__file__))
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'gif', 'GIF'])


config = {
    'default': DevelopConfig
}
