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