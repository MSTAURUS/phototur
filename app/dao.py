from app import db
from app.models import Users, System, Trips, Heads, Stories, Blog, Contacts
from datetime import datetime
from typing import List


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
        return bool(check_pwd and usr)


class SystemDAO:
    def __init__(self, id_system: int = None):
        if id_system:
            self.sys = System.query.filter_by(id=id_system).first()
        else:
            self.sys = System()

    def get_system(self) -> List[System]:
        return self.sys.query.first()

    def save(self, title: str, icon: str, bg_pic: str, main_video: str) -> None:
        self.sys.icon = icon
        self.sys.title = title
        self.sys.bg_pic = bg_pic
        self.sys.main_video = main_video

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
            Trips.id,
        )
        # rows = self.trips.query.add_columns(
        #     Trips.name,
        #     Trips.price,
        #     Trips.short_desc,
        #     Trips.description,
        #     Trips.photo_card,
        #     Trips.showed,
        #     Trips.id,
        # )
        #
        # return [Trips(**row) for row in rows]

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
        photo_list: str,
        showed: bool,
    ) -> None:
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

    def save(self, text: str, bg_text: str, up_head: str, down_head: str, pic: str, type_stories: str):
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

    def save(self, vk: str, instagram: str, telegram: str, email: str, phone: str, desc: str):
        self.contacts.vk = vk
        self.contacts.instagram = instagram
        self.contacts.telegram = telegram
        self.contacts.email = email
        self.contacts.phone = phone
        self.contacts.desc = desc

        if not self.contacts.id:
            db.session.add(self.contacts)

        db.session.commit()
