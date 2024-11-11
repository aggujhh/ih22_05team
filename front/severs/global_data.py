from functools import wraps


def ensure_user_data(func):
    @wraps(func)
    def wrapper(self, user_id, *args, **kwargs):
        self._ensure_user(user_id)  # 初始化用户数据
        return func(self, user_id, *args, **kwargs)

    return wrapper


class GlobalData:
    def __init__(self):
        # 存储每个用户的数据，以 user_id 作为键
        self.users = {}
        self.mails = {}

    def _ensure_user(self, user_id):
        if user_id not in self.users:
            self.users[user_id] = {
                "nickname": "",
                "genre": ["", "", "", "", "", ""]
            }

    def _ensure_mail(self, mail):
        if mail not in self.mails:
            self.mails[mail] = {
                "incorrectPassword": 0,
            }

    @ensure_user_data
    def set_nickname(self, user_id, nickname):
        self.users[user_id]["nickname"] = nickname

    @ensure_user_data
    def get_nickname(self, user_id):
        return self.users[user_id]["nickname"]

    def del_user(self, user_id):
        if user_id in self.users:
            del self.users[user_id]

    def reset_incorrect_password(self, mail):
        self._ensure_mail(mail)
        self.mails[mail]["incorrectPassword"] = 0

    def increment_incorrect_password(self, mail):
        self._ensure_mail(mail)
        self.mails[mail]["incorrectPassword"] += 1
        return self.mails[mail]["incorrectPassword"]

    def del_incorrect_password(self, mail):
        if mail in self.mails:
            del self.mails[mail]

    @ensure_user_data
    def set_genre(self, user_id, genre):
        self.users[user_id]["genre"] = genre

    @ensure_user_data
    def get_genre(self, user_id):
        return self.users[user_id]["genre"]


global_data = GlobalData()
