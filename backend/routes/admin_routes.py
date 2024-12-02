from . import app, global_data
from flask import render_template, request, flash, redirect,jsonify
from servers.flask_login import Flask_login
from db.admin_manage import admin_manage
from db.notification_model import notification_model
from db.log_model import log_model
from decorators.permission_decorators import permission_required
from flask_login import current_user, login_required, logout_user
from werkzeug.security import generate_password_hash
from datetime import datetime
import json
import random,string



######################################################################
# 関数
######################################################################


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


# 権限名たちを２進数に変換
## {'admin_permissions':'}
def roleName_to_bin(roles):
    print('roleName_to_bin')
    result = '0000000'
    for role in roles:
        # 権限名を2進数に変換
        role = admin_manage().get_role(role)
        # 文字列2進数の足し算,先頭0bを除き,7桁になるように0埋め
        result = bin(int(result,2) + int(role,2))[2:].zfill(7)
    return result







######################################################################
# 処理
######################################################################


# 管理者ログインページ表示
@app.route("/")
def redirect_admin():
    error_msg = ["", ""]
    return render_template('admin_login.html', error_msg=error_msg, global_data=global_data)

# 管理者ログイン処理
@app.route("/menu", methods=['POST'])
def login():
    error_msg = ["", ""]
    msg = ''
    count = 0
    id = request.form.get("adminid")
    password = request.form.get("adminps")
    if id == "":
        error_msg[0] = "管理者IDを空欄にしてはいけません。再入力してください。"
        count += 1
    if password == "":
        error_msg[1] = "パスワードを空欄にしてはいけません。再入力してください。"
        count += 1
    if count != 0:
        return render_template('admin_login.html', error_msg=error_msg, msg=msg,global_data=global_data)

    print(id, password)
    result = Flask_login().check_admin_login(id, password, remember=True)
    print(result)
    if result:
        global_data.incorrectPassword = 0
        flash(f"おかえりなさい, {id}.", category='success')
        log_model().update_log(id,'ログイン','ログイン')
        return render_template('menu.html')
    else:
        #global_data.incorrectPassword += 1
        #if global_data.incorrectPassword >= 3:
        #    flash(f"パスワードを3回間違えたため、10秒後にもう一度お試しください。", category='danger')
        #else:
        #    flash(f"ユーザー名またはパスワードが正しくありません。", category='danger')
        msg = 'もう一度入力してください'
        return render_template('admin_login.html', error_msg=error_msg,msg=msg)






# ログアウト
@app.route('/logout')
@login_required
def logout():
    # セッションタイムアウト
    log_model().update_log(current_user.id,'ログアウト','ログアウト')
    return redirect('/')






#######################################################################
# 管理者管理
#######################################################################
@app.route('/admin_manage')
@login_required 
@permission_required(0)
def admin_mange():
    log_model().update_log(current_user.id,'管理者管理画面アクセス','管理者管理画面アクセス')
    
    # DBから管理者一覧取得
    admins = admin_manage().get_alladmin()
    print('current admin_id',current_user.id)
    print(admins)
    return render_template('admin_manage.html',admins=admins)

#######################################################################
# 管理者編集
#######################################################################
@app.route('/admin_edit', methods=['POST'])
@permission_required(0)
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

    log_model().update_log(current_user.id,'管理者編集アクセス',f'変更後の情報 管理者:{admin_id},権限:{roles}')
    return render_template('admin_edit.html',admin=admin,roles=roles)

