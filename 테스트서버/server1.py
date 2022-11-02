import flask
from keras.models import load_model
model = load_model('/workspace/firstContainer/daehan.h5')

import sys
application = flask.Flask(__name__)
msg=[]

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
                            "text": msg+"TEST"
                        }
                    }
                ]
            }
        }
    return flask.jsonify(res)

if __name__ == "__main__":
    application.run(host='0.0.0.0')
