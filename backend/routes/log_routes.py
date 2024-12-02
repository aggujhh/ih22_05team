from . import app
from flask import Flask,render_template
from flask_login import login_required, current_user
from db.log_model import log_model
from decorators.permission_decorators import permission_required





####################################################
# ログ閲覧
####################################################
@app.route('/log', methods=['GET'])
@login_required
@permission_required(3)
def log():
    print('log')
    log = log_model().get_log()
    log_model().update_log(current_user.id,'ログ閲覧','ログ閲覧')
    return render_template('log.html',log=log)