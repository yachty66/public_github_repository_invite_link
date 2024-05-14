"""
this is where i stopped at (need to prompt later):

next i need to create the fast api app. each row in my database contains the url as route:

http://localhost:8080/5ScT1NN5kH5cy3j1hukOhBZgW1IC7x5WaKNutOMG4o6_lw77V-G9pnjRe1Y/test
"""
from fastapi import FastAPI, HTTPException
from urllib.parse import urlparse
from typing import Optional
from supabase import create_client, Client
from fastapi.responses import RedirectResponse
import os 
import dotenv
import httpx

dotenv.load_dotenv()

app = FastAPI()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.get("/callback")
async def handle_callback(code: str):
    try:
        print("Received code in callback:", code)
        access_token = await get_access_token(code)
        username = await get_github_username(access_token)
        print("GitHub username received:", username)
        # Logic to add the user to the repository goes here
        return {"message": f"Logged in as: {username}"}
    except Exception as e:
        print("Error in callback:", str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/{path:path}")
async def handle_dynamic_route(path: str):
    """
    checks if a certain path exists in the database
    http://127.0.0.1:8000/somepath
    http://127.0.0.1:8080/-1oc_zg3yn4WunKm04z0BAcwx1zxiwJW9fFEpXiYHIFwMn1Idb7r8sJOYdE/yolo

    """
    is_valid = check_path_in_database(path)
    if not is_valid:
        raise HTTPException(status_code=404, detail="Route not found")
    #if it works i want to add user to repo
    #add_user_to_repo(path)
    return RedirectResponse(url=get_auth_url())

def check_path_in_database(request_path: str) -> (bool, Optional[str]):
    print("request path", request_path)
    response = supabase.table('links').select("link", "owner").execute()
    #iterate over links of response data and check if link is inside request_path
    for link in response.data:
        if link['link'] == request_path:
            return True
    return False

def get_auth_url():
    client_id = os.getenv("CLIENT_ID")
    redirect_uri = "http://127.0.0.1:8080/callback"  # Adjust this to your actual callback URL
    return f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=user"

async def get_access_token(code: str):
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "redirect_uri": "http://127.0.0.1:8080/callback"
    }
    headers = {"Accept": "application/json"}
    async with httpx.AsyncClient() as client:
        response = await client.post("https://github.com/login/oauth/access_token", data=data, headers=headers)
    return response.json().get("access_token")

async def get_github_username(access_token: str):
    headers = {"Authorization": f"token {access_token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.github.com/user", headers=headers)
    return response.json().get("login")

def add_user_to_repo():
    #get username from path
    username = get_username()
    #add user to repo
    add_user_to_repo(username)

def get_username():
    auth_url = f"https://github.com/login/oauth/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope=user"
    pass