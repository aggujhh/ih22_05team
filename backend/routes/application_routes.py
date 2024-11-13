from . import app, global_data
from flask import Flask,render_template, request, flash, redirect,jsonify
from db.application_model import creator_request_model








##############################################
# 制作者申請画面
##############################################
@app.route('/application_list')
def application_list():
    print('application_list')
    # DBから情報取り出し
    creator_list = creator_request_model().get_creator_list()
    return render_template('application_list.html',creator_list=creator_list)


##############################################
# 制作者申請詳細画面
##############################################
@app.route('/application_detail/<string:creator_application_id>', methods=['GET','POST'])
def application_detail(creator_application_id):
    if request.method=='GET': # 申請詳細画面の表示
        print('/application_detail GET')
        creator = creator_request_model().get_detail(creator_application_id)
        return render_template('application_detail.html', creator=creator)

    if request.method=='POST': # 申請詳細の反映
        print('/application_detail POST')
        
        result = request.form['possibility']
        if result == '0':
            print('allow')

            # 申請者の情報を制作者アカウントに
            ## 制作者アカウント作成
            ### ユーザID生成

            ## 申請者情報を削除

            # mail送信
        else:
            print('deny')
        
            

        return redirect('application_list')

