from . import db
from routes import logger


class Creator_model:
    def fetch_all_creators(self):
        logger.info(f"fetch_all_creators 実行開始")
        try:
            with db as cursor:
                cursor.execute("SELECT creator.user_id, "
                               "creator.request_availability, "
                               "creator.creator_notification, "
                               "expertise.categorys, "
                               "design_preview.images, "
                               "profile.nickname, "
                               "profile.gender "
                               "FROM creator "
                               "INNER JOIN expertise "
                               "ON creator.user_id = expertise.user_id "
                               "INNER JOIN design_preview "
                               "ON creator.user_id = design_preview.user_id "
                               "INNER JOIN profile "
                               "ON creator.user_id = profile.user_id "
                               "LIMIT 0, 4")
                results = cursor.fetchall()
                cursor.execute("SELECT COUNT(*) "
                               "FROM creator")
                count = cursor.fetchone()
            logger.info(f"fetch_all_creators 実行成功しました。data,count>>> ${results, count}")
            return results, count
        except Exception as e:
            logger.error(f"fetch_all_creators 実行中にエラーが発生しました: {e}")
            return None

    def load_creators(self, limit_start):
        logger.info(f"load_creators 実行開始,引数>>>{limit_start}")
        try:
            with db as cursor:
                cursor.execute("SELECT creator.user_id, "
                               "creator.request_availability, "
                               "creator.creator_notification, "
                               "expertise.categorys, "
                               "design_preview.images, "
                               "profile.nickname, "
                               "profile.gender "
                               "FROM creator "
                               "INNER JOIN expertise "
                               "ON creator.user_id = expertise.user_id "
                               "INNER JOIN design_preview "
                               "ON creator.user_id = design_preview.user_id "
                               "INNER JOIN profile "
                               "ON creator.user_id = profile.user_id "
                               "LIMIT %s, 4", limit_start)
                results = cursor.fetchall()
            logger.info(f"load_creators 実行成功しました。data>>> ${results}")
            return results
        except Exception as e:
            logger.error(f"load_creators 実行中にエラーが発生しました: {e}")
            return None

    def fetch_creator_by_id(self, user_id):
        logger.info(f"fetch_creator_by_id 実行開始")
        try:
            with db as cursor:
                cursor.execute("SELECT creator.*, "
                               "expertise.categorys, "
                               "design_preview.images, "
                               "profile.* "
                               "FROM creator "
                               "INNER JOIN expertise "
                               "ON creator.user_id = expertise.user_id "
                               "INNER JOIN design_preview "
                               "ON creator.user_id = design_preview.user_id "
                               "INNER JOIN profile "
                               "ON creator.user_id = profile.user_id "
                               "WHERE creator.user_id=%s", user_id)
                result = cursor.fetchone()
            logger.info(f"fetch_creator_by_id 実行成功しました。data,count>>> ${result}")
            return result
        except Exception as e:
            logger.error(f"fetch_creator_by_id 実行中にエラーが発生しました: {e}")
            return None
