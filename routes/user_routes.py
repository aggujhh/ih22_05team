import random

from . import app, global_data
from flask import render_template, request, flash, redirect
from severs.flask_login import Flask_login
from flask_login import current_user, login_required, logout_user
from severs.flask_mail import mail
from flask_mail import Message
import random


# ログインページ表示
@app.route("/redirect_to_login")
def redirect_to_login():
    error_msg = ["", ""]
    return render_template('login.html', error_msg=error_msg, global_data=global_data)


# ログイン処理
@app.route("/login", methods=['POST'])
def login():
    error_msg = ["", ""]
    count = 0
    id = request.form.get("id")
    password = request.form.get("password")
    if id == "":
        error_msg[0] = "メールアドレスを空欄にしてはいけません。再入力してください。"
        count += 1
    if password == "":
        error_msg[1] = "パスワードを空欄にしてはいけません。再入力してください。"
        count += 1
    if count != 0:
        return render_template('login.html', error_msg=error_msg, global_data=global_data)

    print(id, password)
    result = Flask_login().check_login(id, password)
    print(result)
    if result:
        global_data.incorrectPassword = 0
        flash(f"おかえりなさい, {current_user.id}.", category='success')
        return redirect('/')
    else:
        global_data.incorrectPassword += 1
        if global_data.incorrectPassword >= 3:
            flash(f"パスワードを3回間違えたため、10秒後にもう一度お試しください。", category='danger')
        else:
            flash(f"ユーザー名またはパスワードが正しくありません。", category='danger')
        return redirect('/redirect_to_login')


# パスワード入力可能状態に戻る
@app.route('/reset', methods=['GET'])
def reset():
    global_data.incorrectPassword = 0
    return redirect('/redirect_to_login')


# アカウント作成ページへ
@app.route("/registration")
def registration():
    user_type = "requester_user"
    return render_template('registration.html', user_type=user_type)


# ログアウト
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


# 登録する時、依頼者と制作者をチェンジする
@app.route('/change_user_type')
def change_user_type():
    user_type = request.args.get("user_type_data")
    return render_template('registration.html', user_type=user_type)


# メールに認証コードを送信する
@app.route('/send_email', methods=['POST'])
def send_email():
    email = request.form.get("email")
    rand_gen = random.Random(10000)
    msg = Message('Test Mail', recipients=[email])
    msg.body = "Hello Flask message sent from Flask-Mail"
    mail.send(msg)
    print("发送成功", email)
    return redirect('/registration')
