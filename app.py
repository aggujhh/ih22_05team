# flaskより必要なモジュールをインポートする
from routes import app


# アプリケーションの実行
if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1')
