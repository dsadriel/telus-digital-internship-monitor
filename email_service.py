import smtplib
import os
from datetime import datetime
from email.message import EmailMessage
from typing import Optional, Tuple

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465


def _get_credentials() -> Tuple[Optional[str], Optional[str]]:
    return os.environ.get("EMAIL_USER"), os.environ.get("EMAIL_PASS")


def _send(msg: EmailMessage):
    user, password = _get_credentials()
    if not user or not password:
        print("[email_service] No credentials found — printing email to terminal.")
        print(f"Subject : {msg['Subject']}")
        print(f"From    : {msg['From'] or '(not set)'}")
        print(f"To      : {msg['To'] or '(not set)'}")
        print("-" * 60)
        body = msg.get_body(preferencelist=("html", "plain"))
        print(body.get_content() if body else "(no body)")
        return
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as smtp:
        smtp.login(user, password)
        smtp.send_message(msg)


def _job_to_html(job: dict) -> str:
    """Render a single job as a simple HTML block."""
    locations = job.get("location") or "Remote / Not specified"
    return (
        f"<p>"
        f"<strong><a href=\"{job['jobUrl']}\">{job['title']}</a></strong><br>"
        f"📍 {locations}"
        f"</p>"
    )


# ---------------------------------------------------------------------------
# Alert: single new job notification
# ---------------------------------------------------------------------------

def send_new_job_alert(job: dict):
    """Send an email alert for a single newly posted internship."""
    user, _ = _get_credentials()

    html = f"""\
<html><body>
<h2>New TELUS Digital Internship</h2>
{_job_to_html(job)}
</body></html>"""

    msg = EmailMessage()
    msg["Subject"] = f"[TELUS] New Internship: {job['title']}"
    msg["From"] = user
    msg["To"] = user
    msg.set_content(f"New internship: {job['title']}\n{job['jobUrl']}")
    msg.add_alternative(html, subtype="html")

    _send(msg)


# ---------------------------------------------------------------------------
# Digest: weekly summary of all open internships
# ---------------------------------------------------------------------------

def send_weekly_digest(jobs: list):
    """Send a weekly digest email listing all currently open internships."""
    user, _ = _get_credentials()
    today = datetime.utcnow().strftime("%B %d, %Y")
    count = len(jobs)

    if jobs:
        jobs_html = "\n".join(_job_to_html(j) for j in jobs)
        body = f"<p>Found <strong>{count} open internship(s)</strong> this week:</p>\n{jobs_html}"
    else:
        body = "<p>No internship positions are currently open. Check back next week!</p>"

    html = f"""\
<html><body>
<h2>TELUS Digital – Weekly Internship Digest</h2>
<p><em>{today}</em></p>
<hr>
{body}
<hr>
<p><a href="https://jobs.ashbyhq.com/telus-digital">View full job board</a></p>
</body></html>"""

    msg = EmailMessage()
    msg["Subject"] = f"[TELUS] Weekly Internship Digest – {count} open position(s) · {today}"
    msg["From"] = user
    msg["To"] = user
    msg.set_content("\n".join(
        f"- {j['title']} | {j['jobUrl']}" for j in jobs
    ) or "No open internships this week.")
    msg.add_alternative(html, subtype="html")

    _send(msg)
