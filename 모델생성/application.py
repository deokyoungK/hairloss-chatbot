import flask
import tensorflow.keras
#from keras.models import load_model
import pymysql
import numpy as np
import sys
import urllib.request
from PIL import Image, ImageOps
import json

application = flask.Flask(__name__)

users = {}

model = None
model2 = None

# 문진 모델 불러오기
def load_model():
    global model
    global model2
    model = tensorflow.keras.models.load_model('/workspace/firstContainer/daehan.h5')
    model2 = tensorflow.keras.models.load_model('/workspace/firstContainer/DataflowModel.h5')
    #model = tensorflow.keras.models.load_model('./daehan.h5')
    #model2 = tensorflow.keras.models.load_model('./DataflowModel.h5')
    


#시작블록에서 api 호출
@application.route("/api/user",methods=["POST"])
def api_user():
    global users
    req=flask.request.get_json()
    user_id = req['userRequest']['user']['id']
    #json 유저 포맷
    with open("./users_format.json", 'r') as f:
        temp_json = json.load(f)
        temp_json[user_id]=temp_json['userid']
        del temp_json['userid']
        users.update(temp_json)
    
    #print(users)
    return req


#건성일때 카운트증가
@application.route("/api/get_gunsung",methods=["POST"])
def get_gunsung():
    global users
    req=flask.request.get_json()
    user_id = req['userRequest']['user']['id']
    req_msg = req['action']['clientExtra']['val']
    if req_msg == "건성":
        users[user_id]['product']['cnt_gunsung'] += 1
        
    return req


#민감성일때 카운트증가
@application.route("/api/get_mingam",methods=["POST"])
def get_mingam():
    global users
    req=flask.request.get_json()
    user_id = req['userRequest']['user']['id']
    req_msg = req['action']['clientExtra']['val']
    if req_msg == "민감성":
        users[user_id]['product']['cnt_mingam'] += 1
        
    return req
        
#가격 가져오기
@application.route("/api/get_price",methods=["POST"])
def check_price():
    global users
    req=flask.request.get_json()
    user_id = req['userRequest']['user']['id']
    price = int(req['action']['clientExtra']['val'])
    users[user_id]['product']['price'] = price

    return req

#모발상태 가져오기

@application.route("/api/get_status", methods=["POST"])
def get_status():
    global users
    req=flask.request.get_json()
    user_id = req['userRequest']['user']['id']
    
    sentence = req['action']['clientExtra']['val']
    users[user_id]['product']['sentence'] += sentence 

    return req

# 0단계
@application.route("/api/get_type0", methods=["POST"])
def get_type0():
    global users
    req=flask.request.get_json()
    user_id = req['userRequest']['user']['id']
    
    type0 = req['action']['clientExtra']['val']
    users[user_id]['product']['type0'] = type0

    return req

# 3단계
@application.route("/api/get_type3", methods=["POST"])
def get_type3():
    global users
    req=flask.request.get_json()
    user_id = req['userRequest']['user']['id']
    
    type3 = req['action']['clientExtra']['val']
    users[user_id]['product']['type3'] = type3

    return req


# 결과출력
@application.route("/api/final",methods=["POST"])
def result():
    global users
    req=flask.request.get_json()
    user_id = req['userRequest']['user']['id']

    return result_sql(users[user_id]['predict']['level'], user_id)


