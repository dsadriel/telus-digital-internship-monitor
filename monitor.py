from job_service import fetch_new_jobs
from email_service import send_new_job_alert

if __name__ == "__main__":
    new_jobs = fetch_new_jobs()

    if not new_jobs:
        print("No new internships found.")
    else:
        for job in new_jobs:
            send_new_job_alert(job)
            print(f"Alert sent for: {job['title']}")
