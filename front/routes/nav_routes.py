from . import app
from flask import render_template, request, redirect
from db.request_model import Request_model


@app.route("/")
def hello():
    return render_template('index.html', left_margin="224px")


# すべてのナビのページへのリダイレクト
@app.route('/<nav_name>', methods=['POST'])
def redirect_nav(nav_name):
    left_margin = request.form.get("left_margin")
    if nav_name == "index":
        return redirect('/')
    elif nav_name == "requests":
        results = Request_model().fetch_all_requests()
        for result in results:
            result['image_path'] = f"img/uploads/{result['user_id']}/requests/{result['request_id']}/{result['photo_name']}"
        return render_template(f"{nav_name}.html", left_margin=left_margin, results=results)
    else:
        return render_template(f"{nav_name}.html", left_margin=left_margin)



