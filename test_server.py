import requests
import dotenv
import os
dotenv.load_dotenv()

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

from flask import Flask, request, redirect
import requests
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

REDIRECT_URI = 'http://127.0.0.1:5000/callback'

@app.route('/')
def home():
    return '<a href="/login">Login with GitHub</a>'

@app.route('/login')
def login():
    print(f'https://github.com/login/oauth/authorize?client_id=Ov23li8ErI6ZDY8QRAjk&redirect_uri=http://localhost:5000/callback&scope=user')
    return redirect(f'https://github.com/login/oauth/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope=user')

@app.route('/callback')
def callback():
    code = request.args.get('code')
    print("code", code)
    access_token = get_access_token(code)
    username = get_github_username(access_token)
    log_username(username)
    return f'Logged in as: {username}'

def get_access_token(code):
    print("get access token")
    payload = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': code,
        'redirect_uri': REDIRECT_URI
    }
    headers = {'Accept': 'application/json'}
    response = requests.post('https://github.com/login/oauth/access_token', json=payload, headers=headers)
    response_json = response.json()
    return response_json.get('access_token')

def get_github_username(access_token):
    headers = {'Authorization': f'token {access_token}'}
    response = requests.get('https://api.github.com/user', headers=headers)
    return response.json().get('login')

def log_username(username):
    # Logging the username to a file
    # with open('github_usernames.log', 'a') as file:
    #     file.write(username + '\n')
    print(f"Username {username} logged.")

if __name__ == '__main__':
    app.run(debug=True)
