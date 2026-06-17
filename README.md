# VitaFlow CRM

A customer relationship management (CRM) dashboard built as a course project for the **AI Developer Course — Hebrew University of Jerusalem, 2026**.

Live demo: [vitaflow-crm on Streamlit Cloud](https://vitaflow-crm-rochelle24create.streamlit.app)

---

## Live Persistent Database — Supabase (PostgreSQL)

> **This deployed app is connected to a live cloud database.**
>
> Every change made through the app is written to [Supabase](https://supabase.com) (PostgreSQL) in real time and persists permanently across sessions, restarts, and redeploys.

| Operation | What happens |
|---|---|
| ➕ **Add a new customer** | Saved permanently to Supabase — visible to anyone who opens the app |
| 🗑 **Remove a customer** | Deleted permanently from Supabase |
| ⚑ **Flag a customer for CS** | Flag and note saved permanently to Supabase |
| 🔄 **App restarts or redeploys** | All data survives — nothing is lost |
| 💻 **Open on a different device** | Same data — it's a shared live database |

The 91 seed customers were loaded once on first launch. Every addition or removal since then is real and persistent.

This demonstrates a key concept in production web applications: **stateless frontend + persistent backend database**. The Streamlit app itself holds no data — it is purely a UI that reads from and writes to Supabase on every interaction.

---

## Disclaimer

> **All names, data, and company information in this project are entirely fictional and were generated for educational purposes only.**
>
> - **VitaFlow** is a made-up company. It does not exist and has no affiliation with any real business.
> - All **customer names**, **email addresses**, **cities**, and **health goals** are fabricated and do not represent real individuals.
> - All **account manager names** are fictional and do not represent real people.
> - Any resemblance to real persons, companies, or events is purely coincidental.

---

## What This Project Does

VitaFlow CRM is a fully functional customer dashboard with:

- **Customers tab** — filterable table of 91 fake customers with health scores, CSAT, MRR, plans, and roles. Select any customer from the dropdown to view their full profile, linked support incidents, and sales leads.
- **Sales Leads tab** — 14 fictional sales opportunities with pipeline stage, value, and owner tracking.
- **Support Incidents tab** — 20 fictional support tickets with type, status, priority, and CSAT tracking.
- **Activity tab** — a chronological feed of recent CRM events.
- **Add / Remove / Flag customers** — full CRUD operations with persistent storage backed by [Supabase](https://supabase.com) (PostgreSQL). New customers survive app restarts and redeploys.

---

## Languages & Technologies

| Layer | Technology |
|---|---|
| App framework | [Streamlit](https://streamlit.io) (Python) |
| Backend (original prototype) | [Flask](https://flask.palletsprojects.com) (Python) |
| Database | [Supabase](https://supabase.com) (PostgreSQL) via [`supabase-py`](https://github.com/supabase-community/supabase-py) |
| Data manipulation | [pandas](https://pandas.pydata.org) |
| Frontend (original prototype) | HTML, CSS, JavaScript |
| Version control | Git / GitHub |
| Hosting | Streamlit Community Cloud |

---

## Datasets

All seed data in this project is **synthetically generated** — no real datasets were used.

| Dataset | Description | Size | Storage |
|---|---|---|---|
| Customers | Fictional health & wellness app users with names, emails, cities, plans, MRR, health scores, CSAT, NPS, session counts, login history, and wellness goals | 91 seed records | **Supabase (PostgreSQL)** — live, persistent. New customers added through the app are saved permanently. |
| Account Managers | Fictional CRM account managers assigned to customers | 10 records | Static (in code) |
| Sales Leads | Fictional upsell and expansion opportunities linked to customers | 14 records | Static (in code) |
| Support Incidents | Fictional customer support tickets with type, status, and priority | 20 records | Static (in code) |
| Activity Feed | Fictional recent CRM events (upgrades, logins, churn alerts, etc.) | 15 entries | Static (in code) |

> The **Customers** dataset is the only live dataset. All create, update (flag), and delete operations are persisted to Supabase and survive app restarts. The remaining datasets are static and exist only for display purposes.

---

## AI Models Used

| Purpose | Model |
|---|---|
| Code generation, debugging, and app architecture | **Claude (Anthropic)** via [Cursor](https://cursor.com) |
| Synthetic customer data generation | **Claude (Anthropic)** |
| Synthetic leads, incidents, and activity data | **Claude (Anthropic)** |

---

## Database Setup (Supabase)

The app connects to Supabase over HTTPS using `supabase-py`. Before running for the first time, create the `customers` table by running this SQL once in your **[Supabase SQL Editor](https://supabase.com/dashboard/project/yoqusbndnvzhydvhqgtk/sql/new)**:

```sql
CREATE TABLE IF NOT EXISTS customers (
    id          SERIAL PRIMARY KEY,
    name        TEXT    NOT NULL,
    email       TEXT    NOT NULL,
    status      TEXT    DEFAULT 'Trial',
    plan        TEXT    DEFAULT 'Starter',
    mrr         INTEGER DEFAULT 0,
    score       INTEGER DEFAULT 50,
    csat        REAL    DEFAULT 3.5,
    since       TEXT,
    city        TEXT    DEFAULT '',
    age         INTEGER DEFAULT 0,
    goals       TEXT    DEFAULT '',
    sessions    INTEGER DEFAULT 0,
    nps         INTEGER DEFAULT 7,
    role        TEXT    DEFAULT 'Member',
    username    TEXT,
    last_login  TEXT,
    login_age   INTEGER DEFAULT 999,
    am_idx      INTEGER DEFAULT 0,
    flagged     INTEGER DEFAULT 0,
    flag_note   TEXT,
    created_at  TEXT    DEFAULT NOW()::TEXT
);

ALTER TABLE customers DISABLE ROW LEVEL SECURITY;
```

After the table exists, the app automatically seeds it with the 91 initial customers on first launch.

---

## How to Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/rochelle24-create/vitaflow-crm.git
cd vitaflow-crm

# 2. Create and activate a conda environment
conda create -n vitaflow-crm python=3.11
conda activate vitaflow-crm

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your Supabase credentials
# Create the file .streamlit/secrets.toml with:
#
# [supabase]
# url = "https://<your-project-ref>.supabase.co"
# key = "sb_publishable_..."   ← anon/public key from Supabase Settings → API

# 5. Run the Streamlit app
streamlit run streamlit_app.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.  
On first run the app will automatically seed the `customers` table with 91 records if it is empty.

### Streamlit Cloud secrets

In your Streamlit Cloud app settings, add the following under **Secrets**:

```toml
[supabase]
url = "https://<your-project-ref>.supabase.co"
key = "sb_publishable_..."
```

---

## Project Structure

```
vitaflow-crm/
├── streamlit_app.py       # Main Streamlit application (Supabase-backed)
├── data.py                # Synthetic customer seed data (91 records)
├── app.py                 # Original Flask backend (kept for reference)
├── templates/
│   └── index.html         # Original Flask HTML frontend
├── requirements.txt       # Python dependencies (streamlit, pandas, supabase)
├── .gitignore
└── .streamlit/
    ├── config.toml        # Dark theme configuration
    └── secrets.toml       # Supabase credentials (NOT committed to git)
```

---

## Architecture Notes

- **Database client:** Migrated from `psycopg2` (raw TCP PostgreSQL connection) to `supabase-py` (HTTPS/REST), which is more reliable on cloud hosting platforms that may not support direct PostgreSQL connections.
- **Connection pooling:** Not required — `supabase-py` uses the Supabase PostgREST API over HTTPS.
- **Secrets management:** Credentials are stored in `.streamlit/secrets.toml` locally and in Streamlit Cloud's encrypted secrets manager for deployment. The `secrets.toml` file is excluded from Git via `.gitignore`.
- **State management:** Customer selection and dialog state are managed via `st.session_state` to persist correctly across Streamlit's rerun model.

---

*Built as part of the AI Developer Course — Hebrew University of Jerusalem, 2026.*
