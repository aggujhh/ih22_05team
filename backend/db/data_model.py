from . import db
from routes import logger

class data_model:
    def get_users(self):
        try:
            print('get_data')
            with db as cursor:
                cursor.execute(
                    "SELECT COUNT(user_id) AS USER_NUM, create_time "
                    "FROM USERM "
                    "WHERE user_type='0' "
                    "GROUP BY user_type, create_time "
                    "ORDER BY create_time "
                )
                requester = cursor.fetchall()
                cursor.execute(
                    "SELECT COUNT(user_id) AS USER_NUM, create_time "
                    "FROM USERM "
                    "WHERE user_type='1' "
                    "GROUP BY user_type, create_time "
                    "ORDER BY create_time "
                )
                creator = cursor.fetchall()
            return requester,creator
        except Exception as e:
            print('情報取得失敗',e)
    
    def get_request(self):
        try:
            print('get_request')
            with db as cursor:
                cursor.execute(
                    "SELECT COUNT(request_deadline) AS request_num, request_deadline AS time "
                    "FROM REQUEST AS r "
                    "LEFT JOIN REQUEST_DETAILS AS rd "
                    "ON r.request_id = rd.request_id "
                    "GROUP BY request_deadline "
                    "ORDER BY request_deadline "
                )
                result = cursor.fetchall()
            print('情報取得成功')
            return result
        except Exception as e:
            print('情報取得失敗',e)

    def get_contract(self):
        try:
            print('get_contract')
            with db as cursor:
                cursor.execute(
                    "SELECT COUNT(request_id) AS contract, SUM(contract_amount) AS amount, contract_timestamp AS time "
                    "FROM REQUEST_HISTORY "
                    "GROUP BY contract_timestamp "
                    "ORDER BY contract_timestamp "
                )
                result = cursor.fetchall()
            print('情報取得成功')
            return result
        except Exception as e:
            print('情報取得失敗',e)
