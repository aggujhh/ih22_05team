from . import db
from routes import logger


class inquiry_model:
    # お問い合わせたち取り出し
    def get_inquiries(self):
        try:
            with db as cursor:
                cursor.execute(
                    "SELECT inquiry_id, user_id, inquiry_name, inquiry_category, inquiry_time "
                    "FROM inquiry " 
                    "WHERE inquiry_status != '2' "
                )
                results = cursor.fetchall()
            return results
        except Exception as e:
            print('取り出し失敗',e)
    

    # お問い合わせ取り出し
    def get_inquiry(self,inquiry_id):
        with db as cursor:
            print('get_inquiry')
            cursor.execute(
                "SELECT * "
                "FROM inquiry "
                "WHERE inquiry_id = %s "
                , (inquiry_id,)
            )
            result = cursor.fetchone()
        return result

    # お問い合わせ修正
    def update_inquiry(self,data):
        try:
            print('update_inquiry')
            with db as cursor:
                cursor.execute(
                    "UPDATE INQUIRY "
                    "SET inquiry_status = %s, "
                    "    inquiry_contents = %s "
                    "WHERE inquiry_id = %s "
                    ,(data['inquiry_status'], data['inquiry_contents'], data['inquiry_id'],)
                )
            return 1
        except Exception as e:
            print('update_inquiry error',e)
            return 0

    # お知らせ削除
    def delete_notification(self,notification_id):
        try:
            print('delete_notification',notification_id)
            with db as cursor:
                cursor.execute(
                    "DELETE "
                    "FROM NOTIFICATION "
                    "WHERE notification_id = %s "
                    , (notification_id,)
                )
                #result = cursor.fetchone()
                #print(result)
            return 1
        except Exception as e:
            print('error',e)
            return 0

