from . import app
from flask import render_template, request, jsonify
from db.userm_model import Userm_model
from db.request_model import Request_model
from flask_login import current_user, login_required
import secrets
import base64
import os
import uuid
import json

data_list = {
    "genre": ["", "", "", "", "", ""],
}


# 依頼詳細情報ページへのリダイレクト
@app.route('/request/<request_id>', methods=['POST'])
def request_details(request_id):
    request_title = "SPY×FAMILY アーニャ･フォージャー フルセット"
    return render_template("request.html", request_title=request_title)


# 新しい依頼追加するページへのリダイレクト
@app.route('/new_request_base/<step>', methods=['GET', 'POST'])
@login_required
def new_request_base(step):
    global data_list
    if request.method == 'GET':
        data_list = {
            "genre": ["", "", "", "", "", ""],
        }
    else:
        for key, value in request.form.items():
            if key == "genre":
                data_list[key] = json.loads(value)
            else:
                data_list[key] = value
    print(data_list)
    return render_template(f"new_request_{step}.html", result=data_list)


# 新しい依頼追加する機能
@app.route('/add_new_request', methods=['POST'])
@login_required
def add_new_request():
    request_model = Request_model()
    request_id = "r_" + secrets.token_hex(10)
    while request_model.have_request_id(request_id):
        request_id = secrets.token_hex(10)
    user_id = Userm_model().fetch_id_by_nickname(current_user.id)
    try:
        request_model.add_request(user_id, request_id, data_list)
        upload_img_of_new_request(request_id)
        return jsonify({'message': '追加成功しました。'})
    except Exception as e:
        return jsonify({'error': f'エラーが発生しました: {e}'})


# 新しい依頼追加する時の写真保存機能
def upload_img_of_new_request(request_id):
    request_model = Request_model()

    user_id_folder = Userm_model().fetch_id_by_nickname(current_user.id)
    # フロントエンドからのJSONデータを取得
    data = request.get_json()
    # 画像データの配列を取得
    images = data.get('images', [])
    # 画像が存在しない場合、エラーを返す
    if not images:
        return jsonify({'error': 'No images received'}), 400
    saved_files = []  # 保存されたファイル名リスト
    for idx, image_data in enumerate(images):
        try:
            # 保存する画像のファイル名を生成
            file_name = f'image_{uuid.uuid4()}.png'  # 必要に応じてファイル形式や命名を変更可能
            request_model.add_request_image_file_name(request_id, file_name)
            # Base64データは通常 'data:image/jpeg;base64,' 形式で始まるため、ヘッダー部分を削除
            if 'base64,' in image_data:
                image_data = image_data.split('base64,')[1]
            # Base64文字列をバイナリデータにデコード
            img_data = base64.b64decode(image_data)
            file_path = os.path.join(app.config['UPLOADS_FOLDER'], user_id_folder, "requests", request_id, file_name)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            # バイナリデータをファイルに書き込む
            with open(file_path, 'wb') as img_file:
                img_file.write(img_data)
            # 保存されたファイル名をリストに追加
            saved_files.append(file_path)
        except Exception as e:
            return jsonify({'error': f'Failed to process image {idx}: {str(e)}'}), 500
