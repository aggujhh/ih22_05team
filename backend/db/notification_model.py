from . import db
from routes import logger


class notification_model:
    # お知らせ取り出し
    def get_notifications(self):
        with db as cursor:
            cursor.execute(
                "SELECT notification_id, notification_title, notification_post_time, notification_content "
                "FROM NOTIFICATION " 
                "WHERE notification_post_status = '1' "
            )
            results = cursor.fetchall()
        return results
    
    # お知らせ更新
    def update_notification(self,notification):
        return 1