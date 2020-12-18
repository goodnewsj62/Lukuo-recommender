from flask import Flask, g, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from flask_migrate import Migrate, MigrateCommand
from config.configuration import Config
from flask_babel import Babel
from flask_geoip import GeoIP


db = SQLAlchemy()
bcrypt_ = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'
migrate = Migrate()
# geoip = GeoIP()
# babel = Babel()


def create_app(config_file=Config):
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(config_file)

    bcrypt_.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    # geoip.init_app(app)
    # babel.init_app()

    db.init_app(app)

    # @babel.localeselector
    # def get_locale():
    #     if not g.get('lang_code', None):
    #         g.lang_code = request.accept_languages.best_match(Config.LANGUAGES)
    #     return g.lang_code

    with app.app_context():
        from .home.blog import blog
        from .users.auth import auth
        from .site.site_view import site
        import flask_app.babel_setup

        from .error_pages.error_views import page_forbidden, page_not_found, internal_server_error

        app.register_blueprint(blog)
        app.register_blueprint(auth)
        app.register_blueprint(site)

        app.register_error_handler(404, page_not_found)
        app.register_error_handler(403, page_forbidden)
        app.register_error_handler(500, internal_server_error)

        return app
