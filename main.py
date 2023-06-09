from flask_cors import CORS
from flask import *
import os
import json

app = Flask(__name__)
CORS(app)

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
                return jsonify({"success": True})
            else:
                return jsonify({"success": False})
    else:
        return jsonify({"success": False})

@app.route('/vote')
def vote():
  username = request["username"]
  password = request["password"]
  if os.path.exists('./storage/users/' + username + '.json'):
    with open('./storage/users/' + username + '.json', 'r') as f:
      data = json.load(f)
      if data["password"] == password:
        if data["voted"] == True:
          return {"success":False}
        else:
          data["voted"] = True
          data["votes"] = request["votes"]
          with open('./storage/users/' + username + '.json', 'w') as f:
            json.dump(data, f)
          return {"success":True}
      else:
        return {"success":False}
  else:
    return {"success":False}


if __name__ == "__main__":
    app.run(debug=True, port=5000)
