# flaskより必要なモジュールをインポートする
from flask import Flask, send_from_directory
from routes import app
from config import HOST, PORT
import os,sys


# カスタムフィルターを定義
@app.template_filter('contains')
def contains(value, collection):
    print('reach contains, value: collection:',value,collection)
    return value in collection

# アプリケーションの実行
if __name__ == '__main__':
    app.run(host=HOST, port=PORT,debug=True)
