from . import app
from flask import render_template, request, redirect

ALLOWED_NAV_PAGES = ["index", "requests", "creators", "guide", "news", "contact", "faq"]


@app.route("/")
def hello():
    return render_template('index.html', left_margin="224px")


# 依頼一覧ページへのリダイレクト
@app.route('/redirect/<nav_name>')
def redirect_nav(nav_name):
    print(nav_name)
    left_margin = request.args.get("left_margin")
    nav_number = int(nav_name.strip('<>'))
    html_name = ALLOWED_NAV_PAGES[nav_number]
    print(nav_number)
    if nav_number == 0:
        return redirect('/')
    else:
        return render_template(f"{html_name}.html", left_margin=left_margin)
