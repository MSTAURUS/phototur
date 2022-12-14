import logging
import os
from logging.handlers import RotatingFileHandler
from typing import List

from flask import Flask, render_template
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

login = LoginManager(app)
login.login_view = 'login'
login.login_message = 'Авторизуйтесь для доступа к этой странице.'

if not app.debug:
    if not os.path.exists('log'):
        os.mkdir('log')
    file_handler = RotatingFileHandler('log/phototur.log', maxBytes=1000000,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.ERROR)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.ERROR)
    app.logger.info('Phototur startup')

from app import routes, models, errors, dao


@app.errorhandler(404)
def page_not_found(e):
    system: List[models.System] = routes.get_system_info()
    return render_template('404.tmpl', system=system, head_info=[]), 404


@app.errorhandler(500)
def server_error(e):
    system: List[models.System] = routes.get_system_info()
    return render_template('500.tmpl', system=system, head_info=[]), 500
