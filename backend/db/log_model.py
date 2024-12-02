from . import db
from routes import logger

class log_model:
    def get_log(self):
        print('get_log')
        with db as cursor:
            cursor.execute(
                "SELECT * "
                "FROM LOG "
                "ORDER BY time DESC "
            ) 
            result = cursor.fetchall()
        return result

    def update_log(self,admin_id, action, details):
        try:
            print('update_log')
            with db as cursor:
                cursor.execute(
                    "INSERT INTO LOG(admin_id, action, details) "
                    "VALUES(%s, %s, %s) "
                    ,(admin_id, action, details,)
                )
            print('更新成功')
            return True
        except Exception as e:
            print('更新失敗',e)
            return False

        
