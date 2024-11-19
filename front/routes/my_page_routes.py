from . import app
from flask import render_template, request, redirect, jsonify, url_for
from flask_login import login_required, current_user
from db.my_page_model import My_page_model
import base64
import os
from severs.global_data import global_data
import json
import uuid


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


class Temp_image_names:
    def __init__(self, user_id):
        self.user_id = user_id
        self.image_list = []

    def reset(self, new_image_list):
        self.image_list = new_image_list

    def add(self, image_name):
        self.image_list.append(image_name)

    def remove(self, image_name):
        if image_name in self.image_list:
            self.image_list.remove(image_name)
            return True
        return False

    def get(self):
        return self.image_list


user_instances = {}


def get_user_instances(user_id):
    if user_id not in user_instances:
        user_instances[user_id] = Temp_image_names(user_id)
    return user_instances[user_id]


@app.route("/my_page/<page_num>")
@login_required
def my_page(page_num):
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
    if num == "1":
        alert_message = request.args.get('alert_message')
        result = My_page_model().fetch_creator_data_by_id(current_user.id)
        saved_image_names = get_user_instances(current_user.id)
        saved_image_names.reset(result['images'])
        print(saved_image_names.get())
        result['image_paths'] = []
        for i in result['images']:
            image_path = f"img/uploads/{current_user.id}/design_preview/{i}"
            result['image_paths'].append(image_path)
        return render_template(f'my_page_9_1.html', page_num="1", page_name_list=page_name_list, num=num,
                               result=result, alert_message=alert_message)
    return render_template(f'my_page_9_{num}.html', page_num="1", page_name_list=page_name_list, num=num)


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


@app.route("/update_creator_setting", methods=['POST'])
@login_required
def update_creator_setting():
    try:
        saved_image_names = get_user_instances(current_user.id)
        image_names = saved_image_names.get()
        file_base_path = os.path.join(app.config['UPLOADS_FOLDER'], current_user.id, "design_preview")
        os.makedirs(file_base_path, exist_ok=True)  # フォルダを再作成（存在しない場合は新規作成）

        # 获取文件夹中的所有文件和子目录
        files_and_dirs = os.listdir(file_base_path)

        for f in files_and_dirs:
            if f not in image_names:
                os.remove(file_base_path + "\\" + f)

        data = request.form.to_dict()
        # 保存されたファイル名をリストに追加
        images = json.loads(data.get("image"))['images']
        # ベースパスを構築（ユーザーごとのdesign_previewフォルダ）
        for idx, image_data in enumerate(images):
            # Base64データは通常 'data:image/jpeg;base64,' 形式で始まるため、ヘッダー部分を削除
            if 'base64,' in image_data:
                image_data = image_data.split('base64,')[1]
            # Base64文字列をバイナリデータにデコード
            img_data = base64.b64decode(image_data)
            # 一意のファイル名を生成（UUIDを利用）
            file_name = f'image_{uuid.uuid4()}.png'
            # 最終的な保存パスを生成（ファイル名を結合）
            file_path = os.path.join(file_base_path, file_name)
            # バイナリデータをファイルに書き込む
            with open(file_path, 'wb') as img_file:
                img_file.write(img_data)
            saved_image_names.add(file_name)
        data["image"] = saved_image_names.get()
        My_page_model().update_creator(current_user.id, data)
        alert_message = "内容修正成功しました。"
        return redirect(url_for("production_management", num="1", alert_message=alert_message))
    except Exception as e:
        alert_message = f'エラー発生 >>> {e}'
        return redirect(url_for("production_management", num="1", alert_message=alert_message))


@app.route("/delete_image", methods=['POST'])
@login_required
def delete_image():
    image_name = request.form.get("image_name")
    saved_image_names = get_user_instances(current_user.id)
    if saved_image_names.remove(image_name):
        print(saved_image_names.get())
        return jsonify({'message': '削除成功しました。'})
    else:
        return jsonify({'message': '削除失敗。'})
