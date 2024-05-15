# public_github_repository_invite_link

scenario: i have the repo https://github.com/yachty66/test_repo and want to add the github user Asynchron44 to the repo via an invite link

approach:

- run python script with link to repo as argument and python script returns a invite link which redirects to auth page which when extracts the users email and than is adding the user to the github repository 

- all invite links are saved in supabase 

- if an invite link is clicked and user did auth a function is executed which uses github endpoint for adding a the person as an collaborator 

---

i cannot make the link public cause nobody is putting his token in a public webform. this fucks me up so hard than i am not able to wrap my head around this. 

what do i want? 

how does this part look like where i am trying to get the username of the user from github. 

would be much more simple if the user is just adding his username instead of doing the auth thing. i dont know man. 

if i am not getting it working i will just do a simple input form where people can input their data in the form. 

## app workflow

1. py script is called with name of github repo as argument
2. script generates url in format www.mydomain/uuid/repo_name
3. script adds url together with respective github auth url to database
4. now this url can be called as subdomain and is than getting the username of the user via auth and adds them to the repo
5. user is redirected to callback page 

## steps

- [x] add to the callback page a log string which does make sense
- [x] make the database file return and actual url
- [x] make sure that only the urls work which are also inside the database
    - http://127.0.0.1:8080/5MrpgmEcgqtawmONK7xGIklDMAMXEtqw_PKieghuoU4JorrEX7gYKd-BGss/public_github_repository_invite_link
- [ ] make the whole thing serverless working
    - [ ] make a simple route to "hello" to check if the sanic framework is working
    - [ ] make a route to a link from the database to make sure its working (https://public-github-repository-invite-link-6fc1dttzx.vercel.app/dajqj9lsc9kfUAZS9cKs83bdKAoPv5_Ldg3xWPJlhoem10sAkdfiYgKqFE8/test_test)
    - [ ] change url in database.py to vercel domain
- [ ] instead of throwing internal server error, throw appropriate exception
- [ ] clean the code
- [ ] post on twitter 


https://dev.to/abdadeel/deploying-fastapi-app-on-vercel-serverless-18b1