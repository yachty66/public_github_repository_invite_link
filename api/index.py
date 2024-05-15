from sanic import Sanic
from sanic.response import json

app = Sanic()


@app.route("/<path:path>")
async def index(request, path=""):
    return json({"hello": path})

# @app.route("/other_route")
# async def other_route(request, path="other_route"):
#     return json({"whatever": path})

# from sanic import Sanic, response
# from sanic.exceptions import SanicException
# from urllib.parse import urlparse, quote_plus
# from typing import Optional, Tuple
# from supabase import create_client, Client
# from sanic import Sanic
# from sanic.response import json
# import os
# import dotenv
# import httpx

# dotenv.load_dotenv()

# app = Sanic()

# SUPABASE_URL = os.getenv("SUPABASE_URL")
# SUPABASE_KEY = os.getenv("SUPABASE_KEY")
# GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# @app.route("/callback")
# async def handle_callback(request):
#     code = request.args.get("code")
#     link = request.args.get("link")
#     owner = request.args.get("owner")
#     if not code:
#         raise SanicException("Missing code in the query parameters", status_code=400)
#     access_token = await get_access_token(code)
#     username = await get_github_username(access_token)
#     if link is None or owner is None:
#         raise SanicException(
#             "Missing link or owner in the query parameters", status_code=400
#         )
#     await add_user_to_repo(username, owner, link)
#     return response.json(
#         {"message": f"You were added to the repository {link} from {owner}."}
#     )


# @app.route("/<path:path>")
# async def handle_dynamic_route(request, path):
#     print("path", path)
#     print("request", request)
#     is_valid, link, owner = check_path_in_database(path)
#     print("is_valid", is_valid)
#     print("link", link)
#     print("owner", owner)
#     link = extract_repo_name_from_link(link)
#     if not is_valid:
#         raise SanicException("Route not found", status_code=404)
#     return response.redirect(get_auth_url(link, owner))


# #this should be the simple route which should be callable in my app
# #i need to get this route working cause if this 
# #problem right now is that this route is not callable somehow - how can i fix that?
# #something wents wrong but i cannot really see in the logs what exactly wents wrong. how can i fix that? 
# #how can i make this working? 
# @app.route("/hello")
# async def hello(request):
#     return response.text("hello")


# def check_path_in_database(
#     request_path: str,
# ) -> Tuple[bool, Optional[str], Optional[str]]:
#     print("request path", request_path)
#     response = supabase.table("links").select("link", "owner").execute()
#     for link in response.data:
#         if link["link"] == request_path:
#             return True, link["link"], link["owner"]
#     return False, None, None


# def get_auth_url(link: str, owner: str):
#     client_id = os.getenv("CLIENT_ID")
#     encoded_link = quote_plus(link)
#     encoded_owner = quote_plus(owner)
#     redirect_uri = (
#         f"http://127.0.0.1:8080/callback?link={encoded_link}%26owner={encoded_owner}"
#     )
#     return f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=user"


# def extract_repo_name_from_link(link: str) -> str:
#     parts = link.split("/")
#     return parts[-1] if parts else None


# async def get_access_token(code: str):
#     client_id = os.getenv("CLIENT_ID")
#     client_secret = os.getenv("CLIENT_SECRET")
#     data = {
#         "client_id": client_id,
#         "client_secret": client_secret,
#         "code": code,
#         "redirect_uri": "http://127.0.0.1:8080/callback",
#     }
#     headers = {"Accept": "application/json"}
#     async with httpx.AsyncClient() as client:
#         response = await client.post(
#             "https://github.com/login/oauth/access_token", data=data, headers=headers
#         )
#     return response.json().get("access_token")


# async def get_github_username(access_token: str):
#     headers = {"Authorization": f"token {access_token}"}
#     async with httpx.AsyncClient() as client:
#         response = await client.get("https://api.github.com/user", headers=headers)
#     return response.json().get("login")


# async def add_user_to_repo(username: str, owner: str, repo_name: str):
#     url = f"https://api.github.com/repos/{owner}/{repo_name}/collaborators/{username}"
#     headers = {
#         "Authorization": f"token {GITHUB_TOKEN}",
#         "Accept": "application/vnd.github.v3+json",
#     }
#     async with httpx.AsyncClient() as client:
#         response = await client.put(url, headers=headers)
#         print("response from adding a user:", response)
#         if response.status_code == 201:
#             return "User invited successfully"
#         else:
#             return f"Failed to invite user: {response.json()}"


# if __name__ == "__main__":
#     # http://127.0.0.1:8080/dajqj9lsc9kfUAZS9cKs83bdKAoPv5_Ldg3xWPJlhoem10sAkdfiYgKqFE8/test_test
#     app.run(host="0.0.0.0", port=8080)
