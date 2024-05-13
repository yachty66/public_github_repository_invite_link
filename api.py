from fastapi import FastAPI, Request, HTTPException, Depends
import secrets
from fastapi.responses import RedirectResponse
import httpx
import os
from starlette.status import HTTP_302_FOUND
import dotenv
from supabase import create_client, Client

dotenv.load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = "http://127.0.0.1:8080/callback"
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
app = FastAPI()

### Entry in application ###
@app.get("/")
async def home():
    return RedirectResponse(url="/login")

### Login ###
@app.get("/login")
async def login():
    auth_url = f"https://github.com/login/oauth/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope=user"
    return RedirectResponse(url=auth_url, status_code=HTTP_302_FOUND)

### Callback after github auth ###
@app.get("/callback")
async def callback(code, repository_name, repository_owner):
    access_token = await get_access_token(code)
    username = await get_github_username(access_token)
    log_username(username)
    repo_owner = repository_owner
    repo_name = repository_name
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
    #right now i am manually setting all the variables and url where the server runs is only on my local device - how can i make this public and so that its possible to have the input data dynamic??
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
    
def add_url_to_application(github_repo_name):
    """
    creates url and adds url to database after script is getting called with the repository name

    https://docs.google.com/spreadsheets/d/14Dx8stFbGXtFVTDi7KiLzJCLkbMzA_tDXNw_VBm6zyc/edit?usp=sharing
    """
    #i guess what i need to do is to generate an url and than add this url to the database
    #once the uuiid is added i want to 
    unique_id = secrets.token_urlsafe(44)
    #www.mydomain/unique_id/github_repo_name
    #above is stored in the database and if user is putting this url in search than he will be redirected to auth for the name of the repository but only if url is in database

def check_if_url_exists_in_database():
    """
    if someone is trying to call the api with an url which is not in the database the user is getting blocked    
    """
    pass

def add_link(link_url):
    #okay now i can add links to the db, every link in the database will add people to the repo
    response = supabase.table('links').insert({"link": link_url}).execute()
    print("response",response)

@app.post("/generate/{repo_name}")
async def generate_repo_link(repo_name: str):
    unique_id = secrets.token_urlsafe(16)
    full_path = f"www.mydomain.com/{unique_id}/{repo_name}"
    response = add_link(full_path)
    if response.get('status_code', 400) == 201:
        return {"url": full_path}
    else:
        raise HTTPException(status_code=400, detail="Failed to add link to database")

@app.get("/{unique_id}/{repo_name}")
async def access_repo(unique_id: str, repo_name: str):
    full_path = f"www.mydomain.com/{unique_id}/{repo_name}"
    response = get_link(full_path)
    if response.get('data') and len(response['data']) > 0:
        # Perform the desired action, e.g., redirect to GitHub OAuth or show repository details
        return {"message": f"Access granted to repository: {repo_name}"}
    else:
        raise HTTPException(status_code=404, detail="Repository not found or access denied")