import os
from flask import Flask    # 1
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)      # 2

app.config.from_object(Config)
db: SQLAlchemy = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models     # 3

app.config["SECRET_KEY"] = os.urandom(12)

