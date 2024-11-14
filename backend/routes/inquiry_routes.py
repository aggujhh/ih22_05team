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
@app.route('/inquiry_detail')
def inquiry_detail():
    print('inquiry_detail')
# @app.route('/inquiry_detail/<string:creator_application_id>', methods=['GET','POST'])
# def inquiry_detail(creator_application_id):
#     if request.method=='GET': # 申請詳細画面の表示
#         print('/application_detail GET')
#         creator = creator_request_model().get_detail(creator_application_id)
#         print('creator',creator)
#         ## 画像
#         return render_template('application_detail.html', creator=creator)

#     if request.method=='POST': # 申請詳細の反映
#         print('/application_detail POST')
#         status = request.form['possibility']
        
#         if status == '1':
#             print('allow',status)
#             # 申請者の情報を制作者アカウントに登録

#             ## 制作者アカウント作成
#             creator = creator_request_model().get_detail(creator_application_id)
#             ### ユーザID生成
#             user_id = token_hex(5)
#             while Userm_model().user_authentication(user_id):
#                 user_id = token_hex(5)
#             user = {
#                 'user_id':user_id,
#                 'user_password':creator['creator_password'],
#                 'user_type':status,
#                 'user_email_address':creator['creator_mail'],
#                 'nickname':creator['creator_nickname_id']
#             }

#             try:
#                 # Usermにuser_id,hashed_ps,ユーザ種類,ユーザ状態を登録
#                 print(1)
#                 Userm_model().add_user(user)
#                 print(2)
#                 creator_request_model().add_img(user) # 製作可能イメージ図に画像登録
#                 print('11',creator['creator_application_id'], status)
#                 creator_request_model().change_status(creator['creator_application_id'], status)# 制作者申請のステータスを承認に変更
#                 print(3)
#                 # mail送信
#             except Exception as e:
#                 # エラーが発生した場合、エラーログを記録
#                 logging.error(f"Error occurred: {e}")
#                 #alert_message = "登録失敗"
#                 # 登録が失敗した場合のメッセージ

#         # 申請却下
#         if status == '2':
#             print('deny',status)
#             creator_request_model().change_status(creator['creator_application_id'], status)# 制作者申請のステータスを承認に変更
            
#         return redirect('/application_list')

