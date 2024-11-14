from datetime import timedelta
import secrets
import os,sys

DEBUG = True
HOST = '127.0.0.1'
PORT = '5001'
# secret_key を安全に生成
SECRET_KEY = secrets.token_hex(16)  # 16バイトの安全な秘密鍵を生成

# ファイルサイズ制限、最大2MB
MAX_CONTENT_LENGTH = 2 * 1024 * 1024

# 許可されているファイル拡張子
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# クッキーの有効期限を7日間に設定
REMEMBER_COOKIE_DURATION = timedelta(days=7)

# 画像フォルダへのアクセス
## c:PATH\shared_images
SHARED_IMAGES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'shared_images') 
print('SHARED',SHARED_IMAGES_DIR)
os.makedirs(SHARED_IMAGES_DIR, exist_ok=True) # なければDIR作る



# 静的ファイルフォルダのパスを定義
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, 'static')
IMG_FOLDER = os.path.join(STATIC_DIR, 'img')  # 画像フォルダのパス
UPLOADS_FOLDER = os.path.join(IMG_FOLDER, 'uploads')  # アップロード用フォルダのパス
CREATOR_IMG = os.path.join(IMG_FOLDER, 'creator_img')  # クリエイター画像フォルダのパス


