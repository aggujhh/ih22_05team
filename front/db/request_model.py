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
                    if not i == "":
                        cursor.execute("INSERT INTO request_category(request_id, category_name) "
                                       "VALUES (%s ,%s)", (request_id, i))
                amount = int(data_list["amount"]) if data_list.get("amount") is not None else None
                cursor.execute(
                    "INSERT INTO request_other(request_id, experience, fabric_material, reproducibility, reference_material, reply_frequency, request_budget, required_points, required_amount) "
                    "VALUES (%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s)",
                    (request_id, data_list["option_1"], data_list["option_2"], data_list["option_3"],
                     data_list["option_4"], data_list["option_5"], data_list["option_6"], data_list["want_point"],
                     amount))
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

    def fetch_all_requests(self):
        logger.info(f"fetch_all_requests 実行開始")
        try:
            with db as cursor:
                cursor.execute("SELECT "
                               "request_details.request_id, "
                               "request_details.request_title, "
                               "request_details.request_status, "
                               "request_details.request_deadline, "
                               "(SELECT photo_name "
                               "FROM request_img "
                               "WHERE request_img.request_id = request_details.request_id "
                               "LIMIT 1 ) AS photo_name,"
                               "(SELECT user_id "
                               "FROM request "
                               "WHERE request.request_id = request_details.request_id "
                               "LIMIT 1 ) AS user_id "
                               "FROM request_details "
                               "LIMIT 0, 8")
                results = cursor.fetchall()
                for result in results:
                    request_id = result['request_id']
                    cursor.execute(
                        "SELECT category_name "
                        "FROM request_category "
                        "WHERE request_category.request_id = %s", (request_id,)
                    )
                    result['categories'] = [row['category_name'] for row in cursor.fetchall()][::-1]
                cursor.execute("SELECT COUNT(*) "
                               "FROM request_details ")
                count = cursor.fetchone()
            logger.info(f"fetch_all_requests 実行成功しました。data,count>>> ${results, count}")
            return results, count
        except Exception as e:
            logger.error(f"fetch_all_requests 実行中にエラーが発生しました: {e}")
            return None

    def fetch_request_by_request_id(self, request_id):
        logger.info(f"fetch_request_by_request_id 実行開始、引数: {request_id}")
        try:
            with db as cursor:
                cursor.execute("SELECT request_details. *,"
                               "request_other. *,"
                               "profile.user_id,"
                               "profile.nickname,"
                               "profile.icon_url "
                               "FROM request_details "
                               "INNER JOIN request_other "
                               "ON request_details.request_id = request_other.request_id "
                               "INNER JOIN request "
                               "ON request_details.request_id = request.request_id "
                               "LEFT JOIN profile "
                               "ON profile.user_id = request.user_id "
                               "WHERE request_details.request_id = %s", request_id)
                result = cursor.fetchone()
                print(result)
                cursor.execute(
                    "SELECT category_name "
                    "FROM request_category "
                    "WHERE request_id = %s", request_id)
                result['categories'] = [row['category_name'] for row in cursor.fetchall()][::-1]
                cursor.execute(
                    "SELECT photo_name "
                    "FROM request_img "
                    "WHERE request_id = %s", request_id)
                result['photos'] = [row['photo_name'] for row in cursor.fetchall()]

            logger.info(f"fetch_request_by_request_id 実行成功しました。data >>> ${result}")
            return result
        except Exception as e:
            logger.error(f"fetch_request_by_request_id 実行中にエラーが発生しました: {e}")
            return None

    def load_requests(self, limit_start):
        logger.info(f"load_requests 実行開始,引数>>>{limit_start}")
        try:
            with db as cursor:
                cursor.execute("SELECT "
                               "request_details.request_id, "
                               "request_details.request_title, "
                               "request_details.request_status, "
                               "request_details.request_deadline, "
                               "(SELECT photo_name "
                               "FROM request_img "
                               "WHERE request_img.request_id = request_details.request_id "
                               "LIMIT 1 ) AS photo_name,"
                               "(SELECT user_id "
                               "FROM request "
                               "WHERE request.request_id = request_details.request_id "
                               "LIMIT 1 ) AS user_id "
                               "FROM request_details "
                               "LIMIT %s, 8", limit_start)
                results = cursor.fetchall()
                for result in results:
                    request_id = result['request_id']
                    cursor.execute(
                        "SELECT category_name "
                        "FROM request_category "
                        "WHERE request_category.request_id = %s", (request_id,)
                    )
                    result['categories'] = [row['category_name'] for row in cursor.fetchall()][::-1]
            logger.info(f"load_requests 実行成功しました。data>>> ${results}")
            return results
        except Exception as e:
            logger.error(f"load_requests 実行中にエラーが発生しました: {e}")
            return None
