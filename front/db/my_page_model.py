from . import db
from routes import logger


class My_page_model():

    def fetch_profile_by_id(self, user_id):
        logger.info(f"fetch_profile_by_id関数　実行開始、引数: {user_id}")
        try:
            with db as cursor:
                cursor.execute("SELECT * FROM profile WHERE user_id= %s", user_id)
                result = cursor.fetchone()
            logger.info(f"fetch_profile_by_id関数　実行成功しました。もらった結果: {result}")
            return result
        except Exception as e:
            logger.error(f"fetch_profile_by_id関数 実行中にエラーが発生しました: {e}")
            return None

    def update_profile(self, user_id, data):
        logger.info(f"update_profile関数　実行開始、引数: {user_id, data}")
        try:
            with db as cursor:
                cursor.execute(
                    "UPDATE profile "
                    "SET nickname=%s ,gender=%s ,profile=%s ,hobby=%s "
                    "WHERE user_id=%s ",
                    (data['nickname'], data['gender'], data['profile'], data['hobby'], user_id))
            logger.info(f"update_profile関数　実行成功しました。")
            return True
        except Exception as e:
            logger.error(f"update_profile関数 実行中にエラーが発生しました: {e}")
            return False

    def update_profile_images(self, user_id, data):
        logger.info(f"update_profile_images関数　実行開始、引数: {user_id, data}")
        try:
            with db as cursor:
                cursor.execute(
                    "UPDATE profile "
                    "SET icon_url=%s ,background_photo_url=%s "
                    "WHERE user_id=%s ",
                    (data['icon_url'], data['background_photo_url'], user_id))
            logger.info(f"update_profile_images関数　実行成功しました。")
            return True
        except Exception as e:
            logger.error(f"update_profile_images関数 実行中にエラーが発生しました: {e}")
            return False