# SQL결과
def result_sql(level, user_id):
    global users
    price = users[user_id]['product']['price']
    cnt_mingam = users[user_id]['product']['cnt_mingam']
    cnt_gunsung = users[user_id]['product']['cnt_gunsung']
    
    # ubuntu서버의 mysql연동
    conn = pymysql.connect(host='localhost',
                       port=3306,
                       user='root',
                       passwd='123',
                       db='product',
                       charset='utf8')
    
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
                sql = (
                    "SELECT * "
                    "FROM shampoo_0 "
                    "WHERE " +users[user_id]['product']['type0']+ " ORDER BY RAND()")
            elif level == 3:
                sql = (
                    "SELECT * "
                    "FROM shampoo_3 "
                    "WHERE " +users[user_id]['product']['type3']+ " ORDER BY RAND()")
            elif level == 1:
                sql = (
                    "SELECT * "
                    "FROM shampoo_1 "
                    "WHERE feature " +q1+ " AND feature " +q2+ " AND "+ users[user_id]['product']['sentence'] + " ORDER BY RAND()")
            else:
                sql = (
                    "SELECT * "
                    "FROM shampoo_2 "
                    "WHERE feature " +q1+ " AND feature " +q2+ " AND "+ users[user_id]['product']['sentence'] + " ORDER BY RAND()")
                
            cur.execute(sql)
            result = cur.fetchall()
            rl = list(result)
            
            if(len(rl)==1):
                p_type1 = rl[0][1]
                p_name1 = rl[0][2]
                p_price1 = rl[0][4]
                if(level == 0 or level == 3):
                    p_url1 = rl[0][6]
                else:
                    p_url1 = rl[0][10]
                
                res = {
                  "version": "2.0",
                  "template": {
                    "outputs": [
                      {
                        "carousel": {
                          "type": "listCard",
                          "items": [
                            {
                              "header": {
                                "title": "추천 제품"
                              },
                              "items": [
                                {
                                  "title": p_name1 + "(" +p_type1+ ")" ,
                                  "description": p_price1+"원",
                                  "imageUrl": p_url1
                                }
                              ]
                            }
                          ]
                        }
                      }
                    ]
                  }
                }
            elif(len(rl)==2):
                p_type1 = rl[0][1]
                p_type2 = rl[1][1]

                p_name1 = rl[0][2]
                p_name2 = rl[1][2]

                p_price1 = rl[0][4]
                p_price2 = rl[1][4]
                
                if(level == 0 or level == 3):
                    p_url1 = rl[0][6]
                    p_url2 = rl[1][6]
                else:
                    p_url1 = rl[0][10]
                    p_url2 = rl[1][10]

                res = {
                  "version": "2.0",
                  "template": {
                    "outputs": [
                      {
                        "carousel": {
                          "type": "listCard",
                          "items": [
                            {
                              "header": {
                                "title": "추천 제품"
                              },
                              "items": [
                                {
                                  "title": p_name1 + "(" +p_type1+ ")" ,
                                  "description": p_price1+"원",
                                  "imageUrl": p_url1
                                },
                                {
                                  "title": p_name2 + "(" +p_type2+ ")",
                                  "description": p_price2+"원",
                                  "imageUrl": p_url2
                                }
                              ]
                            }
                          ]
                        }
                      }
                    ]
                  }
                }
            else:
                p_type1 = rl[0][1]
                p_type2 = rl[1][1]
                p_type3 = rl[2][1]

                p_name1 = rl[0][2]
                p_name2 = rl[1][2]
                p_name3 = rl[2][2]

                p_price1 = rl[0][4]
                p_price2 = rl[1][4]
                p_price3 = rl[2][4]

                if(level == 0 or level == 3):
                    p_url1 = rl[0][6]
                    p_url2 = rl[1][6]
                    p_url3 = rl[2][6]
                else:
                    p_url1 = rl[0][10]
                    p_url2 = rl[1][10]
                    p_url3 = rl[2][10]
                    
                res = {
                  "version": "2.0",
                  "template": {
                    "outputs": [
                      {
                        "carousel": {
                          "type": "listCard",
                          "items": [
                            {
                              "header": {
                                "title": "추천 제품"
                              },
                              "items": [
                                {
                                  "title": p_name1 + "(" +p_type1+ ")" ,
                                  "description": p_price1+"원",
                                  "imageUrl": p_url1
                                },
                                {
                                  "title": p_name2 + "(" +p_type2+ ")",
                                  "description": p_price2+"원",
                                  "imageUrl": p_url2
                                },
                                {
                                  "title": p_name3 + "(" +p_type3+ ")",
                                  "description": p_price3+"원",
                                  "imageUrl": p_url3
                                }
                              ]
                            }
                          ]
                        }
                      }
                    ]
                  }
                }

            #유저정보 del
            del users[user_id]
            return flask.jsonify(res)



# 사용자 요청을 배열에 저장
@application.route("/api/val",methods=["POST"])
def api_val():
    global users
    req=flask.request.get_json()
    user_id = req['userRequest']['user']['id']
    users[user_id]['predict']['Hx'].append(req['action']['clientExtra']['val'])
    #val.append(req['action']['clientExtra']['val'])
    print(req['action']['clientExtra']['val'])
    return req


