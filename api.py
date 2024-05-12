from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import RedirectResponse
import httpx
import os
from starlette.status import HTTP_302_FOUND
import dotenv

dotenv.load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = "http://127.0.0.1:8080/callback"

app = FastAPI()

@app.get("/")
async def home():
    return RedirectResponse(url="/login")

@app.get("/login")
async def login():
    auth_url = f"https://github.com/login/oauth/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope=user"
    return RedirectResponse(url=auth_url, status_code=HTTP_302_FOUND)

@app.get("/callback")
async def callback(code: str):
    print("callback is called")
    access_token = await get_access_token(code)
    username = await get_github_username(access_token)
    log_username(username)
    # Specify the repository owner and the repository name
    repo_owner = "yachty66"
    repo_name = "test_test"
    # Attempt to add the user as a collaborator
    if await add_collaborator_to_repo(GITHUB_TOKEN, username, repo_owner, repo_name):
        return {"message": f"Logged in as: {username}, added to repo successfully."}
    else:
        return {"message": f"Logged in as: {username}, failed to add to repo."}

async def get_access_token(code: str):
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "redirect_uri": REDIRECT_URI,
    }
    headers = {"Accept": "application/json"}
    async with httpx.AsyncClient() as client:
        response = await client.post("https://github.com/login/oauth/access_token", json=payload, headers=headers)
    response_json = response.json()
    return response_json.get("access_token")

async def get_github_username(access_token: str):
    headers = {"Authorization": f"token {access_token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.github.com/user", headers=headers)
    return response.json().get("login")

def log_username(username: str):
    print(f"Username {username} logged.")

async def add_collaborator_to_repo(access_token: str, username: str, repo_owner: str, repo_name: str):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/collaborators/{username}"
    print("url", url)
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    permissions = {
        "permission": "push"  # Adjust this as needed, e.g., "triage"
    }
    async with httpx.AsyncClient() as client:
        response = await client.put(url, headers=headers, json=permissions)
    if response.status_code == 201:
        print(f"Successfully added {username} as a collaborator to {repo_name}.")
        return True
    else:
        print(f"Failed to add collaborator: {response.status_code} - {response.text}")
        return False