from . import app
from flask import render_template, request, redirect


@app.route("/")
def hello():
    return render_template('index.html', left_margin="224px")


# 依頼一覧ページへのリダイレクト
@app.route('/<nav_name>', methods=['POST'])
def redirect_nav(nav_name):
    left_margin = request.form.get("left_margin")
    html_name = nav_name.strip('<>')
    if html_name == "index":
        return redirect('/')
    else:
        return render_template(f"{html_name}.html", left_margin=left_margin)
