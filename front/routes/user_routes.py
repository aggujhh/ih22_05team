from . import app, Session
from flask import render_template, request, flash, redirect, jsonify
from severs.flask_login import Flask_login
from flask_login import current_user, login_required, logout_user
from severs.flask_mail import mail
from severs.global_data import global_data
from flask_mail import Message
from db.userm_model import Userm_model
from werkzeug.security import generate_password_hash
import random
import re
import logging
import secrets
import base64
import os
import uuid
import json


# ログインページ表示
@app.route("/redirect_to_login")
def redirect_to_login():
    error_msg = ["", ""]
    return render_template('login.html', error_msg=error_msg, count=0)


# ログイン処理
@app.route("/login", methods=['POST'])
def login():
    error_msg = ["", ""]
    count = 0
    mail_address = request.form.get("mail_address")
    password = request.form.get("password")
    if mail_address == "":
        error_msg[0] = "メールアドレスを空欄にしてはいけません。再入力してください。"
        count += 1
    if password == "":
        error_msg[1] = "パスワードを空欄にしてはいけません。再入力してください。"
        count += 1
    if count != 0:
        return render_template('login.html', error_msg=error_msg, count=0)

    print(mail_address, password)
    remember_me = 'remember' in request.form
    result = Flask_login().check_login(mail_address, password, remember_me)
    print(result)
    if result:
        global_data.del_incorrect_password(mail_address)
        nickname = global_data.get_nickname(current_user.id)
        result = Userm_model().get_avatar_and_user_type(current_user.id)
        icon_path = f"img/uploads/{current_user.id}/icon_url/image_icon_url.png"
        file_path = os.path.join(app.config['STATIC_DIR'], icon_path)
        if not os.path.exists(file_path):
            icon_path = f"img/default_avatar.png"
        avatar = icon_path
        user_type = result["user_type"]
        if avatar:
            global_data.set_avatar(current_user.id, avatar)
        if user_type:
            global_data.set_user_type(current_user.id, user_type)
        flash(f"おかえりなさい, {nickname}.", category='success')
        return redirect('/')
    else:
        count = global_data.increment_incorrect_password(mail_address)
        if count > 3:
            flash(f"パスワードを3回間違えたため、10秒後にもう一度お試しください。", category='danger')
        else:
            flash(f"ユーザー名またはパスワードが正しくありません。", category='danger')
        return render_template('login.html', error_msg=error_msg, mail_address=mail_address, count=count)


# パスワード入力可能状態に戻る
@app.route('/reset', methods=['POST'])
def reset():
    email_address = request.form.get("mail")
    print("email_address", email_address)
    global_data.reset_incorrect_password(email_address)
    return jsonify({"status": "success"})


# アカウント作成ページへ
@app.route("/registration")
def registration():
    error_msg = ["", "", "", ""]
    user_type = "requester_user"
    return render_template('registration.html', user_type=user_type, error_msg=error_msg)


# ログアウト
@app.route('/logout')
@login_required
def logout():
    global_data.del_user(current_user.id)
    logout_user()
    return redirect('/')


# 登録する時、依頼者と制作者をチェンジする
@app.route('/change_user_type')
def change_user_type():
    error_msg = ["", "", "", ""]
    user_type = request.args.get("user_type_data")
    return render_template('registration.html', user_type=user_type, error_msg=error_msg)


# メールに認証コードを送信する
@app.route('/send_email', methods=['POST'])
def send_email():
    email = request.form.get("email")
    rand_gen = random.Random()
    random_number = rand_gen.randint(1, 9999)
    digit_count = len(str(random_number))
    match digit_count:
        case 1:
            authentication_code = "000" + str(random_number)
        case 2:
            authentication_code = "00" + str(random_number)
        case 3:
            authentication_code = "0" + str(random_number)
        case _:
            authentication_code = str(random_number)
    print("set_session", email, authentication_code)
    Session().set_session_with_expiry(email, authentication_code, 600)
    msg = Message('[COSBARA]認証コードをご確認ください。', recipients=[email])
    msg.body = (
        f"""メールには「COSBARA」の認証コード送信メールで、
下記の認証コードをプロフィール設定画面に表示されている
4桁の数字を入力してメールアドレスの認証手続きを完了してください。

▼認証コード
{authentication_code}

※本メール記載の認証コードの有効期限は発行から10分間、1回限り有効です。
10分以内に認証した場合や正しく認証できない場合には認証コードを再送し、
再度登録をお願いいたします。
""")
    mail.send(msg)
    print("发送成功", email)
    return jsonify({'message': '发送成功'})


