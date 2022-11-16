import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://phototur:K554fase6u@127.0.0.1/phototur?charset=utf8mb4"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ADMINS = ["a@b.org"]
    POSTS_PER_PAGE = 25
