from . import db
from routes import logger




class Inquiry_model:
    def add_inquiry(self, user_id, data):
        logger.info(f"add_inquiry関数　実行開始、引数: {data}")
        try:
            with db as cursor:
                cursor.execute(
                    "INSERT INTO inquiry(user_id, inquiry_name, inquiry_mail, inquiry_category, inquiry_contents, inquiry_time, inquiry_status) "
                    "VALUES (%s ,%s ,%s ,%s ,%s ,now() ,0 );",
                    (user_id, data["name"], data["email"], data["category"], data["inquiry_contents"]))
            logger.info(f"add_inquiry関数　実行成功しました。")
            return True
        except Exception as e:
            logger.error(f"add_inquiry関数 実行中にエラーが発生しました: {e}")
            return False
