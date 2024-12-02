from flask_mail import Mail
from routes import app

# メールサーバ
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587  # TLSは587、SSLなら465
app.config['MAIL_USERNAME'] = 'chinntaro31@gmail.com'
app.config['MAIL_PASSWORD'] = 'rtvxujdnsiogpvpa'  # GmailのApp用のmパスワード設定をしておく必要あり
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEFAULT_SENDER'] = 'chinntaro31@gmail.com'  # これがあるとsender設定が不要になる
mail = Mail(app)