#######################################################################
# 管理者追加
#######################################################################
@app.route('/register_admin', methods=['GET', 'POST'])
@login_required 
@permission_required(0)
def add_admin():
    if request.method == 'GET':
        # 管理者追加画面を表示
        ## DBからすべての権限名を取得
        permissions = admin_manage().get_allrole()
        print('permissions',permissions)
        roles = [perm['permission_name'] for perm in permissions]
        print('roles',roles)
        admin = admin_manage().get_adminT_columns()

        log_model().update_log(current_user.id,'管理者追加画面アクセス','管理者追加画面アクセス')
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
        roles = roleName_to_bin(admin_permissions)
        print(roles)

        ## 管理者情報をDBに登録
        admin = {
            'admin_id': admin_id,
            'admin_name': admin_name,
            'admin_password': hashed_password,
            'admin_permissions': roles 
        }
        print('before SQL',admin)
        ### SQL呼び出し
        admin_manage().register_admin(admin)

        # 登録完了画面表示
        admin['admin_password'] = admin_password
        admin['admin_permissions'] = admin_permissions

        log_model().update_log(current_user.id,'管理者追加',f'管理者追加 追加管理者:{admin_id},名前:{admin_name},権限:{roles}')
        return render_template('register_completion.html',admin=admin)




#####################################################################
# 管理者削除
#####################################################################
@app.route('/admin/delete/<admin_id>', methods=['DELETE'])
@login_required 
@permission_required(0)
def delete_admin(admin_id):
    # DBから該当の管理者を削除
    try:
        print('delete_admin',admin_id)
        # 削除SQLの呼び出し
        if admin_id != current_user.id and admin_manage().delete_admin(admin_id): 
            log_model().update_log(current_user.id,'管理者削除',f'管理者削除 削除された管理者:{admin_id}')
            return jsonify({"message": "削除が完了しました"}), 200
        return jsonify({"message": "削除に失敗しました"}), 500
    except Exception as e:
        return jsonify({"message": "予期しないエラーが発生しました。"}), 500




##################################################################
# 管理者修正
##################################################################
@app.route('/modify_admin', methods=['POST'])
@permission_required(0)
def modify_admin():
    try:
        print('modify_admin')
        admin = {
            'admin_id': request.form.get('admin_id'),
            'admin_name': request.form.get('admin_name'),
            'admin_permissions': roleName_to_bin(request.form.getlist('permissions'))
        }
        print('admin',admin)

        # 受け取った情報をDBに登録
        if admin_manage().update_admin(admin):
            log_model().update_log(current_user.id,'管理者修正',f'修正後の情報 管理者ID:{admin["admin_id"]},管理者名:{admin["admin_name"]},権限:{admin["admin_permissions"]}')
            return redirect('/admin_manage')
    except Exception as e:        
        return render_template('error.html',e=e)




##############################################################
# お知らせ画面表示
##############################################################
@app.route('/notification', methods=['GET'])
@login_required 
@permission_required(6)
def notification():
    print('notification')
    ##notification_id = '1'
    ##notification_title = 'test'
    ##notification_content = 'content1'
    ##notification = {
    ##    'notification_id': notification_id,
    ##    'notification_title':notification_title,
    ##    'notification_content':notification_content
    ##}
    ##notifications = [notification]

    # DBからお知らせたちを取得
    notifications = notification_model().get_notifications()
    log_model().update_log(current_user.id,'お知らせ表示','お知らせ表示')
    return render_template('notification.html',notifications=notifications)



##############################################################
# お知らせ詳細表示
##############################################################
@app.route('/notification/<int:notification_id>')
@login_required 
@permission_required(6)
def notification_detail(notification_id):
    print('notification_detail')

    # お知らせ取り出し
    notification = notification_model().get_notification(notification_id)

    log_model().update_log(current_user.id,'お知らせ詳細表示','お知らせ詳細表示')
    return render_template('notification_detail.html',notification=notification)



