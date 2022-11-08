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
# conn = pymysql.connect(host='localhost',
#                        port=3306,
#                        user='root',
#                        passwd='1234',
#                        db='products',
#                        charset='utf8')

# sql = "SELECT * FROM product WHERE brand = %s"

# def connect_sql():
#     print('hi')
#     with conn:
#         with conn.cursor() as cur:
#             cur.execute(sql,('TS'))
#             result = cur.fetchall()
#             for data in result:
#                 print(data)
    

def load_model():
    global model
    model = tensorflow.keras.models.load_model('/workspace/firstContainer/daehan.h5')

@application.route("/api/hello",methods=["POST"])
def api_hello():
    global msg
    req=flask.request.get_json()
    msg=req['userRequest']['utterance']
    #mov=req['action']['clientExtra']['m1']
    print(req)
    #print(msg)
    #print(mov)
    res = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": msg+"kang"
                        }
                    }
                ]   
            }
        }
    return flask.jsonify(res)


@application.route("/api/val",methods=["POST"])
def api_val():
    global val
    req=flask.request.get_json()
    print(req)
    val.append(req['action']['clientExtra']['val'])
    print(req['action']['clientExtra']['val'])
    return req

#결과 출력
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
    result_str = str(result_arr)
    

    
    print("\n")

    print("np array 문자열로변환")
    print(result_str)
    val=[]
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
    return flask.jsonify(res)

    



if __name__ == "__main__":
    load_model()
    connect_sql()
    application.run(host='0.0.0.0')
    