"""
run_once.py
Lightweight entry point for GitHub Actions.
Runs the job() function exactly ONCE and exits — no infinite scheduler loop.
"""

from dotenv import load_dotenv

# Load .env locally (on GitHub Actions, secrets are injected as env vars)
load_dotenv()

from main import job

if __name__ == "__main__":
    job()
