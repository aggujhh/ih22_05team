from . import app
from flask import render_template, request, redirect
from db.request_model import Request_model
from db.notification_model import notification_model
from db.creator_model import Creator_model
import os
import math
from flask_login import current_user


@app.route("/", methods=['GET', 'POST'])
def hello():
    requests, requests_count = Request_model().fetch_all_requests()
    for result in requests:
        result['image_path'] = f"img/uploads/{result['user_id']}/requests/{result['request_id']}/{result['photo_name']}"
    creators, creators_count = Creator_model().fetch_all_creators()
    creators_count = math.ceil(int(creators_count['COUNT(*)']) / 4)
    print(creators, creators_count )
    if creators and creators_count:
        for result in creators:
            icon_path = f"img/uploads/{result['user_id']}/icon_url/image_icon_url.png"
            file_path = os.path.join(app.config['STATIC_DIR'], icon_path)
            if not os.path.exists(file_path):
                icon_path = f"/img/default_avatar.png"
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
                    
    return render_template('index.html', left_margin="0px", requests=requests, creators=creators,
                           creators_count=creators_count)


# すべてのナビのページへのリダイレクト
@app.route('/<nav_name>', methods=['POST'])
def redirect_nav(nav_name):
    left_margin = request.form.get("left_margin")
    if nav_name == "index":
        return redirect('/')
    elif nav_name == "news":
        print("newsに接続しました")
        notifications = notification_model().get_notifications()
        return render_template('news.html', left_margin=left_margin, notifications=notifications)
    elif nav_name == "requests":
        results, count = Request_model().fetch_all_requests()
        for result in results:
            result[
                'image_path'] = f"img/uploads/{result['user_id']}/requests/{result['request_id']}/{result['photo_name']}"
        return render_template(f"{nav_name}.html", left_margin=left_margin, results=results, count=count['COUNT(*)'])
    elif nav_name == "creators":
        results, count = Creator_model().fetch_all_creators()
        for result in results:
            icon_path = f"img/uploads/{result['user_id']}/icon_url/image_icon_url.png"
            file_path = os.path.join(app.config['STATIC_DIR'], icon_path)
            if not os.path.exists(file_path):
                icon_path = f"/img/default_avatar.png"
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

        print(results, count)
        return render_template('creators.html', left_margin=left_margin, results=results, count=count['COUNT(*)'])
    elif nav_name == "inquiry":
        error_msg = []
        return render_template(f"{nav_name}.html", left_margin=left_margin, error_msg=error_msg)
    else:
        return render_template(f"{nav_name}.html", left_margin=left_margin)


@app.errorhandler(405)
def page_not_found(e):
    return render_template('404.html'), 405
