# flaskより必要なモジュールをインポートする
from flask import Flask, render_template, request, redirect, flash, make_response, jsonify
import secrets
from severs.flask_login import Flask_login, User
from flask_login import current_user, LoginManager, logout_user, login_required
from flask_mail import Mail, Message

# from flask_cors import CORS

# Flaskアプリケーションオブジェクトを作成
app = Flask(__name__)

# メールサーバ
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587  # TLSは587、SSLなら465
app.config['MAIL_USERNAME'] = 'chinntaro31@gmail.com'
app.config['MAIL_PASSWORD'] = 'qmwwwvxzmxicrkag'  # GmailのApp用のmパスワード設定をしておく必要あり
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEFAULT_SENDER'] = 'chinntaro31@gmail.com'    # これがあるとsender設定が不要になる
mail = Mail(app)

# LoginManagerクラスのインスタンスを作成（ユーザのログイン管理を行う）
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User(user_id) or None


# secret_key を安全に生成
app.secret_key = secrets.token_hex(16)  # 16バイトの安全な秘密鍵を生成


# Global_dataクラスは、パスワードの間違い回数を記録するためのクラスです。
# このクラスには、パスワードを間違えた回数（incorrectPassword）を保持し、
# その値を初期化および文字列として表示する機能があります。
class Global_data():
    def __init__(self, incorrectPassword=0):
        self.incorrectPassword = incorrectPassword

    def __str__(self):
        return f"incorrectPassword={self.incorrectPassword}"


global_data = Global_data()


# CORS(app)


# 処理
# Flaskの動作確認。
@app.route("/")
def hello():
    return render_template('index.html')


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


@app.route('/change_user_type')
def change_user_type():
    user_type = request.args.get("user_type_data")
    return render_template('registration.html', user_type=user_type)


@app.route('/send_email', methods=['POST'])
def send_email():
    email = request.form.get("email")
    msg = Message('Test Mail', recipients=[email])
    msg.body = "Hello Flask message sent from Flask-Mail"
    mail.send(msg)
    print("发送成功", email)
    return redirect('/registration')


# アプリケーションの実行
if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1')
