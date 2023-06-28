import requests

class GithubStats:
    def __init__(self, token):
        self.token = token
        self.headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {self.token}",
            "X-GitHub-Api-Version": "2022-11-28",
        }

    def get_repo_stats(self, owner, repo):
        # Send a GET request to get the repository data
        repo_response = requests.get(f"https://api.github.com/repos/{owner}/{repo}", headers=self.headers)
        repo_data = repo_response.json()

        # Extract the project name and repository URL
        owner_name = repo_data["owner"]["login"]
        owner_type = repo_data["owner"]["type"]
        project_name = repo_data["name"]
        repo_url = repo_data["html_url"]

        # Send a GET request to get the contributor data
        contrib_response = requests.get(f"https://api.github.com/repos/{owner}/{repo}/contributors", headers=self.headers)
        contrib_data = contrib_response.json()

        # Calculate the number of contributors
        num_contributors = len(contrib_data)

        # Send a GET request to get the commit data
        commits_response = requests.get(f"https://api.github.com/repos/{owner}/{repo}/stats/commit_activity", headers=self.headers)
        commits_data = commits_response.json()

        # Calculate the average number of commits per month
        commits_per_week = [week["total"] for week in commits_data]
        avg_commits_per_month = sum(commits_per_week) / 12

        # Return the data
        return {
            "Owner Name": owner_name,
            "Project Name": project_name,
            "Owner Type": owner_type,
            "Repository URL": repo_url,
            "Number of Contributors": num_contributors,
            "Average Commits per Month": avg_commits_per_month
        }