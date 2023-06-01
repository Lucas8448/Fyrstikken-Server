from flask import *
import os
import json

app = Flask(__name__)

@app.route('/')
def home():
  return 'Hello World!'

@app.route('/users')
def users():
  users = os.listdir('./storage/users')
  users = [user.replace('.json', '') for user in users]
  return json.dumps(users)

@app.route('/users/<username>')
def user(username):
  with open('./storage/users/' + username + '.json') as f:
    return f.read()

@app.route('/submitvotes/<votes>')
def setvote(votes):
  password = request["password"]
  username = request["username"]
  with open('./storage/users/' + username + '.json') as f:
    user = json.load(f)
    if password == user["password"]:
      if user["voted"] == False:
        user["votes"] = votes
        user["voted"] = True
        with open('./storage/users/' + username + '.json', 'w') as f:
          json.dump(user, f)
        return json.dumps(user)
      else:
        # return error:true and why as json
        return json.dumps({"error":True, "message":"Already voted"})
    else:
      return json.dumps({"error":True, "message":"Incorrect password"})
  

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0')