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


# #1번질문
# def one(){
#     #만약 val값이 "건성"이라면 
#     return "feature = 건성"
# }
def one():
    if val=="건성":
        return "건성"

    
def two():
    if val=="건성":
        return "건성"



def three():
    if val=="지성":
        return "지성"


def four():
    if val=="지루성":
        return "지루성"

def five():
    if val=="지성":
        return "지성"

    
def six():
    if val=="지성":
        return "지성"

    

def seven():
    if val=="지성":
        return "지성"


def seven():
    if val=="지성":
        return "지성"

def eight():
    if val=="쿨링":
        return "쿨링"

def nine():
    if val=="민감성":
        return "민감성"
 

def ten():
    if val=="민감성":
        return "민감성"
   

def eleven():
    if val=="민감성":
        return "민감성"
 
def twelve():
    if val=="민감성":
        return "민감성"
 
def thirteen():
    if val=="탈모":
        return "탈모"
   
def fourteen():
    if val=="민감성":
        return "민감성
    

def fifteenth():
    if val=="지루성":
        return "지루성"

def sixteen():
    if val=="탈모":
        return "탈모"


# sql문 결과 출력(test)
def result_sql(level):
    # sql문 임의로 생성(test)
    if level==0:
        sql = "SELECT * FROM shampoo_0 WHERE brand = %s"
    elif level==1:
        sql = "SELECT * FROM shampoo_1 WHERE brand = %s"
    elif level==2:
        sql = "SELECT * FROM shampoo_2 WHERE brand = %s"
    else:
        sql = "SELECT * FROM shampoo_3 WHERE brand = %s"
    
    
    with conn:
        with conn.cursor() as cur:
            cur.execute(sql,('닥터그루트'))
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
    result_sql(answer)
    return flask.jsonify(res)

    
# 메인
if __name__ == "__main__":
    load_model()
    application.run(host='0.0.0.0')
