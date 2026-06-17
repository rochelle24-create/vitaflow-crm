"""
VitaFlow CRM — Streamlit App
Run:  streamlit run streamlit_app.py
"""
import os
import sqlite3
from datetime import datetime

import pandas as pd
import streamlit as st

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="VitaFlow CRM",
    page_icon="💚",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Static data ───────────────────────────────────────────────────────────────
ACCOUNT_MANAGERS = [
    "Jordan Ellis", "Priya Shetty", "Ben Nakamura", "Claire Dubois", "Marcus Tate",
    "Aisha Mensah", "Ryan Kowalski", "Nadia Flores", "Owen Burke", "Simone Vance",
]

LEADS = [
    {"Customer": "Leila Farrokhzad", "Opportunity": "Expand Enterprise license to 50-seat team plan",    "Stage": "Negotiating",   "Value": 28800, "Score": 88, "Owner": "Dana Park",  "Next Action": "Send contract draft",          "Date": "Mar 14, 2026"},
    {"Customer": "Leila Farrokhzad", "Opportunity": "Add clinical data integration add-on",              "Stage": "Proposal sent", "Value": 6000,  "Score": 74, "Owner": "Mia Russo",  "Next Action": "Follow up compliance",         "Date": "Mar 10, 2026"},
    {"Customer": "Priya Nair",       "Opportunity": "Upsell to VitaFlow Clinic tier",                    "Stage": "Qualifying",    "Value": 4800,  "Score": 81, "Owner": "Chris Osei", "Next Action": "Book discovery call",          "Date": "Mar 16, 2026"},
    {"Customer": "Yuki Tanaka",      "Opportunity": "Refer corporate wellness deal — employer",           "Stage": "Prospecting",   "Value": 14400, "Score": 65, "Owner": "Tyler Ng",   "Next Action": "Request intro email",          "Date": "Mar 12, 2026"},
    {"Customer": "Marcus Webb",      "Opportunity": "Upgrade to Family plan — getting married in June",   "Stage": "Qualifying",    "Value": 720,   "Score": 70, "Owner": "Dana Park",  "Next Action": "Send Family plan one-pager",   "Date": "Mar 8, 2026"},
    {"Customer": "Sofia Alvarez",    "Opportunity": "Add teenage kids as sub-accounts",                   "Stage": "Won",           "Value": 480,   "Score": 95, "Owner": "Mia Russo",  "Next Action": "Closed — won",                "Date": "Feb 28, 2026"},
    {"Customer": "Amara Diallo",     "Opportunity": "Upgrade to Enterprise for fertility clinic",         "Stage": "Prospecting",   "Value": 9600,  "Score": 58, "Owner": "Chris Osei", "Next Action": "Send clinic partnership deck", "Date": "Mar 17, 2026"},
    {"Customer": "Tobias Müller",    "Opportunity": "Add 10 sub-accounts for leadership team",            "Stage": "Negotiating",   "Value": 12000, "Score": 82, "Owner": "Kenji Sato", "Next Action": "Finalize seat count",          "Date": "Mar 13, 2026"},
    {"Customer": "Isabelle Dupont",  "Opportunity": "Co-branding partnership — wellness content",         "Stage": "Proposal sent", "Value": 24000, "Score": 77, "Owner": "Dana Park",  "Next Action": "Legal review of proposal",     "Date": "Mar 11, 2026"},
    {"Customer": "Annika Lindqvist", "Opportunity": "Sponsor VitaFlow ultra-marathon challenge",          "Stage": "Qualifying",    "Value": 8000,  "Score": 69, "Owner": "Tyler Ng",   "Next Action": "Influencer brief meeting",     "Date": "Mar 15, 2026"},
    {"Customer": "Leo Martínez",     "Opportunity": "Athletic team license for 25 players",               "Stage": "Prospecting",   "Value": 18000, "Score": 63, "Owner": "Kenji Sato", "Next Action": "Send team plan deck",          "Date": "Mar 17, 2026"},
    {"Customer": "Dmitri Volkov",    "Opportunity": "Cold therapy add-on module",                         "Stage": "Qualifying",    "Value": 3600,  "Score": 72, "Owner": "Chris Osei", "Next Action": "Product team intro",           "Date": "Mar 9, 2026"},
    {"Customer": "Hiroshi Watanabe", "Opportunity": "Refer enterprise deal — Hiroshi's firm",             "Stage": "Prospecting",   "Value": 36000, "Score": 61, "Owner": "Tyler Ng",   "Next Action": "Request HR intro",             "Date": "Mar 16, 2026"},
    {"Customer": "Viviane Santos",   "Opportunity": "Launch VitaFlow wellness retreat partnership",       "Stage": "Proposal sent", "Value": 15000, "Score": 79, "Owner": "Mia Russo",  "Next Action": "Await partner agreement",      "Date": "Mar 12, 2026"},
]

