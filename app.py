# flaskより必要なモジュールをインポートする
from flask import Flask, render_template, request, redirect, flash
from db.userm_model import Userm_model
import secrets

# from flask_cors import CORS


# Flaskアプリケーションオブジェクトを作成
app = Flask("Helloapp")

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

#ログインページ表示
@app.route("/redirect_to_login")
def redirect_to_login():
    error_msg = ["", ""]
    return render_template('login.html', error_msg=error_msg, global_data=global_data)

#ログイン処理
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
        return render_template('login.html', error_msg=error_msg)

    result = Userm_model().user_authentication(id, password)
    print(result)
    if result:
        global_data.incorrectPassword = 0
        flash(f"おかえりなさい, {id}.", category='success')
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
    return render_template('registration.html')


# アプリケーションの実行
if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1')
