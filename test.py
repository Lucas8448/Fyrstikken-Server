import requests
import random
import json
import os

base_url = 'http://localhost:5000'

def get_user_credentials():
    user_credentials = []
    users_directory = './storage/users/'

    for user_file in os.listdir(users_directory):
        if user_file.endswith('.json'):
            with open(os.path.join(users_directory, user_file), 'r') as f:
                data = json.load(f)
                user_credentials.append({
                    "username": data["username"],
                    "password": data["password"]
                })

    return user_credentials

def simulate_user_voting(username, password):
    # Login
    login_response = requests.post(base_url + '/login', json={"username": username, "password": password})
    if not login_response.json()["success"]:
        print(f"Login failed for user {username}")
        return
    
    token = login_response.json()["token"]

    votes = {str(i): random.randint(1, 3) for i in range(1, 15)}

    headers = {'Authorization': f'Bearer {token}'}
    vote_response = requests.post(base_url + '/vote', headers=headers, json={"votes": votes})
    if vote_response.json()["success"]:
        print(f"User {username} successfully voted")
    else:
        print(f"Voting failed for user {username}")

user_credentials = get_user_credentials()

for user in user_credentials:
    simulate_user_voting(user["username"], user["password"])
