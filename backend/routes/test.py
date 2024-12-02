from . import app
from flask import Flask,render_template, request, redirect
from db.admin_manage import admin_manage


@app.route('/test')
def test():
    print('test')

    admin1 = {
        'admin_id':'A_00000000',
        'admin_name':'権限なし',
        'admin_password':'1234',
        'admin_permissions':'0000000'
    }

    if not admin_manage().register_admin(admin1):
        print('admin1成功')
    else:
        print('admin1失敗')

    admin2 = {
        'admin_id':'A_11111111',
        'admin_name':'全権限',
        'admin_password':'1234',
        'admin_permissions':'1111111'
    }

    if not admin_manage().register_admin(admin2):
        print('admin2成功')
    else:
        print('admin2失敗')
    
    return redirect('/')
    