INCIDENTS = [
    {"ID": "#1042", "Customer": "Yuki Tanaka",     "Issue": "Biometric sync failing on Apple Watch Series 9", "Type": "Technical", "Status": "Open",      "Priority": "High",   "Date": "Mar 15, 2026", "CSAT": "—"},
    {"ID": "#1041", "Customer": "Priya Nair",       "Issue": "Duplicate charge on Feb invoice",                "Type": "Billing",   "Status": "Resolved",  "Priority": "High",   "Date": "Mar 12, 2026", "CSAT": "5/5"},
    {"ID": "#1040", "Customer": "James Okafor",     "Issue": "Unable to access mindfulness module",            "Type": "Technical", "Status": "Open",      "Priority": "Medium", "Date": "Mar 11, 2026", "CSAT": "—"},
    {"ID": "#1039", "Customer": "Rachel Kim",       "Issue": "Password reset email not arriving",              "Type": "Account",   "Status": "Resolved",  "Priority": "Low",    "Date": "Mar 9, 2026",  "CSAT": "4/5"},
    {"ID": "#1038", "Customer": "Tom Bradshaw",     "Issue": "Feature request: meal barcode scanner",          "Type": "Feature",   "Status": "Open",      "Priority": "Low",    "Date": "Mar 8, 2026",  "CSAT": "—"},
    {"ID": "#1037", "Customer": "Derek Hollis",     "Issue": "Subscription cancellation not processed",        "Type": "Billing",   "Status": "Escalated", "Priority": "High",   "Date": "Mar 5, 2026",  "CSAT": "1/5"},
    {"ID": "#1036", "Customer": "Amara Diallo",     "Issue": "Cycle prediction data reset unexpectedly",       "Type": "Technical", "Status": "Resolved",  "Priority": "High",   "Date": "Feb 28, 2026", "CSAT": "4/5"},
    {"ID": "#1035", "Customer": "Marcus Webb",      "Issue": "Sleep score showing 0 despite data",             "Type": "Technical", "Status": "Resolved",  "Priority": "Medium", "Date": "Feb 24, 2026", "CSAT": "5/5"},
    {"ID": "#1034", "Customer": "Sofia Alvarez",    "Issue": "Family member profile removed after update",     "Type": "Account",   "Status": "Resolved",  "Priority": "Medium", "Date": "Feb 20, 2026", "CSAT": "4/5"},
    {"ID": "#1033", "Customer": "Leila Farrokhzad", "Issue": "Enterprise SSO login timeout issue",             "Type": "Technical", "Status": "Escalated", "Priority": "High",   "Date": "Feb 17, 2026", "CSAT": "3/5"},
    {"ID": "#1032", "Customer": "Priya Nair",       "Issue": "Dashboard widgets not saving layout",            "Type": "Technical", "Status": "Resolved",  "Priority": "Low",    "Date": "Feb 10, 2026", "CSAT": "5/5"},
    {"ID": "#1031", "Customer": "Yuki Tanaka",      "Issue": "Annual renewal price discrepancy",               "Type": "Billing",   "Status": "Resolved",  "Priority": "Medium", "Date": "Jan 30, 2026", "CSAT": "5/5"},
    {"ID": "#1030", "Customer": "Daniel Park",      "Issue": "Notification spam after app update",             "Type": "Technical", "Status": "Resolved",  "Priority": "Low",    "Date": "Mar 14, 2026", "CSAT": "4/5"},
    {"ID": "#1029", "Customer": "Leo Martínez",     "Issue": "Heart rate zones not calibrating correctly",     "Type": "Technical", "Status": "Open",      "Priority": "Medium", "Date": "Mar 13, 2026", "CSAT": "—"},
    {"ID": "#1028", "Customer": "Fatima Hassan",    "Issue": "Family invite link expired before use",          "Type": "Account",   "Status": "Resolved",  "Priority": "Low",    "Date": "Mar 10, 2026", "CSAT": "5/5"},
    {"ID": "#1027", "Customer": "Tobias Müller",    "Issue": "Enterprise dashboard missing Q1 export",         "Type": "Billing",   "Status": "Escalated", "Priority": "High",   "Date": "Mar 7, 2026",  "CSAT": "2/5"},
    {"ID": "#1026", "Customer": "Chloe Nguyen",     "Issue": "App crashes on iPhone 16 Pro",                   "Type": "Technical", "Status": "Open",      "Priority": "High",   "Date": "Mar 15, 2026", "CSAT": "—"},
    {"ID": "#1025", "Customer": "Annika Lindqvist", "Issue": "GPS route tracking drops mid-run",               "Type": "Technical", "Status": "Open",      "Priority": "Medium", "Date": "Mar 14, 2026", "CSAT": "—"},
    {"ID": "#1024", "Customer": "Carlos Reyes",     "Issue": "Meal plan not syncing with family profiles",     "Type": "Account",   "Status": "Resolved",  "Priority": "Medium", "Date": "Mar 6, 2026",  "CSAT": "4/5"},
    {"ID": "#1023", "Customer": "Ingrid Bjornstad", "Issue": "Cold exposure module showing wrong timer",       "Type": "Technical", "Status": "Resolved",  "Priority": "Low",    "Date": "Mar 3, 2026",  "CSAT": "5/5"},
]

