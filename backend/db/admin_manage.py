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
            # 権限名取得
            result['admin_permissions'] = self.get_role_name(result['admin_permissions'])
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


    def get_adminT_columns(self):
        print('get_adminT_columns')
        with db as cursor:
            cursor.execute("SHOW COLUMNS FROM ADMIN ")
            result = cursor.fetchall()
        print('result',result)
        
        return result