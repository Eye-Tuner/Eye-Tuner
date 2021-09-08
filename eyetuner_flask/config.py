import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

DATABASE_DIR = os.path.join(BASE_DIR, 'db.sqlite')

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_DIR
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = 'ajserwhfdhkaudfhwkjeehw'
