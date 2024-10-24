from flask import Flask, render_template
import secrets

# Flaskアプリケーションオブジェクトを作成
app = Flask(__name__,
            template_folder='../templates',
            static_folder='../static')

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

@app.route("/")
def hello():
    return render_template('index.html')


from . import user_routes
