import os

path, _ = os.path.split(__file__)
path, _ = os.path.split(path)


class DevelopmentConfig():
    SECRET_KEY='dev'
    SQLALCHEMY_DATABASE_URI='sqlite:///' + path + '/instance/development_database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS=False
