from . import app
from flask import render_template, request, jsonify
from flask_login import current_user
from db.creator_model import Creator_model
import os


# もっと制作者を読み込む
@app.route('/load_new_creators', methods=['POST'])
def load_new_creators():
    pass
    load_count = int(request.form.get("load_count"))
    limit_start = load_count * 4
    try:
        results = Creator_model().load_creators(limit_start)
        if results:
            for result in results:
                icon_path = f"img/uploads/{result['user_id']}/icon_url/image_icon_url.png"
                file_path = os.path.join(app.config['STATIC_DIR'], icon_path)
                if not os.path.exists(file_path):
                    icon_path = f"img/default_avatar.png"
                result["icon_path"] = icon_path
                if result['creator_notification'] is not None:
                    result['creator_notification'] = result['creator_notification'].replace("\r\n", "<br>")
                if result['categorys']:
                    result['category_stages'] = result['categorys'].split(",")
                    result['category_names'] = ["衣装", "造形", "小道具", "ウィッグ", "アクセサリー", "その他"]
                    result['category_colors'] = ["#F28C8E", "#FCB869", "#CACA61", "#3FABA4", "#6591C0", "#AC7EAE"]
                if result['images']:
                    result['images_list'] = result['images'].split(",")
                    if len(result['images_list']) > 3:
                        result['images_list'] = result['images_list'][:3]
                    for i in range(len(result['images_list'])):
                        result['images_list'][
                            i] = f"/img/uploads/{result['user_id']}/design_preview/{result['images_list'][i]}"
            return jsonify({'message': '読み込み完了。', 'data': results})
        else:
            return jsonify({'message': '依頼はこの以上です。'})
    except Exception as e:
        return jsonify({'error': f'エラー発生 >>> {e}'})


# 制作者詳細情報ページへのリダイレクト
@app.route('/creator/<user_id>', methods=['POST'])
def creator_details(user_id):
    # result = Request_model().fetch_request_by_request_id(request_id)
    # for index, photo in enumerate(result['photos']):
    #     result['photos'][index] = f"img/uploads/{result['user_id']}/requests/{result['request_id']}/{photo}"
    # result['request_content'] = result['request_content'].replace("\r\n", "<br>")
    # result['required_points'] = result['required_points'].replace("\r\n", "<br>")
    # result['year'] = result['request_deadline'].year
    # result['month'] = result['request_deadline'].month if result['request_deadline'].month > 10 else "0" + str(
    #     result['request_deadline'].month)
    # result['day'] = result['request_deadline'].day if result['request_deadline'].day > 10 else "0" + str(
    #     result['request_deadline'].day)
    return render_template("creator.html", result=user_id)
