from . import app, global_data
from flask import render_template, request, flash, redirect,jsonify
from servers.flask_login import Flask_login
from db.admin_manage import admin_manage
from flask_login import current_user, login_required, logout_user
from werkzeug.security import generate_password_hash
import json
import random,string

def generate_random_password(length=12):
    # パスワードに使う文字を定義(英字,数字,記号)
    characters = string.ascii_letters + string.digits + string.punctuation
    password = []

    # ランダムな文字を指定長分だけ取り出し
    for _ in range(length):
        random_character = random.choice(characters)
        password.append(random_character)
    
    # password内の文字を連結して1つの文字列生成
    return ''.join(password)



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
        # notis =
        notis = False
        
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
    admin = admin_manage().get_admin(admin_id)
    ## 権限コードを権限名に変換
    admin['admin_permissions'] = admin_manage().get_role_name(admin['admin_permissions'])
    ## 権限名の辞書型配列を権限名の配列に変換
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
@app.route('/register_admin', methods=['GET', 'POST'])
def add_admin():
    if request.method == 'GET':
        # 管理者追加画面を表示
        ## DBからすべての権限名を取得
        permissions = admin_manage().get_allrole()
        print('permissions',permissions)
        roles = [perm['permission_name'] for perm in permissions]
        print('roles',roles)
        admin = admin_manage().get_adminT_columns()

        return render_template('register_admin.html', admin=admin, roles=roles)
    
    if request.method == 'POST':
        print('/register_admin POST')
        # 管理者追加
        ## 入力された情報をDBに登録
        admin = {}
        admin_name = request.form['admin_name']
        print('admin_name',admin_name)
        #admin_password = request.form['admin_password']
        admin_permissions = request.form.getlist('permissions')
        print('admin',admin)

        ### admin_idの発行
        admin_id = f'A_{f"{random.randint(0,99999999):08}"}'
        while admin_manage().get_admin(admin_id):
            admin_id = f'A_{f"{random.randint(0,99999999):08}"}'
        print('admin_id',admin_id)

        ### admin_passwordの生成
        admin_password = generate_random_password(16)
        hashed_password = generate_password_hash(admin_password)
        print('admin_password',admin_password)

        ## 権限名を2進数に変換
        roles = '0000000'
        for role in admin_permissions:
            # 権限名を2進数に変換
            role = admin_manage().get_role(role)
            print('role',type(role))
            # 文字列2進数の足し算,先頭0bを除き,7桁になるように0埋め
            roles = bin(int(roles,2) + int(role,2))[2:].zfill(7)
        print(roles)

        ## 管理者情報をDBに登録
        admin = {
            'admin_id': admin_id,
            'admin_name': admin_name,
            'admin_password': hashed_password,
            'admin_permissions': roles 
        }
        ### SQL呼び出し
        admin_manage().register_admin(admin)

        # 登録完了画面表示
        admin['admin_password'] = admin_password
        return render_template('register_completion.html',admin=admin)


#####################################################################
# 管理者削除
#####################################################################
@app.route('/admin/delete/<admin_id>', methods=['DELETE'])
def delete_admin(admin_id):
    # DBから該当の管理者を削除
    try:
        print('delete_admin',admin_id)
        # 削除SQLの呼び出し
        if not admin_manage().delete_admin(admin_id):
            return jsonify({"message": "削除が完了しました"}), 200
        return jsonify({"message": "削除に失敗しました"}), 500
    except Exception as e:
        return jsonify({"message": "予期しないエラーが発生しました。"}), 500











# 管理者,編集後にDBに保存
@app.route('/modify_admin', methods=['POST'])
def modify_admin():
    admin = {
        'admin_id': request.form.get('admin_id'),
        'admin_name': request.form.get('admin_name'),
        'admin_permissions': request.form.get('admin_permissions')
    }