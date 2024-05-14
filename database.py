import secrets
import os
import dotenv
from supabase import create_client, Client
import sys 

dotenv.load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def main():
    """
    Main function to generate a unique repository link and add it to the database with the owner's name.
    
    Usage:
        python database.py <repository_name> <repository_owner>
    
    Args:
        repository_name (str): The name of the repository for which to generate the link.
        repository_owner (str): The GitHub username of the repository owner.
    
    Returns:
        str: The generated URL if the database operation is successful; otherwise, it returns an error message.
    """
    repo_name = sys.argv[1]
    repo_owner = sys.argv[2]
    url = generate_repo_link(repo_name)
    add_url_and_owner_name_to_database(url, repo_owner)
    return url
    
def generate_repo_link(repo_name):
    unique_id = secrets.token_urlsafe(44)
    #todo add the whole correct link here
    full_path = f"{unique_id}/{repo_name}"
    return full_path

def add_url_and_owner_name_to_database(url, repo_owner):
    try:
        response = supabase.table('links').insert({
            "link": url,
            "owner": repo_owner
        }).execute()
        if response.status_code == 201:
            return {"status": "success", "data": response.data}
        else:
            return {"status": "error", "message": "Failed to insert data into the database"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    link=main()
    print(link)