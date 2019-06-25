import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    url = 'postgresql://{}:{}@{}:{}/{}'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://postgres:11111111@localhost:5432/users'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
