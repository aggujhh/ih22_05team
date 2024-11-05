from . import app, global_data
from flask import render_template, request, flash, redirect
from servers.flask_login import Flask_login
from db.admin_manage import admin_manage
from flask_login import current_user, login_required, logout_user
import json



# ログインページの表示

# 管理者ログインページ表示
@app.route("/")
def redirect_admin():
    error_msg = ["", ""]
    return render_template('admin_login.html', error_msg=error_msg, global_data=global_data)

# 管理者ログイン処理
@app.route("/notification", methods=['POST'])
def login():
    error_msg = ["", ""]
    count = 0
    id = request.form.get("adminid")
    password = request.form.get("adminps")
    if id == "":
        error_msg[0] = "メールアドレスを空欄にしてはいけません。再入力してください。"
        count += 1
    if password == "":
        error_msg[1] = "パスワードを空欄にしてはいけません。再入力してください。"
        count += 1
    if count != 0:
        return render_template('admin_login.html', error_msg=error_msg, global_data=global_data)

    print(id, password)
    result = Flask_login().check_admin_login(id, password)
    print(result)
    if result:
        global_data.incorrectPassword = 0
        flash(f"おかえりなさい, {id}.", category='success')

        # お知らせ一覧をすべて取ってくる
<<<<<<< Updated upstream
        # notis =
=======
        notis = False
>>>>>>> Stashed changes
        
        return render_template('notification.html')
    else:
        global_data.incorrectPassword += 1
        if global_data.incorrectPassword >= 3:
            flash(f"パスワードを3回間違えたため、10秒後にもう一度お試しください。", category='danger')
        else:
            flash(f"ユーザー名またはパスワードが正しくありません。", category='danger')
        return redirect('/redirect_admin_login')






# ログアウト
@app.route('/logout')
@login_required
def logout():
    # セッションタイムアウト
    return redirect('/')



# 管理者管理
@app.route('/admin_manage')
def admin_mange():
    
    # DBから管理者一覧取得
    admins = admin_manage().get_alladmin()
    print(admins)

    return render_template('admin_manage.html',admins=admins)

# 管理者編集
@app.route('/admin_edit', methods=['POST'])
def admin_edit():
    
    # データの取得
    admin_id = request.form.get('admin_id')
    print(admin_id)

    # DBから管理者情報取得
    ## 権限コードは権限名に変換済み
    admin = admin_manage().get_admin(admin_id)
    admin['admin_permissions'] = [perm['permission_name'] for perm in admin['admin_permissions']]
    print('admin',admin)

    # DBからすべての権限名を取得
    permissions = admin_manage().get_allrole()
    print('permissoins',permissions)

    # {key: value}の形から[value1,value2]へ
    #roles = []
    #for perm['permissoins_name] in permissions:
    #    for value in perm.values():
    #        print('value',value)
    #        roles.append(value)
    roles = [perm['permission_name'] for perm in permissions]
    print('roles',roles)

    return render_template('admin_edit.html',admin=admin,roles=roles)


# 管理者追加
@app.route('/add_admin', methods=['GET', 'POST'])
def add_admin():
    if request.method == 'GET':
        # 管理者追加画面を表示
        ## DBからすべての権限名を取得
        permissions = admin_manage().get_allrole()
        print('permissions',permissions)
        roles = [perm['permission_name'] for perm in permissions]
        print('roles',roles)
        admin = admin_manage().get_adminT_columns()




# 管理者,編集後にDBに保存
@app.route('/modify_admin', methods=['POST'])
def modify_admin():
    admin = {
        'admin_id': request.form.get('admin_id'),
        'admin_name': request.form.get('admin_name'),
        'admin_permissions': request.form.get('admin_permissions')
    }