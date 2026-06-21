# TELUS Digital Internship Monitor

An automated tool that watches the [TELUS Digital job board](https://jobs.ashbyhq.com/telus-digital) and emails you whenever a new internship is posted — and sends a weekly digest of every open position.

Powered by **GitHub Actions**, so it runs entirely in the cloud with no server required.

---

## How It Works

| Script | What it does |
|---|---|
| `monitor.py` | Runs **twice daily at 6am and 6pm BRT**. Fetches all open internships, compares against `known_jobs.json`, and emails an alert for each new posting. |
| `weekly_digest.py` | Runs **every Sunday at 10am BRT**. Fetches all currently open internships and emails a full digest. |

Both scripts fall back to printing the email content to the terminal if no credentials are configured — useful for local testing.

---

## Getting Started

### 1. Fork the repo

1. Click **Fork** at the top-right of this repository on GitHub
2. Choose your account as the destination
3. Once forked, clone **your** copy locally:

```bash
git clone https://github.com/<your-username>/telus-job-scan.git
cd telus-job-scan
```

### 2. Install dependencies

The only dependency is `requests`:

```bash
pip install requests
```

### 3. Add your credentials

The scripts send email via **Gmail SMTP**. You need to provide two values:

| Variable | Description |
|---|---|
| `EMAIL_USER` | Your Gmail address (e.g. `you@gmail.com`) |
| `EMAIL_PASS` | A Gmail [App Password](https://myaccount.google.com/apppasswords) — **not** your regular password |

> [!NOTE]
> Gmail requires an **App Password** when 2-Step Verification is enabled. Go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords) to generate one.

#### Option A — GitHub Actions (recommended)

Add the secrets to your forked repository so the scheduled workflows can use them:

1. Go to your repo on GitHub → **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret** and add each one:
   - **Name:** `EMAIL_USER` → **Value:** your Gmail address
   - **Name:** `EMAIL_PASS` → **Value:** your Gmail App Password

#### Option B — Local `.env` (for running locally)

Export them in your shell before running a script:

```bash
export EMAIL_USER="you@gmail.com"
export EMAIL_PASS="your-app-password"
```

Or create a `.env` file and source it:

```bash
# .env
export EMAIL_USER="you@gmail.com"
export EMAIL_PASS="your-app-password"
```

```bash
source .env
```

---

## Running Locally

**Check for new internships and send alerts:**

```bash
python monitor.py
```

**Send the full weekly digest:**

```bash
python weekly_digest.py
```

> [!TIP]
> If `EMAIL_USER` / `EMAIL_PASS` are not set, the email content is printed to the terminal instead of being sent. This is handy for testing without credentials.

---

## Automated Scheduling (GitHub Actions)

Once your secrets are set, the two workflows run automatically:

| Workflow | Schedule | Trigger file |
|---|---|---|
| **Job Monitor** | 6:00 and 18:00 BRT (UTC−3) | `.github/workflows/monitor.yml` |
| **Weekly Digest** | Every Sunday at 10:00 BRT (UTC−3) | `.github/workflows/weekly_digest.yml` |

You can also trigger either workflow manually from the **Actions** tab on GitHub.

The monitor workflow automatically commits an updated `known_jobs.json` back to the repo after each run so it remembers which jobs it has already seen.

---

## Project Structure

```
telus-job-scan/
├── monitor.py           # Hourly new-job alert script
├── weekly_digest.py     # Weekly digest script
├── job_service.py       # Fetches & filters internships from the Ashby API
├── email_service.py     # Builds and sends emails via Gmail SMTP
├── known_jobs.json      # Persisted list of seen job IDs (auto-updated)
└── .github/
    └── workflows/
        ├── monitor.yml
        └── weekly_digest.yml
```