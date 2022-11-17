import flask
import tensorflow.keras
from keras.models import load_model
import pymysql
import numpy as np
import sys

application = flask.Flask(__name__)

msg=[]
model = None
val = []

# 문진 모델 불러오기
def load_model():
    global model
    model = tensorflow.keras.models.load_model('/workspace/firstContainer/daehan.h5')

    
# ubuntu서버의 mysql연동
conn = pymysql.connect(host='localhost',
                       port=3306,
                       user='root',
                       passwd='123',
                       db='product',
                       charset='utf8')




#건성일때 카운트증가
cnt_gunsung = 0
@application.route("/api/get_gunsung",methods=["POST"])
def get_gunsung():
    global cnt_gunsung
    req=flask.request.get_json()
    msg = req['action']['clientExtra']['val']
    if msg == "건성":
        cnt_gunsung += 1
    return req

#민감성일때 카운트증가
cnt_mingam = 0
@application.route("/api/get_mingam",methods=["POST"])
def get_mingam():
    global cnt_mingam
    req=flask.request.get_json()
    msg = req['action']['clientExtra']['val']
    if msg == "민감성":
        cnt_mingam += 1
    return req
        
#가격 가져오기
price = 0
@application.route("/api/get_price",methods=["POST"])
def check_price():
    global price
    req = flask.request.get_json()
    price = int(req['action']['clientExtra']['val'])
    print(price)
    return req

#SQL결과출력
def result_sql(level):
    global price
    print("함수들어오자마자 ", price)
    
    with conn:
        with conn.cursor() as cur:
            #건성체크
            if cnt_gunsung <= 2:
                q1 = "NOT LIKE '%건성%'"
            else:
                q1 = "LIKE '%건성%'"
                
            #민감성체크
            if cnt_mingam <= 1:
                q2 = "NOT LIKE '%민감성%'"
            else:
                q2 = "LIKE '%민감성%'" 
            
            #가격체크
            if price == 15000:
                q3 = "price <= 15000"

            elif price == 30000:
                q3 = "price > 15000 && price <= 30000"
            else:
                q3 = "price > 30000"

 
            #sql문 작성
            if level == 0:
                sql = " "
            elif level == 3:
                sql = " "
            else:
                sql = (
                    "SELECT * "
                    "FROM shampoo_1 "
                    "WHERE feature " +q1+ " AND feature " +q2+ " AND "+q3)
            cur.execute(sql)
            result = cur.fetchall()
            for data in result:
                print(data)

   
            
            
# 그냥 요청값 불러오는지 테스트코드
@application.route("/api/hello",methods=["POST"])
def api_hello():
    global msg
    req=flask.request.get_json()
    
    # 사용자가 입력한 요청메시지 추출
    msg=req['userRequest']['utterance']
    res = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": msg
                        }
                    }
                ]   
            }
        }
    return flask.jsonify(res)


# 사용자 요청을 배열에 저장
@application.route("/api/val",methods=["POST"])
def api_val():
    global val
    req=flask.request.get_json()
    val.append(req['action']['clientExtra']['val'])
    print(req['action']['clientExtra']['val'])
    return req

# 결과 출력
@application.route("/api/result",methods=["POST"])
def api_result():
    global val
    result_arr = []
    
    req=flask.request.get_json()
    msg=''
    for i in val:
        msg += i
    print(msg)
    result_arr = model.predict(np.array([[int(msg[0]),int(msg[1]),int(msg[2]),int(msg[3]),int(msg[4]),int(msg[5]),int(msg[6])]]))[0][0]
    
    # np array로 형변환해서 반환
    result_str = str(result_arr)
    result_float = float(result_str)
    
    if(0 <= result_float*100 < 10):
        answer = 0
    elif(10 <= result_float*100 < 50):
        answer = 1
    elif(50 <= result_float*100 < 90):
        answer = 2
    else:
        answer = 3

    res = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": answer
                        }
                    }
                ]
            }
        }
    
    # 선택값 초기화
    val=[]
    result_sql(1)
    return flask.jsonify(res)

    
# 메인
if __name__ == "__main__":
    load_model()
    application.run(host='0.0.0.0')
    