import os
from os import environ

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DB_SERVER = environ.get("DB_SERVER") or "127.0.0.1"
    DB_LOGIN = environ.get("DB_LOGIN") or "phototur"
    DB_PASSWORD = environ.get("DB_PASSWORD") or "K554fase6u"

    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_LOGIN}:{DB_PASSWORD}@{DB_SERVER}/phototur?charset=utf8mb4"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ADMINS = ["a@b.org"]
    POSTS_PER_PAGE = 25
