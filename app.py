import os
import time
import pandas as pd
from pandas import DataFrame
from dotenv import load_dotenv

from github_stats import GithubStats
from data_visualizer import DataVisualizer

load_dotenv()

TOKEN = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")

def fetch_data() -> list:
    """ Fetch data from GitHub """
    repositories = [
        ("Microsoft", "vscode"),
        ("kubernetes", "kubernetes"),
        ("ansible", "ansible"),
        ("hashicorp", "terraform"),
        ("apache", "spark"),
        ("moby", "moby"),
        ("pandas-dev", "pandas"),
        ("facebook", "react"),
        ("flutter", "flutter"),
        ("npm", "cli"),
        ("StanGirard", "quivr"),
        ("hwchase17", "langchain"),
    ]

    stats = GithubStats(TOKEN)

    data = []
    for owner, repo in repositories:
        repo_stats = stats.get_repo_stats(owner, repo)
        data.append(repo_stats)
        # print(repo_stats)

    return data

def load_or_fetch_data(filename) -> DataFrame:
    """
    Load the data from an existing CSV file or 
    fetch new data if the file doesn't exist or is too old. 
    """
    if os.path.exists(filename):
        file_age = time.time() - os.path.getmtime(filename)
        if file_age < 86400: # 86400 seconds = 24 hours
            # Load dataframe from CSV file
            return pd.read_csv(filename)

        os.remove(filename)

    data = fetch_data()
    data_frame = pd.DataFrame(data)
    data_frame.to_csv(filename, index=False)  # Save dataframe to CSV file
    return data_frame

def main():
    """ Main function """
    data_frame = load_or_fetch_data('data.csv')
    data_visualizer = DataVisualizer(data_frame)
    data_visualizer.show_table()
    data_visualizer.plot_data()

if __name__ == '__main__':
    main()
