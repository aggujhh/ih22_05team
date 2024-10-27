from flask import Flask, render_template, session
import secrets
from datetime import timedelta, datetime
import logging
import os

# Flaskアプリケーションオブジェクトを作成
app = Flask(__name__,
            template_folder='../templates',
            static_folder='../static')

# secret_key を安全に生成
app.secret_key = secrets.token_hex(16)  # 16バイトの安全な秘密鍵を生成

# ファイルサイズ制限、最大2MB
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024

# Flask アプリの static フォルダのパスを取得
static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')
# 'static/uploads' フォルダに保存する場合
upload_folder = os.path.join(os.path.join(static_dir, 'img'), 'uploads_creator_image')
# 'static/uploads' フォルダが存在しない場合は作成
if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)
print(f"ファイルの保存先: {upload_folder}")

# 許可されているファイル拡張子
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# ログの設定
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class Session:
    # 特定のセッションキーに有効期限を設定
    def set_session_with_expiry(self, key, value, lifetime_seconds):
        session[key] = {
            'value': value,
            'expiry': (datetime.now() + timedelta(seconds=lifetime_seconds)).timestamp()
        }

    # 特定のセッションキーの有効期限をチェック
    def get_session_with_expiry(self, key):
        item = session.get(key)
        if item:
            expiry = item['expiry']
            if datetime.now().timestamp() > expiry:
                session.pop(key, None)  # 有効期限切れの場合、キーを削除
                return None
            return item['value']
        return None


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
