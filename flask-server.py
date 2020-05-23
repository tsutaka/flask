from flask import Flask, jsonify # pip install flask

from Chat import chat

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False

@app.route('/chat/num', methods=['GET'])
def chat_get_num():
    ansjson = chat.get_num()

    response = jsonify(ansjson)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=3002)
    # 127.0.0.1:3002/chat/num

