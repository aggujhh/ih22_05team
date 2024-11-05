from . import app, global_data
from flask import render_template, request, flash, redirect
from servers.flask_login import Flask_login
from flask_login import current_user, login_required, logout_user



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
        
        return render_template('notification.html')
    else:
        global_data.incorrectPassword += 1
        if global_data.incorrectPassword >= 3:
            flash(f"パスワードを3回間違えたため、10秒後にもう一度お試しください。", category='danger')
        else:
            flash(f"ユーザー名またはパスワードが正しくありません。", category='danger')
        return redirect('/redirect_admin_login')





# ログアウト
# @app.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     return redirect('/redirect_admin_login')



# ログイン処理&ページ遷移
