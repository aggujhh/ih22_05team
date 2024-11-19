from . import db

class notification_model:
    # お知らせたち取り出し
    def get_notifications(self):
        print("get notifications")
        with db as cursor:
            cursor.execute(
                "SELECT notification_id, notification_title, notification_post_time, notification_content "
                "FROM NOTIFICATION " 
                "WHERE notification_post_status IN ('0','1') "
                "ORDER BY notification_id DESC"
            )
            results = cursor.fetchall()
        print("はい",results)
        return results

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
