from datetime import datetime
from time import time
from typing import Optional

import jwt
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import app, db, login


class Staff(db.Model):
    """
    Класс для "нашей" команды
    """

    __tablename__ = "staff"
    id: Optional[int] = db.Column(db.Integer, primary_key=True)
    name: Optional[str] = db.Column(db.String(20))
    description: Optional[str] = db.Column(db.String(128))
    vk: Optional[str] = db.Column(db.String(128))
    instagram: Optional[str] = db.Column(db.String(128))
    telegram: Optional[str] = db.Column(db.String(128))
    photo_card: Optional[str] = db.Column(db.String)

    def __repr__(self):
        return f"<Staffs {self.name}>"


class Users(db.Model, UserMixin):
    """
    Класс пользователей
    """

    __tablename__ = "users"
    id: Optional[int] = db.Column(db.Integer, primary_key=True)
    login: Optional[str] = db.Column(db.String(20), unique=True)
    name: Optional[str] = db.Column(db.String(20), unique=True)
    is_admin: Optional[int] = db.Column(db.Integer)
    is_delete: Optional[int] = db.Column(db.Integer)
    lastdate: Optional[datetime] = db.Column(db.DateTime, default=datetime.utcnow)
    password_hash: Optional[str] = db.Column(db.String(128))
    about: Optional[str] = db.Column(db.String(200))

    def __repr__(self):
        return f"<Users {self.login}>"

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600) -> str:
        return jwt.encode(
            {"reset_password": self.id, "exp": time() + expires_in},
            app.config["SECRET_KEY"],
            algorithm="HS256",
        ).decode("utf-8")

    def get_id(self) -> int:
        return self.id


class Trips(db.Model):
    """
    Класс путешествий
    """

    __tablename__ = "trips"
    id: Optional[int] = db.Column(db.Integer, primary_key=True)
    name: Optional[str] = db.Column(db.String(20), nullable=False)
    price: Optional[int] = db.Column(db.Integer, nullable=False)
    short_desc: Optional[str] = db.Column(db.String(33))
    description: Optional[str] = db.Column(db.String)
    photo_card: Optional[str] = db.Column(db.String)
    showed: Optional[bool] = db.Column(db.Integer)
    date_start: Optional[datetime] = db.Column(db.DateTime)
    date_finish: Optional[datetime] = db.Column(db.DateTime)

    def __repr__(self):
        return f"<Trips {self.name}>"


class Contacts(db.Model):
    """
    Класс для контактов
    """

    __tablename__ = "contacts"
    id: Optional[int] = db.Column(db.Integer, primary_key=True)
    vk: Optional[str] = db.Column(db.String(128))
    instagram: Optional[str] = db.Column(db.String(128))
    telegram: Optional[str] = db.Column(db.String(128))
    whatsapp: Optional[str] = db.Column(db.String(128))
    email: Optional[str] = db.Column(db.String(128))
    phone: Optional[str] = db.Column(db.String(128))
    desc: Optional[str] = db.Column(db.String(256))


class Blog(db.Model):
    """
    Класс для блога
    """

    __tablename__ = "blog"
    id: Optional[int] = db.Column(db.Integer, primary_key=True)
    id_user: Optional[int] = db.Column(db.Integer, db.ForeignKey("users.id"))
    short_text: Optional[str] = db.Column(db.String(136))
    long_text: Optional[str] = db.Column(db.String)
    pic: Optional[str] = db.Column(db.String(256))
    showed: Optional[bool] = db.Column(db.Integer)
    lastdate: Optional[datetime] = db.Column(db.DateTime, default=datetime.utcnow)


class Heads(db.Model):
    """
    Класс для заголовков
    """

    __tablename__ = "heads"
    id: Optional[int] = db.Column(db.Integer, primary_key=True)
    title: Optional[str] = db.Column(db.String(100))
    description: Optional[str] = db.Column(db.String(200))
    type_head: Optional[str] = db.Column(db.String(20), index=True, unique=True)


class System(db.Model):
    """
    Класс для общих данных
    """

    __tablename__ = "system"
    id: Optional[int] = db.Column(db.Integer, primary_key=True)
    title: Optional[str] = db.Column(db.String(20))
    icon: Optional[str] = db.Column(db.String(256))
    bg_pic: Optional[str] = db.Column(db.String(256))
    main_video: Optional[str] = db.Column(db.String(1024))
    statistic: Optional[str] = db.Column(db.String)


class Stories(db.Model):
    """
    Класс для историй
    """

    __tablename__ = "stories"
    id: Optional[int] = db.Column(db.Integer, primary_key=True)
    text: Optional[str] = db.Column(db.String(255))
    pic: Optional[str] = db.Column(db.String(256))
    bg_text: Optional[str] = db.Column(db.String(20))
    up_head: Optional[str] = db.Column(db.String(20))
    down_head: Optional[str] = db.Column(db.String(20))
    type_stories: Optional[str] = db.Column(db.String(20), unique=True)


@login.user_loader
def load_user(id_user):
    return Users.query.filter_by(id=id_user).first()
