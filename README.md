# github-repo-stats
Fetches statistics of some well-known repositories to set as a benchmark baseline.

Generate a [Personal Access Token](https://github.com/settings/tokens) on Github and add that to the the environment variable to `.env`.

Make a copy of `repositories.example.csv` and name it `repositories.csv`. Add repositories in the format of `user/organization`/`repo name` on separate lines.

The application uses `REPORT_EXPIRY_IN_SECONDS` to decide if it should retrieve data or consume previously cached information.

Create and activate a python environment and update the pip version
```bash
python -m venv venv;. venv/bin/activate; pip install -U pip
```

Run the application
```bash
python app.py
```