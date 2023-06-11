from flask_cors import CORS
from flask import *
import os
import json
import secrets

app = Flask(__name__)
CORS(app)

tokens = {}

@app.route('/')
def home():
    return 'Hello World!'

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data["username"]
    password = data["password"]

    if os.path.exists('./storage/users/' + username + '.json'):
        with open('./storage/users/' + username + '.json', 'r') as f:
            data = json.load(f)
            if data["password"] == password:
                token = secrets.token_hex(16)
                tokens[username] = token
                return jsonify({"success": True, "token": token})
            else:
                return jsonify({"success": False})
    else:
        return jsonify({"success": False})


@app.route('/vote', methods=['POST'])
def vote():
    auth_header = request.headers.get('Authorization')

    if not auth_header:
        return jsonify({"success": False, "message": "Token is missing"})

    token = auth_header.split(" ")[1]
    username = None

    for user, user_token in tokens.items():
        if user_token == token:
            username = user
            break

    if username is None:
        return jsonify({"success": False, "message": "Token is invalid"})

    if os.path.exists('./storage/users/' + username + '.json'):
        with open('./storage/users/' + username + '.json', 'r') as f:
            data = json.load(f)
            if data["voted"] == True:
                return jsonify({"success": False})
            else:
                data["voted"] = True
                data["votes"] = request.json["votes"]
                with open('./storage/users/' + username + '.json', 'w') as f:
                    json.dump(data, f)
                return jsonify({"success": True})
    else:
        return jsonify({"success": False})


if __name__ == "__main__":
    app.run(debug=True, port=5000)