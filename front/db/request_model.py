from . import db
from routes import logger

class Request_model:
    def add_request(self, user_id, request_id, data_list):
        logger.info(f"add_request 実行開始、引数: {user_id, request_id, data_list}")
        try:
            with db as cursor:
                cursor.execute(
                    "INSERT INTO request_details(request_id, request_title, request_content, request_status, request_deadline) "
                    "VALUES (%s ,%s ,%s ,%s ,%s)",
                    (request_id, data_list["title"], data_list["details"], 0,
                     f"{data_list['year']}-{data_list['moon']}-{data_list['day']}"))
                cursor.execute("insert into request(user_id, request_id) "
                               "values (%s ,%s)", (user_id, request_id))
                for i in data_list["genre"]:
                    cursor.execute("INSERT INTO request_category(request_id, category_name) "
                                   "VALUES (%s ,%s)", (request_id, i))
                cursor.execute(
                    "INSERT INTO request_other(request_id, experience, fabric_material, reproducibility, reference_material, reply_frequency, request_budget, required_points, required_amount) "
                    "VALUES (%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s)",
                    (request_id, data_list["option_1"], data_list["option_2"], data_list["option_3"],
                     data_list["option_4"], data_list["option_5"], data_list["option_6"], data_list["want_point"],
                     data_list["amount"]))
                logger.info("add_request 実行成功しました。")
                return True
        except Exception as e:
            logger.error(f"add_request 実行中にエラーが発生しました: {e}")
            return False

    def add_request_image_file_name(self, request_id, image_name):
        logger.info(f"add_request_image_file_name 実行開始、引数: {request_id, image_name}")
        try:
            with db as cursor:
                cursor.execute("insert into request_img(request_id, photo_name) "
                               "values (%s ,%s) ", (request_id, image_name))
                logger.info("add_request_image_file_name 実行成功しました。")
                return True
        except Exception as e:
            logger.error(f"add_request_image_file_name 実行中にエラーが発生しました: {e}")
            return False

    def have_request_id(self, request_id):
        logger.info(f"have_request_id 実行開始、引数: {request_id}")
        try:
            with db as cursor:
                cursor.execute("SELECT * FROM request WHERE request_id = %s", id)
                result = cursor.fetchone()
            return result
        except Exception as e:
            logger.error(f"have_request_id 実行中にエラーが発生しました: {e}")
            return None
