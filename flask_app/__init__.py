from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from config.configuration import Config
from flask_app.database import init_db,db_session

bcrypt_ = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'


def create_app(config_file = Config):
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(config_file)

    bcrypt_.init_app(app)
    login_manager.init_app(app)

    init_db()

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    with app.app_context():
        from .home.blog import blog
        from .users.auth import auth

        app.register_blueprint(blog)
        app.register_blueprint(auth)

        return app

