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

# ubuntu서버의 mysql연동
conn = pymysql.connect(host='localhost',
                       port=3306,
                       user='root',
                       passwd='123',
                       db='product',
                       charset='utf8')

# sql문 임의로 생성(test)
sql = "SELECT * FROM tmp WHERE brand = %s"

# sql문 결과 출력(test)
def result_sql():
    with conn:
        with conn.cursor() as cur:
            cur.execute(sql,('TS'))
            result = cur.fetchall()
            for data in result:
                print(data)

# 문진 모델 불러오기
def load_model():
    global model
    model = tensorflow.keras.models.load_model('/workspace/firstContainer/daehan.h5')

    
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
    res = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": result_str
                        }
                    }
                ]
            }
        }
    
    # 선택값 초기화
    val=[]
    return flask.jsonify(res)

    
# 메인
if __name__ == "__main__":
    load_model()
    result_sql()
    application.run(host='0.0.0.0')
    