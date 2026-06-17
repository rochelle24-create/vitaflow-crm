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

- **Customers tab** — filterable table of 92 fake customers with health scores, CSAT, MRR, plans, and roles. Click any row to view a full customer profile with linked incidents and sales leads.
- **Sales Leads tab** — 14 fictional sales opportunities with pipeline stage, value, and owner tracking.
- **Support Incidents tab** — 20 fictional support tickets with status, priority, and CSAT tracking.
- **Activity tab** — a chronological feed of recent CRM events.
- **Add / Remove / Flag customers** — full CRUD operations backed by a SQLite database.

---

## Languages & Technologies

| Layer | Technology |
|---|---|
| App framework | [Streamlit](https://streamlit.io) (Python) |
| Backend (original) | [Flask](https://flask.palletsprojects.com) (Python) |
| Database | SQLite via Python's built-in `sqlite3` |
| Data manipulation | [pandas](https://pandas.pydata.org) |
| Frontend (original) | HTML, CSS, JavaScript |
| Version control | Git / GitHub |
| Hosting | Streamlit Community Cloud |

---

## Datasets

All data in this project is **synthetically generated** — no real datasets were used.

| Dataset | Description | Size |
|---|---|---|
| Customers | Fictional health & wellness app users with names, emails, cities, plans, MRR, health scores, CSAT, NPS, session counts, login history, and wellness goals | 92 records |
| Account Managers | Fictional CRM account managers assigned to customers | 10 records |
| Sales Leads | Fictional upsell and expansion opportunities linked to customers | 14 records |
| Support Incidents | Fictional customer support tickets with type, status, and priority | 20 records |
| Activity Feed | Fictional recent CRM events (upgrades, logins, churn alerts, etc.) | 15 entries |

---

## AI Models Used

| Purpose | Model |
|---|---|
| Code generation, debugging, and app architecture | **Claude (Anthropic)** via [Cursor](https://cursor.com) |
| Synthetic customer data generation | **Claude (Anthropic)** |
| Synthetic leads, incidents, and activity data | **Claude (Anthropic)** |

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

# 4. Run the Streamlit app
streamlit run streamlit_app.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

---

## Project Structure

```
vitaflow-crm/
├── streamlit_app.py       # Main Streamlit application
├── data.py                # Synthetic customer seed data
├── app.py                 # Original Flask backend (kept for reference)
├── templates/
│   └── index.html         # Original Flask HTML frontend
├── requirements.txt       # Python dependencies
├── .gitignore
└── .streamlit/
    └── config.toml        # Dark theme configuration
```

---

*Built as part of the AI Developer Course — Hebrew University of Jerusalem, 2026.*
