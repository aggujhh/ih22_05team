from . import app
from flask import render_template
from db.notification_model import notification_model

@app.route('/news')
def index():
    print("newsに接続しました")
    notifications = notification_model().get_notifications()
    return render_template('news.html', notifications=notifications)
