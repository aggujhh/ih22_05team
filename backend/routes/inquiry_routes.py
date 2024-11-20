from . import app
from flask import Flask,render_template, request, flash, redirect,jsonify
from secrets import token_hex
from db.application_model import creator_request_model
from db.userm_model import Userm_model
from db.inquiry_model import inquiry_model
import logging









##############################################
# お問い合わせ一覧画面
##############################################
@app.route('/inquiry_list')
def inquiry_list():
    print('inquiry_list')
    msg = ''
    # DBから情報取り出し
    inquiries = inquiry_model().get_inquiries()
    print(inquiries)
    if not inquiries:
        msg = '0件です'
    return render_template('inquiry_list.html',inquiries=inquiries, msg=msg)


##############################################
# お問い合わせ詳細画面
##############################################
@app.route('/inquiry_detail/<string:inquiry_id>', methods=['GET','POST'])
def inquiry_detail(inquiry_id):
    if request.method == 'GET':
        print('inquiry_detail GET')
        inquiry = inquiry_model().get_inquiry(inquiry_id)
        print('inquiry',inquiry)
        status = ['未確認', '対応中', '解決', '保留']
        category = ['アカウントについて','取引について','通報']
        inquiry['inquiry_category'] = category[int(inquiry['inquiry_category'])]
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

        return redirect('inquiry_list')


