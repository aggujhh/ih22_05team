from . import app
from flask import render_template, request, redirect


# 依頼詳細情報ページへのリダイレクト
@app.route('/request/<request_id>', methods=['POST'])
def request_details(request_id):
    request_title = "SPY×FAMILY アーニャ･フォージャー フルセット"
    return render_template("request.html", request_title=request_title)


# 新しい依頼追加するページへのリダイレクト
@app.route('/new_request_base/<step>', methods=['GET'])
def new_request_base(step):
    return render_template(f"new_request_{step}.html")
