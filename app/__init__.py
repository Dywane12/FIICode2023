from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__,template_folder='templates')
app.config.from_object(Config)
database = SQLAlchemy(app)
migrate = Migrate(app, database)

from app import routes
from app.domain.entities import
