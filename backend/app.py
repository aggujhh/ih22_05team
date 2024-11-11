# flaskより必要なモジュールをインポートする
from flask import Flask
from routes import app
from config import HOST, PORT
import os


# カスタムフィルターを定義
@app.template_filter('contains')
def contains(value, collection):
    print('reach contains, vlaue: collection:',value,collection)
    return value in collection

# アプリケーションの実行
if __name__ == '__main__':
    app.run(host=HOST, port=PORT,debug=True)
