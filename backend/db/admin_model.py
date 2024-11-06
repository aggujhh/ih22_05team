from . import db
from routes import logger

class admin_model:
    # ログイン
    def login(self, id):
        print(id)
        with db as cursor:
            cursor.execute("SELECT admin_id, admin_password, password_expiration_date, admin_permissions "
                           "FROM ADMIN "
                           "WHERE admin_id = %s",
                           (id,)
            )
            result = cursor.fetchone()
        return result

    # idの確認
    def admin_authentication(self, id):
        print(id)
        with db as cursor:
            cursor.execute("select admin_password from ADMIN where admin_id=%s", id)
            result = cursor.fetchone()
        return result

