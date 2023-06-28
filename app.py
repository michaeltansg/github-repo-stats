import os
from dotenv import load_dotenv
import pandas as pd
from github_stats import GithubStats
import matplotlib.pyplot as plt

load_dotenv()

def main():
    # Replace this with your personal access token
    TOKEN = os.getenv("REPO_STATS")
    repositories = [("microsoft", "vscode")]

    stats = GithubStats(TOKEN)

    data = []
    for owner, repo in repositories:
        repo_stats = stats.get_repo_stats(owner, repo)
        data.append(repo_stats)
        # print(repo_stats)

    df = pd.DataFrame(data)
    
    # Create a bar plot
    plt.figure(figsize=(10, 6))  # Change figure size as per your preference
    plt.barh(df['Project Name'], df['Average Commits per Month'], color='skyblue')

    # Adding and formatting title
    plt.title("Average Commits per Month for Each Project")

    # Adding labels
    plt.xlabel('Average Commits per Month')
    plt.ylabel('Project Name')

    # Displaying the plot
    plt.show()

if __name__ == '__main__':
    main()