ACTIVITIES = [
    {"time": "2 min ago",  "event": "Yuki Tanaka upgraded to Enterprise plan",                     "type": "success"},
    {"time": "8 min ago",  "event": "Astrid Svensson logged in — 318 total sessions milestone",   "type": "info"},
    {"time": "14 min ago", "event": "New trial signup: Max Steinberg (Starter)",                  "type": "info"},
    {"time": "31 min ago", "event": "Derek Hollis — churn detected, account inactive 60+ days",  "type": "error"},
    {"time": "1 hr ago",   "event": "Amara Diallo completed 100th wellness session",              "type": "success"},
    {"time": "2 hrs ago",  "event": "New lead logged: Hiroshi Watanabe — enterprise referral",   "type": "info"},
    {"time": "2 hrs ago",  "event": "Viviane Santos lead updated: proposal sent to partner team", "type": "info"},
    {"time": "3 hrs ago",  "event": "Annika Lindqvist logged 6:30 AM — daily streak: 94 days",   "type": "success"},
    {"time": "4 hrs ago",  "event": "Tobias Müller incident escalated — Q1 export missing",      "type": "error"},
    {"time": "5 hrs ago",  "event": "James Okafor trial ending in 3 days — no payment on file",  "type": "warning"},
    {"time": "6 hrs ago",  "event": "Isabelle Dupont: co-branding proposal entered legal review", "type": "info"},
    {"time": "Yesterday",  "event": "Sofia Alvarez lead closed — won teen sub-accounts",         "type": "success"},
    {"time": "Yesterday",  "event": "Penelope Gray — churned, no response to 3 re-engagement emails", "type": "error"},
    {"time": "2 days ago", "event": "Camille Rousseau completed prenatal milestone check-in",    "type": "success"},
    {"time": "2 days ago", "event": "Dmitri Volkov: cold therapy add-on qualifying call scheduled", "type": "info"},
]

# ── Database ──────────────────────────────────────────────────────────────────
DB_PATH = "vitaflow.db"


