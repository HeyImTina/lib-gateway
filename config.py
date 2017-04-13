import os


class Config(object):

    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = "mysql://job:1234@localhost:3306/library?charset=utf8"
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'


config = {
    "dev": Config
}