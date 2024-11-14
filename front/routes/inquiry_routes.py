from . import app
from flask import render_template, request
from db.inquiry_model import Inquiry_model
from flask_login import current_user


@app.route("/send_inquiry", methods=['POST'])
def send_inquiry():
    data = request.form
    user_id = current_user.id if current_user.is_authenticated else None
    if Inquiry_model().add_inquiry(user_id, data):
        alert_message = "お問い合わせの送信に成功した。"
    else:
        alert_message = "送信に失敗した。"
    return render_template('inquiry.html', alert_message=alert_message)