def get_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    from data import INITIAL_CUSTOMERS
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
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
            created_at  TEXT    DEFAULT CURRENT_TIMESTAMP
        )
    """)
    if conn.execute("SELECT COUNT(*) FROM customers").fetchone()[0] == 0:
        for c in INITIAL_CUSTOMERS:
            conn.execute(
                """INSERT INTO customers
                   (name,email,status,plan,mrr,score,csat,since,city,age,
                    goals,sessions,nps,role,username,last_login,login_age,am_idx)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (c["name"], c["email"], c["status"], c["plan"], c["mrr"],
                 c["score"], c["csat"], c["since"], c["city"], c["age"],
                 c["goals"], c["sessions"], c["nps"], c["role"],
                 c.get("username"), c.get("lastLogin"), c.get("loginAge", 999), c["amIdx"]),
            )
        conn.commit()
    conn.close()


if "db_ready" not in st.session_state:
    init_db()
    st.session_state.db_ready = True

# ── DB helpers ────────────────────────────────────────────────────────────────

def fetch_customers():
    conn = get_db()
    df = pd.read_sql_query("SELECT * FROM customers ORDER BY id", conn)
    conn.close()
    return df


def fetch_metrics():
    conn = get_db()
    df = pd.read_sql_query("SELECT mrr,csat,username,login_age,flagged FROM customers", conn)
    conn.close()
    if df.empty:
        return dict(total=0, mrr=0, web_users=0, recent_logins=0, avg_csat=0.0, flagged=0)
    web = df["username"].notna() & (df["username"] != "")
    return dict(
        total=len(df),
        mrr=int(df["mrr"].sum()),
        web_users=int(web.sum()),
        recent_logins=int((web & (df["login_age"] <= 7)).sum()),
        avg_csat=round(float(df["csat"].mean()), 1),
        flagged=int(df["flagged"].sum()),
    )


def db_add_customer(data):
    conn = get_db()
    conn.execute(
        """INSERT INTO customers
           (name,email,status,plan,mrr,score,csat,since,city,age,goals,role,username,am_idx)
           VALUES (?,?,?,?,?,50,3.5,?,?,?,?,?,?,?)""",
        (data["name"], data["email"], data["status"], data["plan"], data["mrr"],
         data["since"], data["city"], data["age"], data["goals"],
         data["role"], data["username"] or None, data["am_idx"]),
    )
    conn.commit()
    conn.close()


def db_remove_customer(cid):
    conn = get_db()
    conn.execute("DELETE FROM customers WHERE id=?", (cid,))
    conn.commit()
    conn.close()


def db_toggle_flag(cid, note=""):
    conn = get_db()
    row = conn.execute("SELECT flagged FROM customers WHERE id=?", (cid,)).fetchone()
    if row:
        new_flag = 0 if row["flagged"] else 1
        conn.execute(
            "UPDATE customers SET flagged=?,flag_note=? WHERE id=?",
            (new_flag, note if new_flag else None, cid),
        )
        conn.commit()
    conn.close()


def db_resolve_flag(cid):
    conn = get_db()
    conn.execute("UPDATE customers SET flagged=0,flag_note=NULL WHERE id=?", (cid,))
    conn.commit()
    conn.close()


# ── Dialogs ───────────────────────────────────────────────────────────────────

@st.dialog("Add New Customer")
def dialog_add_customer():
    with st.form("add_form"):
        c1, c2 = st.columns(2)
        with c1:
            name     = st.text_input("Full name *")
            status   = st.selectbox("Status", ["Trial", "Active", "Premium", "Churned"])
            role     = st.selectbox("Role", ["Member", "Admin", "Trial user", "Viewer"])
            city     = st.text_input("City")
            username = st.text_input("Username (optional)")
        with c2:
            email  = st.text_input("Email *")
            plan   = st.selectbox("Plan", ["Starter", "Wellness Pro", "Family", "Enterprise"])
            am_idx = st.selectbox(
                "Account Manager", range(len(ACCOUNT_MANAGERS)),
                format_func=lambda i: ACCOUNT_MANAGERS[i],
            )
            age = st.number_input("Age", 0, 120, value=30)
            mrr = st.number_input("MRR ($)", 0, 10000, value=0)
        goals = st.text_input("Health goals")

        if st.form_submit_button("Add Customer", type="primary", use_container_width=True):
            if not name.strip() or not email.strip():
                st.error("Name and email are required.")
            else:
                db_add_customer({
                    "name": name.strip(), "email": email.strip(),
                    "status": status, "plan": plan, "mrr": int(mrr),
                    "since": datetime.now().strftime("%b %Y"),
                    "city": city.strip(), "age": int(age), "goals": goals.strip(),
                    "role": role, "username": username.strip(), "am_idx": int(am_idx),
                })
                st.success(f"✓ {name} added to CRM")
                st.rerun()


