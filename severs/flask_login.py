from flask_login import UserMixin, login_user
from db.userm_model import Userm_model


class User(UserMixin):
    def __init__(self, id):
        self.id = id

class Flask_login:
    def check_login(self, id: str, password: str) -> bool:
        result = Userm_model().user_authentication(id, password)
        if result:
            login_user(User(id))
            return True
        return False
