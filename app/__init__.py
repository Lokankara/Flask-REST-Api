from flask import Flask
from flask_migrate import Migrate

from app.models import db
from app.controllers import main

migrate = Migrate()


def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config.from_object('config.Config')
    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(main)

    return app
