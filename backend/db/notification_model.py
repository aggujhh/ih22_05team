from . import db
from routes import logger


class notification_model:
    # お知らせたち取り出し
    def get_notifications(self):
        with db as cursor:
            cursor.execute(
                "SELECT notification_id, notification_title, notification_post_time, notification_content "
                "FROM NOTIFICATION " 
                "WHERE notification_post_status IN ('0','1') "
            )
            results = cursor.fetchall()
        return results
    
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
                    "SELECT * "
                    "FROM NOTIFICATION "
                    "WHERE notification_id = %s "
                    , (notification_id,)
                )
                result = cursor.fetchone()
                print(result)
            return 1
        except Exception as e:
            print('error',e)
            return 0