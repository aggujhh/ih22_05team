# fraud_detection, account_routes.py関連
from . import db
from routes import logger


class account_model:
    # 不正検知を全件取り出し
    def get_reports(self):
        print('get_reports')
        with db as cursor:
            cursor.execute(
                "SELECT * "
                "FROM REPORT_FRAU "
            )
            results = cursor.fetchall()
        return results
    
    # 1件の不正検知を取り出し
    def get_report(self,fraud_report_id):
        print('get_report fraud_report_id', fraud_report_id)
        with db as cursor:
            cursor.execute(
                "SELECT * "
                "FROM REPORT_FRAU "
                "WHERE fraud_report_id =%s "
                ,(fraud_report_id,)
            )
            result = cursor.fetchone()
        return result
    
    # 詳細画面での変更を登録
    def update_report(self,data):
        print('update_report',data)
        try:
            with db as cursor:
                cursor.execute(
                    "UPDATE REPORT_FRAU "
                    "SET violation_judgment = %s, "
                    "    violation_reason = %s "
                    ,(data['violation_judgment'], data['violation_reason'])
                )
            print('更新成功')
            return 1
        except Exception as e:
            print('更新失敗',e)
            return 0
        
    # 解凍申請一覧取得
    def get_thaw_list(self):
        try:
            print('get_thaw_requests')
            with db as cursor:
                cursor.execute(
                    "SELECT * "
                    "FROM THAW_REQ "
                    "WHERE unfreeze_request_status = '0' "
                )
                result = cursor.fetchall()
            print('取り出し成功')
            return result
        except Exception as e:
            print('情報取り出し失敗',e)
            return 0
    
    # 一件の解除申請詳細を取得
    def get_thaw_request(self,unfreeze_request_id):
        try:
            print('get_thaw_request')
            with db as cursor:
                cursor.execute(
                    "SELECT * "
                    "FROM THAW_REQ "
                    "WHERE unfreeze_request_id=%s "
                    ,(unfreeze_request_id,)
                )
                result = cursor.fetchone()
            return result
        except Exception as e:
            print('情報取り出し失敗',e)
            return 0
    
    # 解除申請詳細内容を変更
    def update_thaw_request(self,data):
        try:
            print('update_thaw_request')
            with db as cursor:
                cursor.execute(
                    "UPDATE THAW_REQ "
                    "SET unfreeze_request_status=%s, "
                    "    unfreeze_request_reason=%s "
                    "WHERE unfreeze_request_id=%s "
                    ,(data['unfreeze_request_status'], data['unfreeze_request_reason'], data['unfreeze_request_id'])
                )
            print('更新成功')
            return 1
        except Exception as e:
            print('更新失敗',e)
            return 0
        

            