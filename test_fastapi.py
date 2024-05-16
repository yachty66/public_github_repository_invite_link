from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from urllib.parse import quote_plus
from typing import Optional, Tuple
from supabase import create_client, Client
import os
import dotenv
import httpx

dotenv.load_dotenv()

app = FastAPI()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# http://127.0.0.1:8080/dajqj9lsc9kfUAZS9cKs83bdKAoPv5_Ldg3xWPJlhoem10sAkdfiYgKqFE8/test_test
# https://public-github-repository-invite-link-kahcwhqa9.vercel.app/dajqj9lsc9kfUAZS9cKs83bdKAoPv5_Ldg3xWPJlhoem10sAkdfiYgKqFE8/test_test

#https://public-github-repository-invite-link.vercel.app/dajqj9lsc9kfUAZS9cKs83bdKAoPv5_Ldg3xWPJlhoem10sAkdfiYgKqFE8/test_test
@app.get("/callback")
async def handle_callback(
    request: Request, code: str, link: Optional[str] = None, owner: Optional[str] = None
):
    access_token = await get_access_token(request, code)
    username = await get_github_username(access_token)
    if link is None or owner is None:
        raise HTTPException(
            status_code=400, detail="Missing link or owner in the query parameters"
        )
    await add_user_to_repo(username, owner, link)
    return {"message": f"You were added to the repository {link} from {owner}."}


@app.get("/hello")
async def say_hello():
    return {"message": "Hello, World!"}


@app.get("/{path:path}")
async def handle_dynamic_route(request: Request, path: str):
    is_valid, link, owner = check_path_in_database(path)
    link = extract_repo_name_from_link(link)
    if not is_valid:
        raise HTTPException(status_code=404, detail="Route not found")
    return RedirectResponse(url=get_auth_url(request, link, owner))


def check_path_in_database(
    request_path: str,
) -> Tuple[bool, Optional[str], Optional[str]]:
    print("request path", request_path)
    response = supabase.table("links").select("link", "owner").execute()
    for link in response.data:
        if link["link"] == request_path:
            return True, link["link"], link["owner"]
    return False, None, None


def get_auth_url(request: Request, link: str, owner: str):
    client_id = os.getenv("CLIENT_ID")
    encoded_link = quote_plus(link)
    encoded_owner = quote_plus(owner)
    print("getting request")
    base_url = str(request.base_url).rstrip("/")
    print("base_url", base_url)
    redirect_uri = f"{base_url}/callback?link={encoded_link}&owner={encoded_owner}"
    return f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=user"


def extract_repo_name_from_link(link: str) -> str:
    parts = link.split("/")
    return parts[-1] if parts else None


async def get_access_token(request: Request, code: str):
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    base_url = str(request.base_url).rstrip("/")
    redirect_uri = f"{base_url}/callback"
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "redirect_uri": redirect_uri,
    }
    headers = {"Accept": "application/json"}
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://github.com/login/oauth/access_token", data=data, headers=headers
        )
    return response.json().get("access_token")


async def get_github_username(access_token: str):
    headers = {"Authorization": f"token {access_token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.github.com/user", headers=headers)
    return response.json().get("login")


async def add_user_to_repo(username: str, owner: str, repo_name: str):
    url = f"https://api.github.com/repos/{owner}/{repo_name}/collaborators/{username}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }
    async with httpx.AsyncClient() as client:
        response = await client.put(url, headers=headers)
        print("response from adding a user:", response)
        if response.status_code == 201:
            return "User invited successfully"
        else:
            return f"Failed to invite user: {response.json()}"