##############################################################
# お知らせ追加
##############################################################
@app.route('/add_notification', methods=['GET', 'POST'])
@login_required 
@permission_required(6)
def add_notification():
    if request.method == 'GET': # お知らせ追加画面表示
        print('add_notification GET')
        notification = {
            'notificatoin_id':'',
            'notification_title':'',
            'notification_post_time':'',
            'notification_post_status':''
        }
        log_model().update_log(current_user.id,'お知らせ追加画面表示','お知らせ追加画面表示')
        return render_template('notification_detail.html',notification=notification)

    if request.method == 'POST': # お知らせ追加処理
        action = request.form.get('action') # 押下ボタン
        print('add_notification POST', action)

        if action == 'cancel':
            return redirect('/notification')

        # 入力内容の取得
        title = request.form.get('title')
        content = request.form.get('content')
        show_calendar = 'showCalendar' in request.form
        reservationDatetime = request.form.get('reservationDatetime') if show_calendar else None
        visibility = request.form.get('visibility')

        # show_calendarをDBのDATETIME形式に変換
        if reservationDatetime:
            print(reservationDatetime)
            ## ISO 8601形式をMySQL DATETIME形式に変換
            formatted_datetiem = reservationDatetime.replace('T', ' ')
            ### 文字列->datetime object
            reservationDatetime = datetime.strptime(formatted_datetiem, '%Y-%m-%d %H:%M')

        # 下書きか投稿するか
        if action == 'save': # 下書き
            notification_post_status = '0'
        else : # post : 投稿
            notification_post_status = '1'


        notification = {
            'notification_title':title,
            'notification_post_status':notification_post_status,
            'notification_post_time':reservationDatetime,
            'notification_content':content
        }
        print('notification',notification)

        try:
            # 下書きをDBに登録
            if notification_model().add_notification(notification):
                log_model().update_log(current_user.id,'お知らせ追加',f'追加するお知らせ タイトル:{title},投稿状態:{action},投稿日時:{reservationDatetime},内容:{content}')
                return redirect('/notification')
        except Exception as e:
            return render_template('error.html',e=e)
        


######################################################################
# お知らせ修正
######################################################################
@app.route('/modify_notification/<int:notification_id>', methods=['GET', 'POST'])
@login_required 
@permission_required(6)
def modify_notification(notification_id):
    if request.method=='GET':
        print('modify_notification GET',notification_id)
        notification = notification_model().get_notification(notification_id)
        log_model().update_log(current_user.id,'お知らせ修正画面表示',f'お知らせ修正画面表示 id:{notification_id}')
        return render_template('modify_notification.html',notification=notification)

    if request.method=='POST':
        action = request.form.get('action') # 押下ボタン
        print('modify_notification POST', action)

        if action == 'cancel':
            return redirect('/notification')

        # 入力内容の取得
        title = request.form.get('title')
        content = request.form.get('content')
        show_calendar = 'showCalendar' in request.form
        reservationDatetime = request.form.get('reservationDatetime') if show_calendar else None
        visibility = request.form.get('visibility')

        # show_calendarをDBのDATETIME形式に変換
        if reservationDatetime:
            print(reservationDatetime)
            ## ISO 8601形式をMySQL DATETIME形式に変換
            formatted_datetiem = reservationDatetime.replace('T', ' ')
            ### 文字列->datetime object
            reservationDatetime = datetime.strptime(formatted_datetiem, '%Y-%m-%d %H:%M')

        # 下書きか投稿するか
        if action == 'save': # 下書き
            notification_post_status = '0'
        else : # post : 投稿
            notification_post_status = '1'


        notification = {
            'notification_id':notification_id,
            'notification_title':title,
            'notification_post_status':notification_post_status,
            'notification_post_time':reservationDatetime,
            'notification_content':content
        }
        print('notification',notification)

        try:
            # 下書きをDBに登録
            if notification_model().update_notification(notification):
                log_model().update_log(current_user.id,'お知らせ修正',f'修正後のお知らせ ID:{notification_id},タイトル:{title},投稿状態:{notification_post_status},投稿日時:{reservationDatetime},内容:{content}')
                return redirect('/notification')
        except Exception as e:
            return render_template('error.html',e=e)
        

####################################################################
# お知らせ削除
####################################################################
@app.route('/delete_notification', methods=['POST'])
@login_required 
@permission_required(6)
def delete_notification():
    notification_id = request.form.get('notification_id')
    print('delete_notification', notification_id)
    try:
        # DBから情報削除
        if notification_model().delete_notification(notification_id):
            log_model().update_log(current_user.id,'お知らせ削除',f'削除されたお知らせ id:{notification_id}')
            return redirect('/notification')
    except Exception as e:
        return render_template('error.html',e=e)















######################################################################
# エラーハンドリング
######################################################################
# @app.errorhandler()
# def error1(error):
#     print('hi')