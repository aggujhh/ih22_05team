from . import db


class Userm_model:
    # idとパスワードの確認
    def user_authentication(self, id):
        print(id)
        with db as cursor:
            cursor.execute("select user_password from userm where user_id=%s", id)
            result = cursor.fetchone()
        return result

    def add_user(self, user):
        print(user)
        with db as cursor:
            cursor.execute("INSERT INTO userm(user_id, user_password, user_type, user_status, create_time)"
                           "VALUES (%s, %s, %s, 0, NOW())",
                           (user["user_id"], user["user_password"], user["user_type"]))
            cursor.execute("INSERT INTO user_infom(user_id, user_email_address)"
                           "VALUES (%s, %s)",
                           (user["user_id"], user["user_email_address"]))
            cursor.execute("INSERT INTO profile(user_id, nickname)"
                           "VALUES (%s, %s)",
                           (user["user_id"], user["nickname"]))

