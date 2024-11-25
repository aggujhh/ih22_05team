from . import app
from flask import Flask,render_template, request, flash, redirect,jsonify
from secrets import token_hex
from flask_login import login_required
from db.application_model import creator_request_model
from db.userm_model import Userm_model
from db.inquiry_model import inquiry_model
from db.account_model import account_model
from db.data_model import data_model
import logging
import datetime,re
# グラフ
from pyecharts import options as opts
from pyecharts.charts import Bar





################################################
# DBからの情報を整形して返す関数
# 引数 dict: [ { time:xx, num:xx }, ...] , key:dictのnum
# dictはDATETIMEで並び替え済み
# 返り値 result: { 'yyyy':[x,x,x,x,x,x,x,x,x,x,x,x,], ...}
################################################
def format_data(dict,key):
    print('format_data')
    i = 0
    sum = 0
    array = [0,0,0,0,0,0,0,0,0,0,0,0]
    result = {}
    ay = '' # after y

    # keyに time が含まれる文字列をkeyに設定
    pattern = r".*time.*"
    match_time = next((key for key in dict[0].keys() if re.search(pattern,key)),None)

    while i < len(dict):
        bm = ''

        print('i,max',i,len(dict))
        print('i',dict[i])
        
        # 年月の準備
        y = str(dict[i][match_time].year) 
        m = str(dict[i][match_time].month)
        if i+1 == len(dict):
            ay = 'tail' 
            am = 'tail'
        else:
            ay = str(dict[i+1][match_time].year)
            am = str(dict[i+1][match_time].month)
        
        # 月ごとにデータ
        if y == ay or ay == 'tail':

            # 月の確認(配列の添字を使っているなら場合分けせずに足していけばいいのでは？,それなら,年でソートされていれば月では事前にソートされている必要はない)
            if bm != m and m != am:
                print('int1',int(m))
                array[int(m)-1] = dict[i][key]
                print(array)
            elif m == am: # (bym != ym and ym == aym) or (bym == ym and ym == aym)
                sum+=dict[i][key]
                print(sum)
            elif bm == m and m != am: #bm == m and m != am
                array[int(m)-1] = sum
                print('int2',int(m))
                print(array)
                sum = 0
            bm = m

        # 年ごとのデータ
        if y != ay or ay == 'tail':
            print('y',y)
            result[y] = array
            print('result',result)
            array = [0,0,0,0,0,0,0,0,0,0,0,0]
        i=i+1
            
    return result



        


###############################################
# 情報閲覧
###############################################

# 情報閲覧画面表示
@app.route('/data', methods=(['POST','PUT']))
@login_required 
def data():
    if request.method == 'POST':
        print('data')

        # DBから情報取り出し
        ## 依頼者数(月ごとにカウント), 制作者数(月ごとにカウント)
        requester,creator = data_model().get_users() # {'USER_NUM':5, 'create_time': '2024-10-31 18:27:07' }
        print('requester',requester)
        print('creator',creator)
        #requester = format_data(requester,'create_time', 'USER_NUM')
        #creator = format_data(creator, 'create_time', 'USER_NUM')
        requester = format_data(requester,'USER_NUM')
        creator = format_data(creator,'USER_NUM')
        print('requester',requester)
        print('creator',creator)

        ## 依頼数(月ごとにカウント),依頼登録時間がなかったので依頼期限を用いた
        request_data = format_data(data_model().get_request(),'request_num') # {'request_deadline':1, 'request_deadline':'2024-08-10' }
        print('request1',request_data)
        ## 取引数(月ごとにカウント)
        contract_data = data_model().get_contract()
        contract_num = format_data(contract_data,'contract') # {'}
        #contract_num = []
        #for data in contract:
        #    contract_num.append( {'time':data['time'], 'contract':data['num']} )    
        print('contract',contract_num)

        ## 売上管理(月ごとに入金額の合計)
        contract_amount = []
        contract_amount = format_data(contract_data,'amount')
        #for data in contract_data:
        #    contract_amount.append( {'time':data['time'], 'amount':data['num']})
        print('contract amount',contract_amount)

        ### 手数料を考慮して売上を算出

        # グラフ生成
        x_data = ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"]

        c = (
            Bar()
            .add_xaxis(xaxis_data=x_data)
            .add_yaxis("依頼者", requester['2024'])
            .add_yaxis("制作者", creator['2024'])
            .set_global_opts(
                title_opts=opts.TitleOpts(title=""),
                datazoom_opts=opts.DataZoomOpts(),
            )
        #    .render("data.html")
        )

        return render_template('data.html',chart_options=c.dump_options_with_quotes())