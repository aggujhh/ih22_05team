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
                    "WHERE creator_application_status = '0' "
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
                r = cursor.fetchall()
                result['product_image_url'] = r
                print(result)
            return result
        except Exception as e:
            print('情報の取り出しに失敗',e)
            return 0
    
    # 制作物の画像を登録
    def add_img(self,creator):
        try:
            print('add_img')
            user_id = creator['creator_application_id']
            with db as cursor:
                for image_url in creator['product_image_url']['product_image_url']:
                    cursor.execute(
                        "INSERT INTO DESIGN_PREVIEW(user_id, image_url) "
                        "VALUES(%s, %s, %s) "
                        , (user_id, image_url,)
                    )
        except Exception as e:
            print('登録に失敗',e)
    
    # 制作者申請の状態を変更
    def change_status(self,creator_application_id, status):
        try:
            print('change_status',creator_application_id,status)
            with db as cursor:
                cursor.execute(
                    "UPDATE PRODUCER_APP "
                    "SET creator_application_status = %s "
                    "WHERE creator_application_id = %s "
                    , (status, creator_application_id,)
                )
        except Exception as e:
            print('更新失敗',e)
    

    # 申請承認された制作者の情報をDBに登録
    def add_user(self, user):
        try:
            print('add_user',user)
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
        except Exception as e:
            print('登録失敗',e)