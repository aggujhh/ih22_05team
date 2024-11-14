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
                )
                results = cursor.fetchall()
            return results
        except Exception as e:
            print('取り出し失敗',e)
    
    # お知らせ追加
    def add_notification(self,notification):
        try:
            print('add_notification')
            with db as cursor:
                cursor.execute(
                    "INSERT INTO NOTIFICATION(notification_title, notification_post_status, notification_post_time, notification_content) "
                    "VALUES(%s, %s, %s, %s) "
                    , (notification['notification_title'], notification['notification_post_status'], notification['notification_post_time'], notification['notification_content'], )
                )
            return 1
        except Exception as e:
            print('add_notification error',e)
            return 0

    # お知らせ取り出し
    def get_notification(self,notification_id):
        with db as cursor:
            cursor.execute(
                "SELECT notification_id, notification_title, notification_content, notification_post_time "
                "FROM NOTIFICATION "
                "WHERE notification_id = %s "
                , (notification_id,)
            )
            result = cursor.fetchone()
        return result

    # お知らせ修正
    def update_notification(self,notification):
        try:
            print('add_notification')
            with db as cursor:
                cursor.execute(
                    "UPDATE NOTIFICATION "
                    "SET notification_title = %s, "
                    "    notification_post_status = %s, "
                    "    notification_post_time = %s, "
                    "    notification_content = %s "
                    "WHERE notification_id = %s "
                    ,(notification['notification_title'], notification['notification_post_status'], notification['notification_post_time'], notification['notification_content'], notification['notification_id'], )
                )
            return 1
        except Exception as e:
            print('update_notification error',e)
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