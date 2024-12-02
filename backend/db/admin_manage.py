from . import db
from routes import logger

class admin_manage:
    # すべての管理者を取得
    def get_alladmin(self):
        print('get_admins')
        with db as cursor:
            cursor.execute(
                "SELECT admin_id, admin_name, admin_password, password_expiration_date, admin_permissions "
                "FROM ADMIN "
                "WHERE status = '1' "
            )
            result = cursor.fetchall()
        
        print(result)

        # nbit目に1が立っているか
        admins = []
        for admin in result:
            role = admin['admin_permissions']
            print('admin_perm',role)
            admin['admin_permissions'] = self.get_role_name(role)
            admins.append(admin)

        return admins

    # idからadmin取得
    def get_admin(self,admin_id):
        print('get_admin',admin_id)
        with db as cursor:
            cursor.execute(
                "SELECT * "
                "FROM ADMIN "
                "WHERE admin_id = %s"
                , (admin_id,)
            )
            result = cursor.fetchone()
        print('result',result)
        return result
    
    # admin_permissionsから権限名を取得
    def get_role_name(self, role):
        print('get_role_name', role)
        try:
            with db as cursor:
                cursor.execute(
                    "SELECT permission_name "
                    "FROM admin_permissions "
                    "WHERE (CAST(permission_id AS BINARY) & CAST(%s AS BINARY)) != 0 "
                    , (role,)
                )
                perm_name = cursor.fetchall()
                print('perm_name',perm_name)
            return perm_name
        except Exception as e:
            print(f'ExceptionError: {e}')
    
    # すべての権限名を取得
    def get_allrole(self):
        print('get_allrole')
        with db as cursor:
            cursor.execute(
                "SELECT permission_name "
                "FROM admin_permissions "
            )
            roles = cursor.fetchall()
        #print('roles',roles)
        return roles


    # idの確認
    def admin_authentication(self, id):
        print(id)
        with db as cursor:
            cursor.execute("select admin_password from ADMIN where admin_id=%s", id)
            result = cursor.fetchone()
        return result


    # ADMIN テーブルからカラム名を取り出す
    def get_adminT_columns(self):
        print('get_adminT_columns')
        with db as cursor:
            cursor.execute("SHOW COLUMNS FROM ADMIN ")
            result = cursor.fetchall()
        print('result',result)

        # resultからADMINテーブルからカラム名を取り出す
        fields = {}
        for array in result:
            fields[array['Field']] = ''
        print('fields',fields)
            
        return fields
    
    # 権限名から２進数表現に変換
    def get_role(self,name):
        print('get_role',name)
        with db as cursor:
            cursor.execute(
                "SELECT permission_id "
                "FROM admin_permissions "
                "WHERE permission_name = %s "
                , (name,)
            )
            result = cursor.fetchone()
        print('result',result)
        return result['permission_id']

    # 管理者を登録
    def register_admin(self,admin):
        print('register_admin',admin)
        with db as cursor:
            cursor.execute(
                "INSERT INTO ADMIN(admin_id, admin_name, admin_password, password_expiration_date, admin_permissions) "
                "VALUES (%s, %s, %s, DATE_ADD(NOW(), INTERVAL 1 MONTH), %s);"
                ,(admin['admin_id'], admin['admin_name'], admin['admin_password'], admin['admin_permissions'],)
            )
        return 0
    
    # 管理者を削除
    def delete_admin(self,admin_id):
        print('delete_admin',admin_id)
        try:
            with db as cursor:
                cursor.execute(
                    #"DELETE FROM ADMIN WHERE admin_id = %s "
                    "UPDATE ADMIN "
                    "SET status = '0' "
                    "WHERE admin_id = %s "
                    , (admin_id,)
                )
            return 1
        except Exception as e:
            print("削除失敗:", e)
            return 0
            
    # admin_idから管理者情報を更新
    def update_admin(self,admin):
        print('update_admin',admin)
        try:
            with db as cursor:
                cursor.execute(
                    "UPDATE ADMIN "
                    "SET admin_name=%s, "
                    "    admin_permissions=%s "
                    "WHERE admin_id=%s "
                    , (admin['admin_name'], admin['admin_permissions'], admin['admin_id'],)
                )
            return 1
        except Exception as e:
            print("更新失敗:",e)
            return 0