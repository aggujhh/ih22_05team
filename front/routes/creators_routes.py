from . import app
from flask import render_template, request, jsonify
from db.creator_model import Creator_model
import os


# もっと制作者を読み込む
@app.route('/load_new_creators', methods=['POST'])
def load_new_creators():
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
    result = Creator_model().fetch_creator_by_id(user_id)
    if result:
        icon_path = f"img/uploads/{result['user_id']}/icon_url/image_icon_url.png"
        file_path = os.path.join(app.config['STATIC_DIR'], icon_path)
        if not os.path.exists(file_path):
            icon_path = f"img/default_avatar.png"
        result["icon_path"] = icon_path
        bg_img_path = f"img/uploads/{result['user_id']}/background_photo_url/image_background_photo_url.png"
        file_path = os.path.join(app.config['STATIC_DIR'], bg_img_path)
        if not os.path.exists(file_path):
            bg_img_path = f"img/default_bg_img.png"
        result["bg_img_path"] = bg_img_path
        if result['creator_notification'] is not None:
            result['creator_notification'] = result['creator_notification'].replace("\r\n", "<br>")
        if result['profile'] is not None:
            result['profile'] = result['profile'].replace("\r\n", "<br>")
        if result['categorys']:
            result['category_stages'] = result['categorys'].split(",")
            result['category_names'] = ["衣装", "造形", "小道具", "ウィッグ", "アクセサリー", "その他"]
            result['category_colors'] = ["#F28C8E", "#FCB869", "#CACA61", "#3FABA4", "#6591C0", "#AC7EAE"]
        if result['images']:
            result['images_list'] = result['images'].split(",")
            result['image_path_list'] = []
            for i in result['images_list']:
                result['image_path_list'].append(f"/img/uploads/{result['user_id']}/design_preview/{i}")
    to_bottom = bool(request.form.get("to_bottom"))
    if not to_bottom:
        to_bottom = False
    print("to_bottom>>>>>>>>>>", to_bottom, type(to_bottom))
    return render_template("creator.html", result=result, to_bottom=to_bottom)


# 画像表示
@app.route('/show_image/<user_id>/<image_name>')
def show_image(user_id, image_name):
    image_path_list = f"/img/uploads/{user_id}/design_preview/{image_name}"
    return render_template("show_image.html", result=image_path_list, user_id=user_id)
