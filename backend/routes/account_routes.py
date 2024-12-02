from . import app
from flask import Flask,render_template, request, redirect
from flask_login import login_required, current_user
from db.account_model import account_model
from db.log_model import log_model
from decorators.permission_decorators import permission_required



########################################
# 不正検知処理
########################################

# 不正検知一覧画面表示
@app.route('/fraud_reports')
@login_required 
@permission_required(2)
def fraud_reports():
    print('fraud_reports')
    # DBから情報取り出し
    reports = account_model().get_reports()
    log_model().update_log(current_user.id,'不正検知一覧画面表示','不正検知一覧画面表示')
    return render_template('fraud_reports.html',reports=reports)


# 不正検知詳細
@app.route('/fraud_report_detail/<string:fraud_report_id>', methods=(['GET','POST']))
@login_required 
@permission_required(2)
def fraud_report_detail(fraud_report_id):

    # 不正検知詳細画面表示
    if request.method == 'GET':
        print('fraud_report_detail GET',fraud_report_id)
        # DBから情報取り出し
        report = account_model().get_report(fraud_report_id)
        judge = ['未確認', '違反', '違反でない']
        log_model().update_log(current_user.id,'不正検知詳細画面表示',f'表示情報 報告id:{fraud_report_id}')
        return render_template('fraud_report_detail.html',report=report,judge=judge)

    # 詳細画面での変更項目をDBに反映させる処理
    if request.method == 'POST':
        print('fraud_report_detail POST ', fraud_report_id)
        # クライアントから情報受取
        data = request.form
        print('data',data)
        # DBに情報登録
        if account_model().update_report(data):
            log_model().update_log(current_user.id,'不正検知詳細反映',f'反映情報:{data}')
            return redirect('/fraud_reports')

        e = 'DB反映エラー'
        return redirect('/error',e=e)

    




########################################
# 凍結解除申請処理 
########################################

# 凍結解除申請一覧表示
@app.route('/unfreeze_request')
@login_required 
@permission_required(2)
def unfreeze_request():
    print('unfreeze_request')
    # DBへSQL文依頼,一覧情報取得
    data = account_model().get_thaw_list()
    if not data:
        msg = '0件です'
    log_model().update_log(current_user.id,'凍結解除申請一覧表示',f'一覧表示')
    return render_template('unfreeze_request.html',data=data,msg=msg)

# 凍結解除詳細
@app.route('/unfreeze_request_detail/<string:unfreeze_request_id>', methods=(['GET','POST']))
@login_required 
@permission_required(2)
def unfreeze_request_detail(unfreeze_request_id):
    if request.method == 'GET':
        print('unfreeze_request_id')
        # SQL文実行,一覧情報取得
        data = account_model().get_thaw_request(unfreeze_request_id)
        log_model().update_log(current_user.id,'凍結解除詳細表示',f'表示情報 id{unfreeze_request_id},data:{data}')
        return render_template('unfreeze_request_detail.html',data=data)
    if request.method == 'POST':
        print('unfreeze_request_detail POST', unfreeze_request_id)
        data = request.form
        print('data',data)
        # 変更内容をDBに反映
        ## 内容が変更されたかをチェックしてか,全部DBに反映するのだとどっちのほうが早い？
        if account_model().update_thaw_request(data):
            log_model().update_log(current_user.id,'凍結解除',f'凍結解除:{data}')
            return redirect('/unfreeze_request')
        
        # エラー時にエラーハンドリング,デコレータ
        print('error')
