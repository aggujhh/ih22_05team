from flask_login import UserMixin, login_user, LoginManager, current_user
from db.userm_model import Userm_model
from severs.global_data import global_data
from werkzeug.security import check_password_hash
from routes import app

# LoginManagerクラスのインスタンスを作成（ユーザのログイン管理を行う）
login_manager = LoginManager()
login_manager.init_app(app)  # FlaskアプリにLoginManagerを設定
login_manager.login_view = 'redirect_to_login'  # ログインページのビュー関数を指定


# ログイン時にユーザのロードを行う関数
@login_manager.user_loader
def load_user(user_id):
    return User(user_id) or None  # 指定されたユーザIDに基づきユーザを返す


# Flask-LoginのUserMixinを継承したユーザクラス
class User(UserMixin):
    def __init__(self, id):
        self.id = id  # ユーザIDをセット


# ログイン機能を提供するクラス
class Flask_login:
    def check_login(self, mail_address: str, password: str, remember) -> bool:
        # Userm_modelのuser_authenticationメソッドで認証を行う
        result = Userm_model().login(mail_address)
        print("result:", result)
        if result and check_password_hash(result["user_password"], password):  # 認証成功時
            login_user(User(result["user_id"]), remember=remember)  # ユーザをログイン状態にする
            nickname = Userm_model().fetch_nickname_by_userid(current_user.id)
            global_data.set_nickname(current_user.id, nickname)
            return True  # ログイン成功を返す
        return False  # ログイン失敗を返す
