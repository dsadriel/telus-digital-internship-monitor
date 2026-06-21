from job_service import fetch_all_internships
from email_service import send_weekly_digest

if __name__ == "__main__":
    print("Fetching all open internships...")
    jobs = fetch_all_internships()
    print(f"Found {len(jobs)} internship(s). Sending digest email...")
    send_weekly_digest(jobs)
    print("✅ Weekly digest sent successfully!")
