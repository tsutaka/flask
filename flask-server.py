from flask import Flask, jsonify, request # pip install flask
import configparser 
import json

from Chat import chat
from Shiri import shiri

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False

@app.route('/chat/num', methods=['GET'])
def chat_get_num():
    ansjson = chat.get_num()

    response = jsonify(ansjson)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

@app.route('/shiri/status', methods=['GET'])
def shiri_get_status():
    ansjson = shiri.get_data()

    response = jsonify(ansjson)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

@app.route('/shiri/post', methods=['POST'])
def shiri_post():
    request_json = json.loads(request.data.decode('utf-8'))
    print(request_json)
    ansjson = shiri.post_data(request_json["name"])

    response = jsonify(ansjson)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

@app.route('/shiri/reset', methods=['POST'])
def shiri_reset():
    ansjson = shiri.post_reset()

    response = jsonify(ansjson)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=3002)
    # 127.0.0.1:3002/chat/num
    # 127.0.0.1:3002/shiri/status

