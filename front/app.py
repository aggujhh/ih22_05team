# flaskより必要なモジュールをインポートする
from routes import app
from config import HOST, PORT


# アプリケーションの実行
if __name__ == '__main__':
    app.run(host=HOST, port=PORT)