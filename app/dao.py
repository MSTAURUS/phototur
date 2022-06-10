from app import db
from app.models import Users
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
        usr.about = ''
        db.session.add(usr)
        db.session.commit()

    @staticmethod
    def get_by_login(login: str) -> Users:
        return Users.query.filter_by(login=login).first()
        # return [Users(**row) for row in rows]

    @staticmethod
    def get_by_id(id_user: int) -> List[Users]:
        rows: Users = Users.query.filter_by(id=id_user).first()
        return [Users(**row) for row in rows]

    def check_login(self, login: str, password: str) -> bool:
        usr = self.get_by_login(login)

        check_pwd = usr.check_password(password)

        if check_pwd and usr:
            return True

        return False

# def qqqqqq(self, is_admin) -> List[User]:
#     rows = User.query.filter(is_admin=is_admin).fetch_all
#     [User(**row) for row in rows]
