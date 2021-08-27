import os

from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flaskr.development_config import DevelopmentConfig

"""Create the database object"""
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()


"""Creating an application factory"""
def create_app(test_config=None):
    """Create the app. The __name__ built-in variable sets the import_name.
    Instance_relative_config tells the app that the configuration files are relative to the instance folder."""
    app = Flask(__name__, instance_relative_config=True)

    """Configure the app. This sets default development configurations using the development_config file. 
    This can be committed to a repository"""
    app.config.from_object(DevelopmentConfig)

    """If no test_config is given, the default configurations will be overwritten by values from the config.py file
    located in the instance folder, only if this file exists. This can be used to set the real SECRET_KEY.
    If there is a test_config, that will be used to set and overwrite the default configuration."""
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    """Try to make an instance folder. If this folder already exists an OSError is raised.
    The instance folder is mandatory, since it will contain the database"""
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    """Create the database object"""
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from flaskr.users.routes import users
    from flaskr.main.routes import main

    app.register_blueprint(users)
    app.register_blueprint(main)

    return app