# アカウント作成したフォームの正解性チェック
@app.route('/check_registration/<user_type>', methods=['POST'])
def check_registration(user_type):
    error_msg = ["", "", "", ""]
    count = 0
    user_id = secrets.token_hex(5)
    while Userm_model().user_authentication(user_id):
        user_id = secrets.token_hex(5)
    password = request.form.get("password")
    # パスワードをハッシュ化する
    hashed_password = generate_password_hash(password)
    user = {
        "user_id": user_id,
        "nickname": request.form.get("nickname"),
        "user_email_address": request.form.get("email"),
        "authentication_code": request.form.get("authentication_code"),
        "user_password": hashed_password,
        "confirm_password": request.form.get("confirm_password"),
        "user_type": 0
    }
    # ユーザーが制作者の時
    if user_type == "creator_user":
        creator_user_id = "app_" + secrets.token_hex(4)
        while Userm_model().have_creator_id(creator_user_id):
            creator_user_id = "app_" + secrets.token_hex(4)
        user["user_id"] = creator_user_id
        user["tel"] = request.form.get("tel")
        user["creator_history"] = request.form.get("creator_history")
        user["image"] = json.loads(request.form.get("image"))
        phone_pattern = r"^(0\d{1,4})[-.\s]?\d{1,4}[-.\s]?\d{4}$"
        if not re.match(phone_pattern, user["tel"]):
            error_msg[3] = "電話番号の形式が正しくありません。再入力してください。"
            count += 1
    mail_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(mail_pattern, user["user_email_address"]):
        error_msg[0] = "メールアドレスの形式が正しくありません。再入力してください。"
        count += 1
    session_code = Session().get_session_with_expiry(user["user_email_address"])
    if session_code is None:
        error_msg[1] = "認証コードが無効です。もう一度ログインしてください。"
        count += 1
    elif user["authentication_code"] != session_code:
        error_msg[1] = "認証コードが間違っています。もう一度入力してください。"
        count += 1
    if password != user["confirm_password"]:
        error_msg[2] = "パスワードが一致しません。もう一度入力してください。"
        count += 1
    if count == 0:
        try:
            if user_type == "requester_user":
                Userm_model().add_user(user)
            else:
                Userm_model().add_creator_application(user)
            print("登録完成")
            Flask_login().check_login(user["user_email_address"], password, remember=False)
            return render_template('register_completion.html', user_type=user_type, remember=False)
        except Exception as e:
            # エラーが発生した場合、エラーログを記録
            logging.error(f"Error occurred: {e}")
            alert_message = "登録失敗"
            # 登録が失敗した場合のメッセージ
            return render_template('registration.html', user_type=user_type, error_msg=error_msg,
                                   alert_message=alert_message)
    else:
        return render_template('registration.html', user_type=user_type, error_msg=error_msg)


# 制作者アカウント作成時にアップロードした制作物画像の処理
@app.route("/upload_img", methods=['POST'])
def upload_img():
    # フロントエンドからのJSONデータを取得
    data = request.get_json()
    # 画像データの配列を取得
    images = data.get('images', [])
    # 画像が存在しない場合、エラーを返す
    if not images:
        return jsonify({'error': 'No images received'}), 400
    saved_files = []  # 保存されたファイル名リスト
    for idx, image_data in enumerate(images):
        try:
            # Base64データは通常 'data:image/jpeg;base64,' 形式で始まるため、ヘッダー部分を削除
            if 'base64,' in image_data:
                image_data = image_data.split('base64,')[1]
            # Base64文字列をバイナリデータにデコード
            img_data = base64.b64decode(image_data)
            # 保存する画像のファイル名を生成
            file_name = f'image_{uuid.uuid4()}.png'  # 必要に応じてファイル形式や命名を変更可能
            file_path = os.path.join(app.config['CREATOR_IMG'], file_name)
            # バイナリデータをファイルに書き込む
            with open(file_path, 'wb') as img_file:
                img_file.write(img_data)
            # 保存されたファイル名をリストに追加
            saved_files.append(file_path)
        except Exception as e:
            return jsonify({'error': f'Failed to process image {idx}: {str(e)}'}), 500
    # 画像が正常にアップロードされた場合の応答
    return jsonify({'message': 'Images uploaded successfully', 'urls': saved_files})


# パスワードを再設定ページへ
@app.route('/forgot_password')
def forgot_password():
    error_msg = ["", ""]
    return render_template('forgot_password.html', error_msg=error_msg, count=0)


# パスワードを再設定
@app.route('/reset_password', methods=['POST'])
def reset_password():
    count = 0
    error_msg = ["", ""]
    password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")
    mail_address = request.form.get("mail_address")
    print("get_____", password, confirm_password, mail_address)
    if password == "":
        error_msg[0] = "新しいパスワードを空欄にしてはいけません。再入力してください。"
        count += 1
    if confirm_password == "":
        error_msg[1] = "パスワード確認を空欄にしてはいけません。再入力してください。"
        count += 1
    if password != confirm_password:
        error_msg[1] = "パスワードが一致しません。もう一度入力してください。"
        count += 1
    if count != 0:
        return render_template('forgot_password.html', error_msg=error_msg,
                               mail_address=mail_address, count=0)
    # パスワードをハッシュ化する
    hashed_password = generate_password_hash(password)
    Userm_model().reset_ps(mail_address, hashed_password)
    Flask_login().check_login(mail_address, password, remember=False)
    nickname = global_data.get_nickname(current_user.id)
    flash(f"おかえりなさい, {nickname}.", category='success')
    return redirect('/')


# 認証コードを確認する
@app.route('/check_authentication_code', methods=['POST'])
def check_authentication_code():
    error_msg = ["", ""]
    count = 0
    mail_address = request.form.get("hidden_mail_address")
    session_code = Session().get_session_with_expiry(mail_address)
    print("session_code:", mail_address, session_code, request.form.get("code"))
    if session_code is None:
        error_msg[1] = "認証コードが無効です。もう一度ログインしてください。"
        count += 1
    elif request.form.get("code") != session_code:
        error_msg[1] = "認証コードが間違っています。もう一度入力してください。"
        count += 1
    if count == 0:
        return render_template('forgot_password.html', error_msg=error_msg, count=0,
                               mail_address=mail_address)
    else:
        return render_template('forgot_password.html', error_msg=error_msg, count=0)
