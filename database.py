"""
this file is adding the link to the database 
"""
from supabase import create_client, Client

# Supabase URL and Key (do not expose these in production environments)
url = 'https://hrdeupsgkornnuyhawtd.supabase.co'  # e.g., 'https://xyzcompany.supabase.co'
key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhyZGV1cHNna29ybm51eWhhd3RkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTU1NDM5MTQsImV4cCI6MjAzMTExOTkxNH0.FpkvS21XQkBsAgGd8TcbWPRDJvQylOYuo7voKhzJpwQ'  # your anon or service key

# Create a Supabase client
supabase: Client = create_client(url, key)

def add_link(link_url):
    #okay now i can add links to the db, every link in the database will add people to the repo
    response = supabase.table('links').insert({"link": link_url}).execute()
    print("response",response)
    #response = supabase.table('links').insert(data).execute()
    #if response.status_code == 201:
    #    print("Link added successfully!")
    #else:
    #    print("Failed to add link:", response.status_code, response.text)

# Example of adding a link
add_link('https://example.com')

