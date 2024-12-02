from . import app
from flask import Flask,render_template, request, redirect
from flask_login import login_required,current_user
from db.inquiry_model import inquiry_model
from db.log_model import log_model
from decorators.permission_decorators import permission_required









##############################################
# お問い合わせ一覧画面
##############################################
@app.route('/inquiry_list')
@login_required 
@permission_required(5)
def inquiry_list():
    print('inquiry_list')
    msg = ''
    # DBから情報取り出し
    inquiries = inquiry_model().get_inquiries()
    print(inquiries)
    if not inquiries:
        msg = '0件です'
    log_model().update_log(current_user.id,'お問い合わせ一覧表示','お問い合わせ一覧表示')    
    return render_template('inquiry_list.html',inquiries=inquiries, msg=msg)


##############################################
# お問い合わせ詳細画面
##############################################
@app.route('/inquiry_detail/<string:inquiry_id>', methods=['GET','POST'])
@login_required 
@permission_required(5)
def inquiry_detail(inquiry_id):
    if request.method == 'GET':
        print('inquiry_detail GET')
        inquiry = inquiry_model().get_inquiry(inquiry_id)
        print('inquiry',inquiry)
        status = ['未確認', '対応中', '解決', '保留']
        category = ['アカウントについて','取引について','通報']
        inquiry['inquiry_category'] = category[int(inquiry['inquiry_category'])]
        log_model().update_log(current_user.id,'お問い合わせ詳細表示',f'お問い合わせ詳細表示 ID:{inquiry_id}')    
        return render_template('inquiry_detail.html',inquiry=inquiry, status=status)
    
    if request.method == 'POST':
        print('inquiry_detail POST' )
        data = request.form
        print('data',data)
        print('status category',data['inquiry_status'], data['inquiry_category'])

        if inquiry_model().update_inquiry(data):
            print('yes')
        else:
            print('no')

        log_model().update_log(current_user.id,'お問い合わせ詳細変更',f"変更後の情報 ID:{inquiry_id}, 状態:{data['inquiry_status']}, カテゴリー:{data['inquiry_category']}")    
        return redirect('inquiry_list')


