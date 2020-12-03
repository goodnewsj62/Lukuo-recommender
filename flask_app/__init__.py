from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from flask_migrate import Migrate, MigrateCommand
from config.configuration import Config


db = SQLAlchemy()
bcrypt_ = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'
migrate = Migrate()


def create_app(config_file=Config):
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(config_file)

    bcrypt_.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    db.init_app(app)

    with app.app_context():
        from .home.blog import blog
        from .users.auth import auth

        from .error_pages.error_views import page_forbidden, page_not_found, internal_server_error

        app.register_blueprint(blog)
        app.register_blueprint(auth)

        app.register_error_handler(404, page_not_found)
        app.register_error_handler(403, page_forbidden)
        app.register_error_handler(500, internal_server_error)

        return app
