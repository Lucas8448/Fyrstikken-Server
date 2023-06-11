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

@app.route('/total_votes', methods=['GET'])
def total_votes():
    # Initialize vote counts for categories 1-14 and contestants 1-3
    vote_counts = {str(i): {str(j): 0 for j in range(1, 4)}
                   for i in range(1, 15)}
    # Initialize leaders for each category
    leaders = {str(i): "None" for i in range(1, 15)}
    for user_file in os.listdir('./storage/users/'):
        if user_file.endswith('.json'):
            with open(os.path.join('./storage/users/', user_file), 'r') as f:
                data = json.load(f)
                # Check if the user has voted
                if data.get("voted") == True:
                    # Sum the votes in each category
                    for category, contestant in data["votes"].items():
                        if contestant != 0:
                            vote_counts[category][str(contestant)] += 1
    for category, contestants in vote_counts.items():
        max_votes = max(contestants.values())
        for contestant, votes in contestants.items():
            if votes == max_votes:
                leaders[category] = contestant
                break
    html_content = """
    <table border="1">
        <tr>
            <th>Category</th>
            <th>Contestant 1</th>
            <th>Contestant 2</th>
            <th>Contestant 3</th>
            <th>Leader</th>
        </tr>
    """
    for category, contestants in vote_counts.items():
        html_content += f"""
        <tr>
            <td>{category}</td>
            <td>{contestants['1']}</td>
            <td>{contestants['2']}</td>
            <td>{contestants['3']}</td>
            <td>Contestant {leaders[category]}</td>
        </tr>
        """
    html_content += "</table>"
    response = make_response(html_content)
    response.headers["Content-Type"] = "text/html"

    return response

if __name__ == "__main__":
    app.run(debug=True, port=5000)