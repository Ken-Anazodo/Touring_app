from flask import Flask
from flask_wtf import CSRFProtect
from flask_migrate import Migrate
from sightapp.models import db

csrf= CSRFProtect()
def create_app():
    app = Flask(__name__,instance_relative_config=True)
    app.config.from_pyfile('config.py',silent=True)

    db.init_app(app)
    migrate = Migrate(app,db)
    csrf.init_app(app)

    return app

app = create_app()

from sightapp import admin_route,center_route,tourist_route,models,myforms
