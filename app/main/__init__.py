import logging
import sys

from flask import Flask

from app import commands
from app.extensions import api, bcrypt, db, debug_toolbar, migrate  # cache
from app.main.controller.user_controller import ns as user_ns


def create_app(config_object="app.settings"):
    """Create application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split(".")[0])
    app.config.from_object(config_object)
    register_extensions(app)
    register_errorhandlers(app)
    register_commands(app)
    configure_logger(app)

    return app


def register_extensions(app):
    """Register Flask extensions."""
    bcrypt.init_app(app)
    db.init_app(app)
    api.init_app(app)
    api.add_namespace(user_ns)
    debug_toolbar.init_app(app)
    migrate.init_app(app, db)
    # cache.init_app(app)
    return None


def register_errorhandlers(app):
    """Register error handlers."""

    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)
    return None


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.lint)


def configure_logger(app):
    """Configure loggers."""
    handler = logging.StreamHandler(sys.stdout)
    if not app.logger.handlers:
        app.logger.addHandler(handler)
