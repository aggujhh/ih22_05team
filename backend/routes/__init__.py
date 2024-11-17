from flask import Flask, session
from datetime import timedelta, datetime
import logging
import os

# Flaskアプリケーションオブジェクトを作成
app = Flask(__name__,
            template_folder='../templates',
            static_folder='../static')

config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.py')
app.config.from_pyfile(config_path)

# アップロードフォルダが存在するか確認,存在していない時作る
if not os.path.exists(app.config['CREATOR_IMG']):
    os.makedirs(app.config['CREATOR_IMG'])
print(f"ファイルの保存先: {app.config['CREATOR_IMG']}")

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

from . import admin_routes
from . import application_routes
from . import inquiry_routes