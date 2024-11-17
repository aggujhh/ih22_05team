from . import app
from flask import render_template, request, redirect, jsonify
from flask_login import login_required, current_user
from db.my_page_model import My_page_model
import base64
import os
import json
from severs.global_data import global_data


@app.route("/my_page/<page_num>")
@login_required
def my_page(page_num):
    page_name_list = {
        "1": "依頼管理",
        "2": "プロフィール設定",
        "3": "個人情報設定",
        "4": "採寸早見表設定",
        "5": "ポイント",
        "6": "クーポン",
        "7": "通知設定",
        "8": "アカウント削除",
    }
    user_type = global_data.get_user_type(current_user.id)
    if user_type == "1":
        page_name_list["1"] = "制作管理"
    if int(page_num) == 2:
        result = My_page_model().fetch_profile_by_id(current_user.id)
        print(result)
        return render_template(f'my_page_2.html', page_num=page_num, page_name_list=page_name_list, result=result)
    elif int(page_num) == 9:
        return redirect('/my_page/9/1')

    return render_template(f'my_page_{page_num}.html', page_num=page_num, page_name_list=page_name_list)


@app.route("/my_page/9/<num>")
@login_required
def production_management(num):
    result = {
        "genre": ""
    }
    page_name_list = {
        "1": "制作管理",
        "2": "プロフィール設定",
        "3": "個人情報設定",
        "4": "採寸早見表設定",
        "5": "ポイント",
        "6": "クーポン",
        "7": "通知設定",
        "8": "アカウント削除",
    }
    return render_template(f'my_page_9_{num}.html', page_num="1", page_name_list=page_name_list, num=num, result=result)


@app.route("/update_profile", methods=['POST'])
@login_required
def update_profile():
    data = {
        'nickname': '',
        'gender': '0',
        'profile': '',
        'hobby': '',
    }
    for key, value in request.form.items():
        print(key, value)
        data[key] = value
    My_page_model().update_profile(current_user.id, data)
    global_data.set_nickname(current_user.id, data['nickname'])
    return redirect('/my_page/2')


@app.route("/update_profile_images", methods=['POST'])
@login_required
def update_profile_images():
    img_list = {
        'icon_url': '',
        'background_photo_url': ''
    }
    user_id_folder = current_user.id
    data = request.get_json()
    for key, value in data.get("imagesArray").items():
        file_name = f'image_{key}.png'
        img_list[key] = file_name
        if 'base64,' in value:
            value = value.split('base64,')[1]
        img_data = base64.b64decode(value)
        file_path = os.path.join(app.config['UPLOADS_FOLDER'], user_id_folder, key, file_name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        # バイナリデータをファイルに書き込む
        with open(file_path, 'wb') as img_file:
            img_file.write(img_data)
    My_page_model().update_profile_images(current_user.id, img_list)
    return jsonify({'message': 'プロフィール設定成功しました。'})
