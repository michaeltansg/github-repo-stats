import os
import time
import pandas as pd
from pandas import DataFrame
from dotenv import load_dotenv

from github_stats import GithubStats
from data_visualizer import DataVisualizer

load_dotenv()

TOKEN = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
REPORT_EXPIRY_IN_SECONDS = os.getenv("REPORT_EXPIRY_IN_SECONDS")

def fetch_data() -> list:
    """ Fetch data from GitHub """
    # Read the CSV file into a DataFrame
    df = pd.read_csv("path_to_your_csv_file/repositories.csv")

    # Convert the DataFrame to a list
    repositories = df["Repositories"].tolist()

    stats = GithubStats(TOKEN)

    data = []

    for owner, repo in (item.split('/') for item in repositories):
    # for owner, repo in repositories:
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
        if file_age < float(REPORT_EXPIRY_IN_SECONDS):
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
