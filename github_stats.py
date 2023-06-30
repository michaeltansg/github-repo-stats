import requests
from tenacity import retry, stop_after_attempt, wait_fixed
import numpy as np
from scipy.stats import zscore

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
        stars = repo_data["stargazers_count"]

        # Send a GET request to get the contributor data
        # https://docs.github.com/en/rest/repos/repos?apiVersion=2022-11-28#list-repository-contributors
        # https://stackoverflow.com/a/36462386 <---- explains how to get anonymous contributors
        # https://api.github.com/repos/{owner}/{repo}/contributors?anon=1
        # For now, we are not interested in anonymous contributors. We will only consider authenticated contributors on GitHub only.
        contrib_list = self.fetch_contributors(f"https://api.github.com/repos/{owner}/{repo}/contributors", headers=self.headers)
        # Calculate the number of contributors
        num_contributors = len(contrib_list)
        # print(num_contributors)
        # [print(f"=== {contrib['contributions']} ===") for contrib in contrib_list]
        # self.threshold_percentiles(contrib_list)
        # self.threshold_standard_deviation(contrib_list)
        # self.threshold_z_score(contrib_list)
        # self.threshold_interquartile_range(contrib_list)
        # self.threshold_pareto_principle(contrib_list)
        significant_contributors = self.threshold_interquartile_range(contrib_list)

        # Send a GET request to get the commit data
        # https://docs.github.com/en/rest/metrics/statistics?apiVersion=2022-11-28
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
            "Average Commits per Month": avg_commits_per_month,
            "Stars": stars,
            "Contribution data": contrib_list,
            "Significant Contributors": significant_contributors
        }
    
    def fetch_contributors(self, base_url, headers):
        page = 1
        contributors = []
        while True:
            # define the parameters
            params = {
                "per_page": 100,
                "page": page
            }

            # make the request
            try:
                data = self.paginated_fetch(base_url, headers, params)
            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}")
                break

            # handle the response
            if data:  # if data is not an empty list
                contributors.extend(data) # add the data to the list
                page += 1  # increment the page counter
            else:
                break  # if data is an empty list, we've reached the end and exit the loop

        print(f"Found {len(contributors)} contributors")
        return contributors

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def paginated_fetch(self, url, headers, params):
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            response.raise_for_status()
        return response.json()

    def threshold_percentiles(self, data):
        # extract the list of contributions
        contributions = [d['contributions'] for d in data]

        # calculate the 90th percentile
        threshold = np.percentile(contributions, 90)
        print(f"Threshold (90th percentile): {threshold}")

        # find significant contributors
        significant_contributors = [d for d in data if d['contributions'] >= threshold]
        print(f"Found {len(significant_contributors)} significant contributors")
        return significant_contributors

    def threshold_standard_deviation(self, data):
        # extract the list of contributions
        contributions = [d['contributions'] for d in data]

        mean_contributions = np.mean(contributions)
        std_contributions = np.std(contributions)

        # set threshold as mean plus 2 standard deviations
        threshold = mean_contributions + 2 * std_contributions
        print(f"Threshold (Standard Deviation): {threshold}")

        # find significant contributors
        significant_contributors = [d for d in data if d['contributions'] >= threshold]
        print(f"Found {len(significant_contributors)} significant contributors")
        return significant_contributors

    def threshold_z_score(self, data):
        # extract the list of contributions
        contributions = [d['contributions'] for d in data]

        # calculate z-scores
        z_scores = zscore(contributions)

        # set threshold as z-score of 2
        threshold = 2
        print(f"Threshold (Z-Score): {threshold}")

        # find significant contributors
        significant_contributors = [d for d, z in zip(data, z_scores) if z >= threshold]
        print(f"Found {len(significant_contributors)} significant contributors")
        return significant_contributors

    def threshold_interquartile_range(self, data):
        # extract the list of contributions
        contributions = [d['contributions'] for d in data]

        Q1 = np.percentile(contributions, 25)
        Q3 = np.percentile(contributions, 75)
        IQR = Q3 - Q1

        # set threshold as Q3 plus 1.5 IQR
        threshold = Q3 + 1.5 * IQR
        # print(f"Threshold (Interquartile Range): {threshold}")

        # find significant contributors
        significant_contributors = [d for d in data if d['contributions'] >= threshold]
        # print(f"Found {len(significant_contributors)} significant contributors")
        return significant_contributors

    def threshold_pareto_principle(self, data):
        # extract the list of contributions
        contributions = [d['contributions'] for d in data]

        # set threshold as 80/20
        threshold = np.percentile(contributions, 80)
        print(f"Threshold (80/20): {threshold}")

        # find significant contributors
        significant_contributors = [d for d in data if d['contributions'] >= threshold]
        print(f"Found {len(significant_contributors)} significant contributors")
        return significant_contributors
