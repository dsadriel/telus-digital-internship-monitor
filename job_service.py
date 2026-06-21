import requests
import json
import os

STORAGE_FILE = "known_jobs.json"
API_URL = "https://api.ashbyhq.com/posting-api/job-board/telus-digital?includeCompensation=true"


def _fetch_internships() -> list:
    """Shared helper: fetch and filter all intern-type jobs from the API."""
    response = requests.get(API_URL, timeout=10)
    response.raise_for_status()
    jobs = response.json().get("jobs", [])
    return [j for j in jobs if j.get("employmentType") == "Intern"]


def load_known_jobs() -> list:
    if os.path.exists(STORAGE_FILE):
        with open(STORAGE_FILE, "r") as f:
            return json.load(f)
    return []


def save_known_jobs(ids: list):
    with open(STORAGE_FILE, "w") as f:
        json.dump(ids, f, indent=4)


def fetch_all_internships() -> list:
    """Return every currently open internship, regardless of known status."""
    try:
        return _fetch_internships()
    except Exception as e:
        print(f"Error fetching jobs: {e}")
        return []


def fetch_new_jobs() -> list:
    """Return only internships that have not been seen before, and persist the updated list."""
    try:
        all_jobs = _fetch_internships()
        known_jobs = load_known_jobs()
        new_jobs = [j for j in all_jobs if j["id"] not in known_jobs]

        if new_jobs:
            save_known_jobs([j["id"] for j in all_jobs])

        return new_jobs
    except Exception as e:
        print(f"Error fetching jobs: {e}")
        return []