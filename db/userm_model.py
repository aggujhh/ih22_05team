from . import db


class Userm_model:
    # idとパスワードの確認
    def user_authentication(self, id, password):
        print(id, password)
        with db as cursor:
            cursor.execute("select user_id from userm where user_id=%s and user_password=%s", (id, password))
            result = cursor.fetchall()
        return result

