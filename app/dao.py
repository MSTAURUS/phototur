from app import db
from app.models import Users, System, Trips
from datetime import datetime
from typing import Dict, List


class UserDAO:
    def __int__(self):
        pass

    @staticmethod
    def create_superuser(login: str, password: str) -> None:
        usr: Users = Users()
        usr.set_password(password)
        usr.login = login
        usr.is_admin = 0
        usr.is_delete = 0
        usr.lastdate = datetime.now()
        usr.about = ""
        db.session.add(usr)
        db.session.commit()

    @staticmethod
    def get_by_login(login: str) -> Users:
        return Users.query.filter_by(login=login).first()
        # return [Users(**row) for row in rows]

    @staticmethod
    def get_by_id(id_user: int) -> List[Users]:
        return Users.query.filter_by(id=id_user).first()

    def check_login(self, login: str, password: str) -> bool:
        usr = self.get_by_login(login)

        check_pwd = usr.check_password(password)

        if check_pwd and usr:
            return True

        return False


class SystemDAO:
    def __init__(self, id_system: int):
        if id_system:
            self.sys = System.query.filter_by(id=id_system).first()
        else:
            self.sys = System()

    @staticmethod
    def get_system() -> List[System]:
        return System.query.first()

    def update(self, title: str, icon: str, bg_pic: str, main_video: str) -> None:
        self.sys.icon = icon
        self.sys.title = title
        self.sys.bg_pic = bg_pic
        self.sys.main_video = main_video

        # Если записей нет, то нужно создать
        if self.sys.id is None:
            db.session.add(self.sys)
        db.session.commit()


class TripsDAO:
    def __init__(self, id_trips: int):
        if id_trips:
            self.trips = Trips.query.filter_by(id=id_trips).first()
        else:
            self.trips = Trips()

    def get_trips(self) -> List[Trips]:
        return self.trips.query.add_columns(
            Trips.name,
            Trips.price,
            Trips.short_desc,
            Trips.description,
            Trips.photo_list,
            Trips.showed,
            Trips.id,
        )

    def get_trip(self) -> List[Trips]:
        # rows = self.trips.query.filter_by(id=id_trip).first()
        return self.trips

    def delete_trip(self) -> None:
        db.session.delete(self.trips)
        db.session.commit()

    def update(
        self,
        name: str,
        price: int,
        short_desc: str,
        description: str,
        photo_list: str,
        showed: bool,
    ):
        self.trips.name = name
        self.trips.price = price
        self.trips.short_desc = short_desc
        self.trips.description = description
        self.trips.photo_list = photo_list
        self.trips.showed = showed

        # Если записей нет, то нужно создать
        if self.trips.id is None:
            db.session.add(self.trips)
        db.session.commit()
