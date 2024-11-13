from . import db
from routes import logger




class creator_request_model:
    def get_creator_list(self):
        try:
            print('get_creator_list')
            with db as cursor:
                cursor.execute(
                    "SELECT * "
                    "FROM PRODUCER_APP "
                )
                results = cursor.fetchall()
            print('results',results)
            return results
        except Exception as e:
            print(f"情報取り出しに失敗しました。{e}")
    
    def get_detail(self,creator_application_id):
        try:
            print('get_detail')
            with db as cursor:
                cursor.execute(
                    "SELECT * "
                    "FROM PRODUCER_APP "
                    "WHERE creator_application_id = %s "
                    ,(creator_application_id,)
                )
                result = cursor.fetchone()
                cursor.execute(
                    "SELECT product_image_url "
                    "FROM IMG_APP "
                    "WHERE creator_application_id = %s "
                    ,(creator_application_id,)
                )
                result['product_image_url'] = cursor.fetchall()
            return result
        except Exception as e:
            print('情報の取り出しに失敗',e)
            return 0