# 문진모델 예
@application.route("/api/result",methods=["POST"])
def api_result():
    global users
    req=flask.request.get_json()
    user_id = req['userRequest']['user']['id']
    result_arr = []
    val = users[user_id]['predict']['Hx']
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
    
    
    #문진*0.3 + 이미지*0.7
    answer = round(answer*0.3 + users[user_id]['predict']['image']*0.7)
    
    users[user_id]['predict']['answer'] = answer
    users[user_id]['predict']['level'] = answer
        
    if(answer == 0):
        res = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": answer
                        }
                    }
                ],
                "quickReplies": [
                    {
                          "label": "블록이동",
                          "action": "block",
                          "blockId": "637e17ca7452e2550afde230"

                    }
                ]
            }
        }

        # 문진,이미지 초기화
        users[user_id]['predict']['Hx'] = []
        users[user_id]['predict']['image'] = 0

        return flask.jsonify(res)
    
    elif(answer == 3):
        res = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": answer
                        }
                    }
                ],
                "quickReplies": [
                    {
                          "label": "블록이동",
                          "action": "block",
                          "blockId": "637e26add0c041460703b01c"

                    }
                ]
            }
        }

        # 문진,이미지 초기화
        users[user_id]['predict']['Hx'] = []
        users[user_id]['predict']['image'] = 0

        return flask.jsonify(res)
    
    else:
        res = {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                                "text": answer
                            }
                        }
                    ],
                    "quickReplies": [
                        {
                              "label": "블록이동",
                              "action": "block",
                              "blockId": "636b873e3236e276c315a9f6"

                        }
                    ]
                }
            }

        # 문진,이미지 초기화
        users[user_id]['predict']['Hx'] = []
        users[user_id]['predict']['image'] = 0

        return flask.jsonify(res)
























@application.route("/api/img", methods=["POST"])
def api_img():
    global users
    req = flask.request.get_json()
    user_id = req['userRequest']['user']['id']
    
    req_img = req['userRequest']['utterance']
    if 'jpg' in req_img or 'png' in req_img:
        np.set_printoptions(suppress=True)	#소수점 제거
        #유저 이미지 저장
        #경로: /workspace/Project/userimage/user_id.png
        #user_img = './userimage/' + user_id
        #urllib.request.urlretrieve(req_img, user_img)
        #image = Image.open(user_img).convert('RGB')
        
        urllib.request.urlretrieve(req_img, 'img')	#img load
        image = Image.open('img').convert('RGB')
        size = (150, 150)
        image = ImageOps.fit(image, size, Image.ANTIALIAS) #방향값 제거, 안티앨리어싱
        image_array = np.asarray(image)
        normalized_image_array = (image_array.astype(np.float32) / 255.0)	#normalizing
        data = np.ndarray(shape=(1, 150, 150, 3), dtype=np.float32)	#reshape
        data[0] = normalized_image_array
        prediction = model2.predict(data)	#예측
        output = np.argmax(prediction, axis=-1)	#가장 높은 예측값
        
        if(output[0] == 4):
            users[user_id]['predict']['image'] = output[0] - 1
        else:
            users[user_id]['predict']['image'] = output[0]
        
        '''
		# basic card format
        res = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "basicCard": {
                            "title": output[0],
                            "description": "",
                            "thumbnail": {
                                "imageUrl": req_img
                            },
                            "buttons": [
                                {
                                    "action":  "webLink",
                                    "label": "상세정보",
                                    "webLinkUrl": req_img
                                }
                            ]
                        }
                    }
                ]
            }
        }'''
        res = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": str(output[0])
                        }
                    }
                ],
                "quickReplies": [
                    {
                          "label": "블록이동",
                          "action": "block",
                          "blockId": "6363af20862f77129379c7cf"

                    }
                ]
            }
        }
    else:
    	# simple text format
        res = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": "사진을 보내주세요"
                        }
                    }
                ]
            }
        }
    #file_path = "./userimage/" + user_id + ".json"
    #with open(file_path, 'w', encoding='utf-8') as outfile:
        #json.dump(res, outfile, ensure_ascii = False)
    return flask.jsonify(res)


    
# 메인
if __name__ == "__main__":
    load_model()
    application.run(host='0.0.0.0')