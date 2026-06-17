# VitaFlow CRM

A customer relationship management (CRM) dashboard built as a course project for the **AI Developer Course — Hebrew University of Jerusalem, 2026**.

Live demo: [vitaflow-crm on Streamlit Cloud](https://vitaflow-crm-rochelle24create.streamlit.app)

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

- **Customers tab** — filterable table of 92 fake customers with health scores, CSAT, MRR, plans, and roles. Select any customer from the dropdown to view their full profile, linked support incidents, and sales leads.
- **Sales Leads tab** — 14 fictional sales opportunities with pipeline stage, value, and owner tracking.
- **Support Incidents tab** — 20 fictional support tickets with type, status, priority, and CSAT tracking.
- **Activity tab** — a chronological feed of recent CRM events.
- **Add / Remove / Flag customers** — full CRUD operations with persistent storage backed by Supabase (PostgreSQL).

---

## Languages & Technologies

| Layer | Technology |
|---|---|
| App framework | [Streamlit](https://streamlit.io) (Python) |
| Backend (original prototype) | [Flask](https://flask.palletsprojects.com) (Python) |
| Database | [Supabase](https://supabase.com) (PostgreSQL) via `psycopg2` |
| Data manipulation | [pandas](https://pandas.pydata.org) |
| Frontend (original prototype) | HTML, CSS, JavaScript |
| Version control | Git / GitHub |
| Hosting | Streamlit Community Cloud |

---

## Datasets

All seed data in this project is **synthetically generated** — no real datasets were used.

| Dataset | Description | Size | Storage |
|---|---|---|---|
| Customers | Fictional health & wellness app users with names, emails, cities, plans, MRR, health scores, CSAT, NPS, session counts, login history, and wellness goals | 92 seed records | **Supabase (PostgreSQL)** — live, persistent. New customers added through the app are saved permanently. |
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

## How to Run Locally

**Prerequisites:** A Supabase project with the `customers` table (auto-created on first run).

```bash
# 1. Clone the repo
git clone https://github.com/rochelle24-create/vitaflow-crm.git
cd vitaflow-crm

# 2. Create and activate a conda environment
conda create -n vitaflow-crm python=3.11
conda activate vitaflow-crm

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your Supabase connection string
# Create .streamlit/secrets.toml with:
# [supabase]
# connection_string = "postgresql://postgres:PASSWORD@db.YOUR_REF.supabase.co:5432/postgres"

# 5. Run the Streamlit app
streamlit run streamlit_app.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.  
On first run the app will automatically create the `customers` table and seed it with 92 records.

---

## Project Structure

```
vitaflow-crm/
├── streamlit_app.py       # Main Streamlit application (Supabase-backed)
├── data.py                # Synthetic customer seed data
├── app.py                 # Original Flask backend (kept for reference)
├── templates/
│   └── index.html         # Original Flask HTML frontend
├── requirements.txt       # Python dependencies
├── .gitignore
└── .streamlit/
    ├── config.toml        # Dark theme configuration
    └── secrets.toml       # Supabase credentials (NOT committed to git)
```

---

*Built as part of the AI Developer Course — Hebrew University of Jerusalem, 2026.*
