from flask_login import UserMixin, login_user, LoginManager
from db.userm_model import Userm_model
from routes import app

# LoginManagerクラスのインスタンスを作成（ユーザのログイン管理を行う）
login_manager = LoginManager()
login_manager.init_app(app)  # FlaskアプリにLoginManagerを設定
login_manager.login_view = 'login'  # ログインページのビュー関数を指定


# ログイン時にユーザのロードを行う関数
@login_manager.user_loader
def load_user(user_id):
    return User(user_id) or None  # 指定されたユーザIDに基づきユーザを返す


# Flask-LoginのUserMixinを継承したユーザクラス
class User(UserMixin):
    def __init__(self, id):
        self.id = id  # ユーザIDをセット
        self.role = role # ユーザの役割('admin' or 'user')

# ログイン機能を提供するクラス
class Flask_login:
    def check_login(self, id: str, password: str) -> bool:
        # Userm_modelのuser_authenticationメソッドで認証を行う
        result = Userm_model().user_authentication(id, password)
        if result:  # 認証成功時
            login_user(User(id))  # ユーザをログイン状態にする
            return True  # ログイン成功を返す
        return False  # ログイン失敗を返す