@st.dialog("Flag Customer for CS Manager")
def dialog_flag_customer(customer_id: int):
    # Fetch fresh from DB — avoids numpy type serialization issues
    conn = get_db()
    row = conn.execute(
        "SELECT id, name, flagged, flag_note FROM customers WHERE id=?", (customer_id,)
    ).fetchone()
    conn.close()
    if not row:
        st.error("Customer not found.")
        return

    name      = row["name"]
    flagged   = row["flagged"]
    flag_note = row["flag_note"] or ""

    if flagged:
        st.warning(f"**Currently flagged:** {flag_note or 'No note provided'}")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✓ Resolve Flag", type="primary", use_container_width=True):
                db_resolve_flag(customer_id)
                st.rerun()
        with col2:
            if st.button("Cancel", use_container_width=True):
                st.rerun()
    else:
        st.write(f"Flag **{name}** for CS Manager review.")
        note = st.text_area(
            "Reason / note for CS Manager",
            placeholder="Describe why this customer needs attention...",
        )
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⚑ Flag for CS Manager", type="primary", use_container_width=True):
                db_toggle_flag(customer_id, note)
                st.rerun()
        with col2:
            if st.button("Cancel", use_container_width=True):
                st.rerun()


# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div style="margin-bottom:24px;padding-bottom:20px;border-bottom:2px solid #1e3054;">
      <div style="font-size:26px;font-weight:700;letter-spacing:-0.5px;">
        Vita<span style="color:#4a9eff;">Flow</span>&nbsp;
        <span style="font-size:16px;font-weight:400;color:#6b84a8;">CRM</span>
      </div>
      <div style="font-size:12px;color:#6b84a8;margin-top:2px;letter-spacing:0.3px;">
        Health &amp; Wellness Consumer Platform
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Tabs ──────────────────────────────────────────────────────────────────────
t_customers, t_leads, t_incidents, t_activity = st.tabs([
    "👥  Customers",
    "📊  Sales Leads",
    "🎫  Support Incidents",
    "📋  Activity",
])

