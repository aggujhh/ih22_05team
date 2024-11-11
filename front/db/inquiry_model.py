from . import db
from routes import logger


class Inquiry_model:
    def add_inquiry(self, data):
        pass
        # logger.info(f"add_inquiry関数　実行開始、引数: {data}")
        # try:
        #     with db as cursor:
        #         cursor.execute("SELECT * FROM request WHERE request_id = %s", id)
        #         result = cursor.fetchone()
        #     return result
        # except Exception as e:
        #     logger.error(f"add_inquiry関数 実行中にエラーが発生しました: {e}")
        #     return None
