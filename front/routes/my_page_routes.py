from . import app
from flask import render_template, request, redirect
from flask_login import current_user, login_required


@app.route("/my_page/<page_num>")
@login_required
def my_page(page_num):
    page_name_list = [
        "依頼管理",
        "プロフィール設定",
        "個人情報設定",
        "採寸早見表設定",
        "ポイント",
        "クーポン",
        "通知設定",
        "アカウント削除",
    ]
    return render_template(f'my_page_{page_num}.html', page_num=int(page_num),page_name_list=page_name_list)