# ═════════════════════════════════════════════════════════════════════════════
# CUSTOMERS TAB
# ═════════════════════════════════════════════════════════════════════════════
with t_customers:
    metrics = fetch_metrics()

    # ── Metric cards ──────────────────────────────────────────────────────────
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Total Customers",  metrics["total"],              "Across all plans")
    m2.metric("Monthly Revenue",  f"${metrics['mrr'] / 1000:.1f}K", "+8.4% vs last month")
    m3.metric(
        "Active Web Users",
        f"{metrics['web_users']}/{metrics['total']}",
        f"{metrics['recent_logins']} logged in last 7 days",
    )
    m4.metric("Avg CSAT", f"{metrics['avg_csat']}/5", "+0.2 this quarter")
    m5.metric(
        "CS Flagged",
        metrics["flagged"],
        "Needs attention" if metrics["flagged"] > 0 else "No flags active",
    )

    st.divider()

    # ── Filters row 1 ─────────────────────────────────────────────────────────
    f1, f2, f3, f4 = st.columns([3, 1.5, 1.5, 1.5])
    with f1:
        q = st.text_input(
            "", placeholder="🔍  Search name, email, city, username...",
            label_visibility="collapsed",
        )
    with f2:
        status_f = st.selectbox(
            "Status", ["All statuses", "Active", "Trial", "Churned", "Premium"],
            label_visibility="collapsed",
        )
    with f3:
        plan_f = st.selectbox(
            "Plan", ["All plans", "Starter", "Wellness Pro", "Family", "Enterprise"],
            label_visibility="collapsed",
        )
    with f4:
        role_f = st.selectbox(
            "Role", ["All roles", "Admin", "Member", "Viewer", "Trial user"],
            label_visibility="collapsed",
        )

    # ── Filters row 2 ─────────────────────────────────────────────────────────
    f5, f6, f7, _, btn_col = st.columns([2, 1.5, 1.5, 2, 1.5])
    with f5:
        am_f = st.selectbox(
            "AM", ["All AMs"] + ACCOUNT_MANAGERS,
            label_visibility="collapsed",
        )
    with f6:
        web_f = st.selectbox(
            "Web", ["All web", "Has account", "No account"],
            label_visibility="collapsed",
        )
    with f7:
        flag_f = st.selectbox(
            "Flag", ["All customers", "⚑ Flagged only"],
            label_visibility="collapsed",
        )
    with btn_col:
        if st.button("＋  Add Customer", type="primary", use_container_width=True):
            dialog_add_customer()

    # ── Load & filter ──────────────────────────────────────────────────────────
    df = fetch_customers()

    if q:
        mask = (
            df["name"].str.lower().str.contains(q.lower(), na=False)
            | df["email"].str.lower().str.contains(q.lower(), na=False)
            | df["city"].str.lower().str.contains(q.lower(), na=False)
            | df["username"].fillna("").str.lower().str.contains(q.lower())
        )
        df = df[mask]
    if status_f != "All statuses":
        df = df[df["status"] == status_f]
    if plan_f != "All plans":
        df = df[df["plan"] == plan_f]
    if role_f != "All roles":
        df = df[df["role"] == role_f]
    if am_f != "All AMs":
        df = df[df["am_idx"] == ACCOUNT_MANAGERS.index(am_f)]
    if web_f == "Has account":
        df = df[df["username"].notna() & (df["username"] != "")]
    elif web_f == "No account":
        df = df[df["username"].isna() | (df["username"] == "")]
    if flag_f == "⚑ Flagged only":
        df = df[df["flagged"] == 1]

    # ── Build display dataframe ────────────────────────────────────────────────
    disp = pd.DataFrame({
        "Name":            df["name"].values,
        "Email":           df["email"].values,
        "Status":          df["status"].values,
        "Plan":            df["plan"].values,
        "Role":            df["role"].values,
        "Account Manager": df["am_idx"].apply(
            lambda i: ACCOUNT_MANAGERS[int(i)] if pd.notna(i) and int(i) < len(ACCOUNT_MANAGERS) else "—"
        ).values,
        "Username":        df["username"].fillna("—").values,
        "Last Login":      df["last_login"].fillna("—").values,
        "Health":          df["score"].astype(int).values,
        "CSAT":            df["csat"].round(1).values,
        "MRR ($)":         df["mrr"].values,
        "Since":           df["since"].values,
        "⚑":              df["flagged"].apply(lambda f: "⚑" if f else "").values,
    })

    event = st.dataframe(
        disp,
        use_container_width=True,
        hide_index=True,
        height=460,
        on_select="rerun",
        selection_mode="single-row",
        column_config={
            "Health": st.column_config.ProgressColumn(
                "Health", min_value=0, max_value=100, format="%d"
            ),
            "CSAT": st.column_config.NumberColumn("CSAT", format="%.1f"),
            "MRR ($)": st.column_config.NumberColumn("MRR ($)", format="$%d"),
        },
    )
    st.caption(f"Showing {len(df)} of {metrics['total']} customers  ·  click a row to view details")

    # ── Customer Detail ────────────────────────────────────────────────────────
    sel = event.selection.rows
    if sel:
        cust = df.iloc[sel[0]].to_dict()
        am   = ACCOUNT_MANAGERS[int(cust["am_idx"])] if pd.notna(cust.get("am_idx")) else "—"

        st.markdown("---")
        h1, h2 = st.columns([6, 1])
        with h1:
            flag_icon = "  ⚑" if cust["flagged"] else ""
            st.markdown(f"### {cust['name']}{flag_icon}")
            st.caption(
                f"{cust['email']}  ·  {cust['city']}  ·  Age {cust['age']}  ·  Customer since {cust['since']}"
            )
        with h2:
            st.markdown(f"**{cust['status']}** — {cust['plan']}")

        if cust["flagged"]:
            st.warning(f"⚑  **Flagged for CS Manager:** {cust['flag_note'] or 'No note provided'}")

        d1, d2, d3 = st.columns(3)
        with d1:
            st.markdown("**Customer Info**")
            st.markdown(f"Goals: {cust['goals'] or '—'}")
            st.markdown(f"Role: {cust['role']}")
            st.markdown(f"Account Manager: {am}")
        with d2:
            st.markdown("**Web Account**")
            if cust["username"]:
                st.markdown(f"Username: `@{cust['username']}`")
            else:
                st.markdown("No web account")
            st.markdown(f"Last Login: {cust['last_login'] or '—'}")
        with d3:
            st.markdown("**Revenue & Engagement**")
            st.markdown(f"MRR: {'$' + str(cust['mrr']) if cust['mrr'] > 0 else '—'}")
            st.markdown(f"LTV (est.): {'$' + str(round(cust['mrr'] * 14)) if cust['mrr'] > 0 else '—'}")
            st.markdown(f"Sessions: {cust['sessions']}")

        mc1, mc2, mc3, mc4 = st.columns(4)
        mc1.metric("Health Score", f"{cust['score']}/100")
        mc2.metric("CSAT",         f"{cust['csat']:.1f}/5")
        mc3.metric("NPS",          f"{cust['nps']}/10")
        mc4.metric("Sessions",     cust["sessions"])

        # ── Linked incidents ──────────────────────────────────────────────────
        linked_inc = [i for i in INCIDENTS if i["Customer"] == cust["name"]]
        if linked_inc:
            st.markdown(f"**Support History** ({len(linked_inc)} incident{'s' if len(linked_inc) != 1 else ''})")
            st.dataframe(
                pd.DataFrame(linked_inc)[["ID", "Issue", "Type", "Status", "Priority", "Date", "CSAT"]],
                use_container_width=True,
                hide_index=True,
            )

        # ── Linked leads ──────────────────────────────────────────────────────
        linked_leads = [l for l in LEADS if l["Customer"] == cust["name"]]
        if linked_leads:
            st.markdown(f"**Sales Leads** ({len(linked_leads)})")
            ld = pd.DataFrame(linked_leads)
            ld["Value"] = ld["Value"].apply(lambda v: f"${v:,}")
            st.dataframe(
                ld[["Opportunity", "Stage", "Value", "Score", "Owner", "Next Action", "Date"]],
                use_container_width=True,
                hide_index=True,
            )

        # ── Actions ───────────────────────────────────────────────────────────
        st.markdown("")
        a1, a2, _ = st.columns([1.5, 1.8, 5])
        with a1:
            flag_label = "⚑  Update Flag" if cust["flagged"] else "⚐  Flag for CS"
            if st.button(flag_label, key="btn_flag"):
                dialog_flag_customer(int(cust["id"]))
        with a2:
            if st.button("🗑  Remove Customer", key="btn_remove", type="secondary"):
                db_remove_customer(int(cust["id"]))
                st.toast(f"{cust['name']} removed from CRM.")
                st.rerun()


