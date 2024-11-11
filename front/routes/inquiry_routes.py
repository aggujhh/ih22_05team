from . import app
from flask import render_template, request
from db.inquiry_model import Inquiry_model


@app.route("/send_inquiry", methods=['POST'])
def send_inquiry():
    data = request.form
    Inquiry_model().add_inquiry(data)
    alert_message = "お問い合わせの送信に成功しました。"
    return render_template('inquiry.html', alert_message=alert_message)
