from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from config.configuration import Config


db = SQLAlchemy()
bcrypt_ = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'


def create_app(config_file=Config):
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(config_file)

    bcrypt_.init_app(app)
    login_manager.init_app(app)

    db.init_app(app)

    with app.app_context():
        from .home.blog import blog
        from .users.auth import auth

        app.register_blueprint(blog)
        app.register_blueprint(auth)

        return app
