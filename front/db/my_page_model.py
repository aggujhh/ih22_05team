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

    def fetch_creator_data_by_id(self, user_id):
        logger.info(f"fetch_creator_data_by_id関数　実行開始、引数: {user_id}")
        try:
            with (db as cursor):
                cursor.execute("SELECT * FROM creator WHERE user_id= %s", user_id)
                result = cursor.fetchone()
                if result:
                    cursor.execute(
                        "SELECT categorys "
                        "FROM expertise "
                        "WHERE user_id = %s", user_id)
                    result["categories"] = cursor.fetchone()['categorys'].split(",")
                    cursor.execute(
                        "SELECT images "
                        "FROM design_preview "
                        "WHERE user_id = %s", user_id)
                    images = cursor.fetchone()['images']
                    if images:
                        result['images'] = images.split(",")
                else:
                    cursor.execute(
                        "INSERT INTO creator(user_id, request_availability, owned_tools, creator_notification, creator_level) "
                        "VALUES (%s, '0', null, null, '0')", user_id)
                    cursor.execute(
                        "INSERT INTO expertise(user_id, categorys) "
                        "VALUES (%s, %s)", (user_id, '0,0,0,0,0,0'))
                    cursor.execute(
                        "INSERT INTO design_preview(user_id, images) "
                        "VALUES (%s, null)", user_id)
                    result = {
                        "request_availability": '0',
                        "owned_tools": "",
                        "creator_notification": "",
                        "creator_level": '0',
                        "categories": ['0', '0', '0', '0', '0', '0'],
                        'images': []
                    }
            logger.info(f"fetch_creator_data_by_id関数　実行成功しました。もらった結果: {result}")
            return result
        except Exception as e:
            logger.error(f"fetch_creator_data_by_id関数 実行中にエラーが発生しました: {e}")
            return None

    def update_creator(self, user_id, data):
        logger.info(f"update_creator関数　実行開始、引数: {user_id, data}")
        try:
            with db as cursor:
                cursor.execute(
                    "UPDATE creator "
                    "SET request_availability = %s,"
                    "owned_tools = %s,"
                    "creator_notification = %s "
                    "WHERE user_id = %s",
                    (data['request_availability'], data['owned_tools'], data['details'], user_id))
                cursor.execute(
                    "UPDATE expertise "
                    "SET categorys = %s "
                    "WHERE user_id = %s", (data['expertise'].strip("[]"), user_id))
                cursor.execute(
                    "UPDATE design_preview "
                    "SET images = %s "
                    "WHERE user_id = %s", (",".join(data['image']), user_id))
            logger.info(f"update_creator関数　実行成功しました。")
            return True
        except Exception as e:
            logger.error(f"update_creator関数 実行中にエラーが発生しました: {e}")
            return False
