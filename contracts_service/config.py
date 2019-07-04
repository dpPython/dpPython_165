import os

basedir = os.path.abspath(os.path.dirname(__file__))
DEBUG = True
PORT = 5000
HOST = "0.0.0.0"
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = "postgresql://postgres:1@127.0.0.1/contracts"
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
