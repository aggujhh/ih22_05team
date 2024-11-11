from flask import Flask, session, send_from_directory
from datetime import timedelta, datetime
from flask_login import current_user
from severs.global_data import global_data
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


@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.context_processor
def inject_user_data():
    if current_user.is_authenticated:
        # 获取当前用户的昵称
        nickname = global_data.get_nickname(current_user.id)
    else:
        nickname = None
    # 将 nickname 注入到模板上下文中
    return {'nickname': nickname}


from . import user_routes
from . import nav_routes
from . import request_routes
from . import my_page_routes
from . import inquiry_routes
