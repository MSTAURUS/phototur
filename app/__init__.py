import logging
import os
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

login = LoginManager(app)
login.login_view = "login"
login.login_message = "Авторизуйтесь для доступа к этой странице."

if not app.debug:
    if not os.path.exists("log"):
        os.mkdir("log")
    file_handler = RotatingFileHandler(
        "log/phototur.log", maxBytes=1000000, backupCount=10
    )
    file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
        )
    )
    file_handler.setLevel(logging.ERROR)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.ERROR)
    app.logger.info("Phototur startup")

from app import dao, errors, models, routes  # noqa: F401,E402