# ═════════════════════════════════════════════════════════════════════════════
# SALES LEADS TAB
# ═════════════════════════════════════════════════════════════════════════════
with t_leads:
    lm1, lm2, lm3, lm4 = st.columns(4)
    lm1.metric("Open Leads",       "14",    "+3 this week")
    lm2.metric("Pipeline Value",   "$312K", "Est. annual upside")
    lm3.metric("Avg Lead Score",   "71",    "Strong pipeline")
    lm4.metric("Won This Quarter", "9",     "$74K closed")

    st.divider()

    lf1, lf2, lf3 = st.columns([3, 1.5, 1.5])
    with lf1:
        lq = st.text_input(
            "", placeholder="🔍  Search leads...", key="lsearch",
            label_visibility="collapsed",
        )
    with lf2:
        stage_f = st.selectbox(
            "Stage",
            ["All stages", "Prospecting", "Qualifying", "Proposal sent", "Negotiating", "Won"],
            label_visibility="collapsed", key="lstage",
        )
    with lf3:
        owner_f = st.selectbox(
            "Owner",
            ["All reps", "Dana Park", "Chris Osei", "Mia Russo", "Tyler Ng", "Kenji Sato"],
            label_visibility="collapsed", key="lowner",
        )

    leads_df = pd.DataFrame(LEADS)
    if lq:
        leads_df = leads_df[
            leads_df["Customer"].str.lower().str.contains(lq.lower(), na=False)
            | leads_df["Opportunity"].str.lower().str.contains(lq.lower(), na=False)
        ]
    if stage_f != "All stages":
        leads_df = leads_df[leads_df["Stage"] == stage_f]
    if owner_f != "All reps":
        leads_df = leads_df[leads_df["Owner"] == owner_f]

    leads_disp = leads_df.copy()
    leads_disp["Value"] = leads_disp["Value"].apply(lambda v: f"${v:,}")

    st.dataframe(
        leads_disp[["Customer", "Opportunity", "Stage", "Value", "Score", "Owner", "Next Action", "Date"]],
        use_container_width=True,
        hide_index=True,
        column_config={
            "Score": st.column_config.ProgressColumn("Score", min_value=0, max_value=100, format="%d"),
        },
    )
    st.caption(f"Showing {len(leads_df)} leads")


