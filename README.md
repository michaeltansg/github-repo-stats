## GitHub Repo Stats

This project fetches statistics from a list of repositories to create benchmark baselines.

### Prerequisites
1. **Generate GitHub Token**: Create a [Personal Access Token](https://github.com/settings/tokens) on GitHub and add it to the `.env` file.
2. **Set Up Repository List**: Copy `repositories.example.csv` to `repositories.csv` and list repositories as `user/repo` on separate lines.
3. **Python Environment**: Create and activate a Python environment, then update pip:
   ```sh
   python -m venv venv
   . venv/bin/activate
   pip install -U pip
   ```

### Installation
1. **Install Dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

### Usage
1. **Run the Application**:
   ```sh
   python app.py
   ```

### Configuration
- **Environment Variables**: Add your GitHub token to `.env`.
- **Cache Expiry**: Set `REPORT_EXPIRY_IN_SECONDS` to control data retrieval frequency.

### Files
- **`app.py`**: Main application file.
- **`data_visualizer.py`**: Handles data visualization.
- **`github_stats.py`**: Fetches GitHub statistics.

### License
This project is licensed under the MIT License.

For more information, visit the [repository](https://github.com/michaeltansg/github-repo-stats).