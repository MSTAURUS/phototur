from datetime import datetime
from typing import List

from app import db
from app.models import Blog, Contacts, Heads, Staff, Stories, System, Trips, Users


class UserDAO:
    def __init__(self, id_user: int = None):
        if id_user:
            self.user = Users.query.filter_by(id=id_user).first()
        else:
            self.user = Users()
        # pass

    def create_superuser(
        self, login: str, name: str, password: str, about: str, is_admin: bool
    ) -> None:
        if password:
            self.user.set_password(password)
        self.user.login = login
        self.user.name = name
        self.user.is_admin = is_admin
        self.user.is_delete = 0
        self.user.lastdate = datetime.now()
        self.user.about = about
        db.session.add(self.user)
        db.session.commit()

    def get_users(self) -> List[Users]:
        return self.user.query.add_columns(
            Users.login,
            Users.name,
            Users.is_admin,
            Users.is_delete,
            Users.password_hash,
            Users.id,
            Users.about,
        )

    def get_user(self) -> List[Users]:
        return self.user

    def delete_user(self) -> None:
        db.session.delete(self.user)
        db.session.commit()
        #
        # def save(
        #     self,
        #     login,
        #     name,
        #     is_admin,
        #     is_delete,
        #     password_hash,
        #     about,
        # ) -> None:
        #     self.user.login = login
        #     self.user.name = name
        #     self.user.is_admin = is_admin
        #     self.user.is_delete = is_delete
        #     self.user.password_hash = password_hash
        #     self.user.about = about
        #
        #     # Если записей нет, то нужно создать
        #     if self.user.id is None:
        #         db.session.add(self.user)
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
        check_pwd: bool = False
        if usr:
            check_pwd = usr.check_password(password)
        return bool(check_pwd and usr)


class SystemDAO:
    def __init__(self, id_system: int = None):
        if id_system:
            self.sys = System.query.filter_by(id=id_system).first()
        else:
            self.sys = System()

    def get_system(self) -> List[System]:
        return self.sys.query.first()

    def save(
        self, title: str, icon: str, bg_pic: str, main_video: str, statistic: str
    ) -> None:
        self.sys.icon = icon
        self.sys.title = title
        self.sys.bg_pic = bg_pic
        self.sys.main_video = main_video
        if statistic:
            self.sys.statistic = statistic

        # Если записей нет, то нужно создать
        if self.sys.id is None:
            db.session.add(self.sys)
        db.session.commit()

    def save_statistic(self, statistic: str) -> None:
        self.sys.statistic = statistic

        # Если записей нет, то нужно создать
        if self.sys.id is None:
            db.session.add(self.sys)
        db.session.commit()


class TripsDAO:
    def __init__(self, id_trips: int = None):
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
            Trips.photo_card,
            Trips.showed,
            Trips.date_start,
            Trips.date_finish,
            Trips.id,
        )

    def get_showed_trips(self, limit: int = 1000) -> List[Trips]:
        return (
            self.trips.query.add_columns(
                Trips.name,
                Trips.price,
                Trips.short_desc,
                Trips.description,
                Trips.photo_card,
                Trips.showed,
                Trips.date_start,
                Trips.date_finish,
                Trips.id,
            )
            .filter(Trips.showed == 1)
            .limit(limit)
        )

    def get_trip(self) -> List[Trips]:
        # rows = self.trips.query.filter_by(id=id_trip).first()
        return self.trips

    def delete_trip(self) -> None:
        db.session.delete(self.trips)
        db.session.commit()

    def save(
        self,
        name: str,
        price: int,
        short_desc: str,
        description: str,
        photo_card: str,
        showed: bool,
        date_start: datetime,
        date_finish: datetime,
    ) -> None:
        self.trips.name = name
        self.trips.price = price
        self.trips.short_desc = short_desc
        self.trips.description = description
        self.trips.photo_card = photo_card
        self.trips.showed = showed
        self.trips.date_start = date_start
        self.trips.date_finish = date_finish

        # Если записей нет, то нужно создать
        if self.trips.id is None:
            db.session.add(self.trips)
        db.session.commit()


class HeadsDAO:
    def __init__(self, type_head: str = None):
        self.head = Heads.query.filter_by(type_head=type_head).first()
        if not type_head or self.head is None:
            self.head = Heads()

    def get_head(self) -> List[Heads]:
        return self.head

    def save(self, title: str, description: str, type_head: str) -> None:
        self.head.title = title
        self.head.description = description

        if not self.head.id:
            self.head.type_head = type_head
            db.session.add(self.head)

        db.session.commit()


class BlogDAO:
    def __init__(self):
        pass

    def get_last_blog_record(self) -> List[Blog]:
        return []


class StoriesDAO:
    def __init__(self, type_stories: str = None):
        self.story = Stories.query.filter_by(type_stories=type_stories).first()
        # get вместо фёрст +фильтр?
        if not type_stories or self.story is None:
            self.story = Stories()

    def get_story(self) -> List[Stories]:
        return self.story

    def save(
        self,
        text: str,
        bg_text: str,
        up_head: str,
        down_head: str,
        pic: str,
        type_stories: str,
    ):
        self.story.text = text
        self.story.bg_text = bg_text
        self.story.up_head = up_head
        self.story.down_head = down_head
        self.story.pic = pic

        if not self.story.id:
            self.story.type_stories = type_stories
            db.session.add(self.story)
        db.session.commit()


class ContactsDAO:
    def __init__(self):
        self.contacts = Contacts.query.first()
        if self.contacts is None:
            self.contacts = Contacts()

    def get_contacts(self) -> List[Contacts]:
        return self.contacts

    def save(
        self,
        vk: str,
        instagram: str,
        telegram: str,
        whatsapp: str,
        email: str,
        phone: str,
        desc: str,
    ):
        self.contacts.vk = vk
        self.contacts.instagram = instagram
        self.contacts.telegram = telegram
        self.contacts.whatsapp = whatsapp
        self.contacts.email = email
        self.contacts.phone = phone
        self.contacts.desc = desc

        if not self.contacts.id:
            db.session.add(self.contacts)

        db.session.commit()


class StaffDAO:
    def __init__(self, id_empl: int = None):
        if id_empl:
            self.empl = Staff.query.filter_by(id=id_empl).first()
        else:
            self.empl = Staff()

    def get_staff(self) -> List[Staff]:
        return self.empl.query.add_columns(
            Staff.name,
            Staff.description,
            Staff.vk,
            Staff.instagram,
            Staff.telegram,
            Staff.id,
            Staff.photo_card,
        )

    def get_empl(self) -> List[Staff]:
        return self.empl

    def delete_empl(self) -> None:
        db.session.delete(self.empl)
        db.session.commit()

    def save(
        self,
        name: str,
        description: str,
        vk: str,
        instagram: str,
        telegram: str,
        photo_card: str,
    ) -> None:
        self.empl.name = name
        self.empl.description = description
        self.empl.vk = vk
        self.empl.instagram = instagram
        self.empl.telegram = telegram
        self.empl.photo_card = photo_card

        # Если записей нет, то нужно создать
        if self.empl.id is None:
            db.session.add(self.empl)
        db.session.commit()
