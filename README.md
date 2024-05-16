# Public GitHub Repository Invite Link

GitHub currently lacks the feature to create a public link that allows others to collaborate on a repository. The only way to add collaborators to a GitHub repository is to do this manually. This repository solves this problem by generating a link from your repository through which others can be added as collaborators.

## How Does It Work

This project leverages GitHub's OAuth and API to automate the process of adding collaborators to a repository. When a user clicks on the generated invite link, they are redirected to GitHub to authorize the application. Once authorized, the user is automatically added as a collaborator to the specified repository.

### Workflow

1. **Generate Invite Link**: An invite link is generated for the repository.
2. **User Clicks Link**: The user clicks on the invite link and is redirected to GitHub for authorization.
3. **OAuth Authorization**: The user authorizes the application to access their GitHub account.
4. **Add Collaborator**: The application uses the GitHub API to add the user as a collaborator to the repository.

## How to Set It Up

### Prerequisites

- GitHub account
- Supabase account (for storing invite links)
- Vercel account (for deployment)

### Installation

1. **Clone the Repository**

```bash
git clone https://github.com/yourusername/public_github_repository_invite_link.git
```

2. **Set Up Environment Variables**

Create a `.env` file in the root directory and add the following environment variables:

```env
CLIENT_ID=your_github_client_id
CLIENT_SECRET=your_github_client_secret
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
GITHUB_TOKEN=your_github_token
```

3. **Set Up Supabase**

- Go to the [Supabase website](https://supabase.io/) and create an account.
- Create a new project in Supabase.
- Navigate to the "Table Editor" and create a new table named `links` with the following columns (for an easier but less secure setup, disable Row Level Security (RLS)):
    - `id` (UUID, primary key)
    - `link` (text)
    - `owner` (text)

### Deployment

1. **Deploy to Vercel**

- Connect your GitHub repository to Vercel.
- Set the environment variables in the Vercel dashboard.
- Deploy the application.
- Take the URL from the Vercel application and set it to the environment variable `VERCEL_URL`.

### Usage

1. **Generate an Invite Link**

Run the `database.py` script with your repository name and your username. For example:

```bash
python database.py public_github_repository_invite_link yachty66
```

This will return a link which can be used to invite collaborators.

2. **Share the Link**

Share the generated link with potential collaborators.

3. **Collaborators Click the Link**

When collaborators click the link, they will be redirected to GitHub to authorize the application and will be automatically added to the repository.