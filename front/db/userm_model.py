from . import db
from routes import logger


class Userm_model:
    # ログイン
    def login(self, mail_address):
        print(mail_address)
        with db as cursor:
            cursor.execute("SELECT userm.user_id,user_password "
                           "FROM userm "
                           "INNER JOIN user_infom "
                           "ON userm.user_id = user_infom.user_id "
                           "WHERE user_email_address = %s"
                           , mail_address)
            result = cursor.fetchone()
        return result

    # idの確認
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

    def add_creator_application(self, user):
        print(user)
        with db as cursor:
            cursor.execute(
                "INSERT INTO producer_app(creator_application_id, creator_nickname_id, creator_mail, creator_password, creator_tel, creator_history, creator_application_status) "
                "VALUES (%s, %s, %s, %s, %s, %s, 0)",
                (user["user_id"], user["nickname"], user["user_email_address"], user["user_password"], user["tel"],
                 user["creator_history"]))

            for i in user["creator_image"]:
                cursor.execute("INSERT INTO img_app(creator_application_id, product_image_url)"
                               "VALUES (%s, %s)",
                               (user["user_id"], i))

    def have_creator_id(self, id):
        print(id)
        with db as cursor:
            cursor.execute("SELECT * FROM producer_app WHERE creator_application_id = %s", id)
            result = cursor.fetchone()
        return result

    def reset_ps(self, mail, ps):
        print("reset_ps", mail, ps)
        with db as cursor:
            cursor.execute("SELECT user_id "
                           "FROM user_infom "
                           "WHERE user_email_address= %s", mail)
            result = cursor.fetchone()
            cursor.execute("UPDATE userm "
                           "SET user_password= %s "
                           "WHERE user_id= %s ", (ps, result["user_id"]))
        logger.info("パスワードの再設定が成功しました")

    def fetch_nickname_by_userid(self, user_id):
        logger.info(f"fetch_nickname_by_userid関数 実行開始、引数:{user_id}")
        try:
            with db as cursor:
                cursor.execute("SELECT nickname "
                               "FROM profile "
                               "WHERE user_id = %s", user_id)
                result = cursor.fetchone()
                if result:
                    logger.info(f"ネックネーム: {result['nickname']} を取得しました")
                    return result['nickname']
                else:
                    logger.warning("ニックネームが見つかりません")
                    return None
        except Exception as e:
            logger.error(f"fetch_nickname_by_userid関数 実行中にエラーが発生しました: {e}")
            return None

    def get_avatar(self, user_id):
        logger.info(f"get_avatar関数 実行開始、引数:{user_id}")
        try:
            with db as cursor:
                cursor.execute("SELECT icon_url "
                               "FROM profile "
                               "WHERE user_id = %s", user_id)
                result = cursor.fetchone()
                if result:
                    logger.info(f"アバター: {result['icon_url']} を取得しました")
                    return result['icon_url']
                else:
                    logger.warning("アバターが見つかりません")
                    return None
        except Exception as e:
            logger.error(f"get_avatar関数 実行中にエラーが発生しました: {e}")
            return None