# ═════════════════════════════════════════════════════════════════════════════
# SUPPORT INCIDENTS TAB
# ═════════════════════════════════════════════════════════════════════════════
with t_incidents:
    im1, im2, im3, im4 = st.columns(4)
    im1.metric("Total Incidents", "89",     "+11 this month")
    im2.metric("Open",            "18",     "Needs attention")
    im3.metric("Avg Resolution",  "1.6d",   "-0.2d vs last month")
    im4.metric("CSAT Score",      "4.4/5",  "Stable")

    st.divider()

    if1, if2, if3 = st.columns([3, 1.5, 1.5])
    with if1:
        iq = st.text_input(
            "", placeholder="🔍  Search incidents...", key="isearch",
            label_visibility="collapsed",
        )
    with if2:
        istatus_f = st.selectbox(
            "Status", ["All", "Open", "Resolved", "Escalated"],
            label_visibility="collapsed", key="istatus",
        )
    with if3:
        itype_f = st.selectbox(
            "Type", ["All types", "Billing", "Technical", "Account", "Feature"],
            label_visibility="collapsed", key="itype",
        )

    inc_df = pd.DataFrame(INCIDENTS)
    if iq:
        inc_df = inc_df[
            inc_df["Customer"].str.lower().str.contains(iq.lower(), na=False)
            | inc_df["Issue"].str.lower().str.contains(iq.lower(), na=False)
        ]
    if istatus_f != "All":
        inc_df = inc_df[inc_df["Status"] == istatus_f]
    if itype_f != "All types":
        inc_df = inc_df[inc_df["Type"] == itype_f]

    st.dataframe(inc_df, use_container_width=True, hide_index=True)
    st.caption(f"Showing {len(inc_df)} incidents")


# ═════════════════════════════════════════════════════════════════════════════
# ACTIVITY TAB
# ═════════════════════════════════════════════════════════════════════════════
with t_activity:
    st.subheader("Recent Activity")
    st.markdown("")

    TYPE_ICON = {"success": "🟢", "info": "🔵", "warning": "🟡", "error": "🔴"}

    for a in ACTIVITIES:
        icon = TYPE_ICON.get(a["type"], "⚪")
        col1, col2 = st.columns([6, 1])
        with col1:
            st.markdown(f"{icon} &nbsp; {a['event']}")
        with col2:
            st.caption(a["time"])
        st.divider()
