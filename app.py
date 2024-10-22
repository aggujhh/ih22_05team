# flaskより必要なモジュールをインポートする
from flask import Flask, render_template, request
from flask_cors import CORS
import requests

# Flaskアプリケーションオブジェクトを作成
app = Flask("Helloapp")
CORS(app)

#処理
# Flaskの動作確認。
@app.route("/")
def hello():
    return render_template(
        'index.html',
        title='COSBARA',
    )

# アプリケーションの実行
if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1')