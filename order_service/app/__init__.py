from flask import Flask
from app.routes import register_blueprints
import logging


def create_app():

    # crea e configuro l'applicazione Flask
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    app.logger.setLevel(logging.DEBUG)

    # registro i blueprint
    register_blueprints(app)

    return app
