"""
VitaFlow CRM — Flask Backend
Run: python app.py
Then open: http://localhost:5000
"""
from flask import Flask, render_template, jsonify, request
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'vitaflow.db')


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    from data import INITIAL_CUSTOMERS
    conn = get_db()
    conn.execute('''CREATE TABLE IF NOT EXISTS customers (
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
    )''')

    count = conn.execute('SELECT COUNT(*) FROM customers').fetchone()[0]
    if count == 0:
        for c in INITIAL_CUSTOMERS:
            conn.execute(
                '''INSERT INTO customers
                   (name, email, status, plan, mrr, score, csat, since, city, age,
                    goals, sessions, nps, role, username, last_login, login_age, am_idx)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                (c['name'], c['email'], c['status'], c['plan'], c['mrr'],
                 c['score'], c['csat'], c['since'], c['city'], c['age'],
                 c['goals'], c['sessions'], c['nps'], c['role'],
                 c.get('username'), c.get('lastLogin'),
                 c.get('loginAge', 999), c['amIdx'])
            )
    conn.commit()
    conn.close()


# ── Routes ────────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/customers', methods=['GET'])
def get_customers():
    conn = get_db()
    rows = conn.execute('SELECT * FROM customers ORDER BY id').fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.route('/api/customers', methods=['POST'])
def add_customer():
    data = request.get_json()
    if not data or not data.get('name') or not data.get('email'):
        return jsonify({'error': 'Name and email are required'}), 400

    now = datetime.now().strftime('%b %Y')
    conn = get_db()
    cur = conn.execute(
        '''INSERT INTO customers
           (name, email, status, plan, mrr, score, csat, since, city, age,
            goals, role, username, am_idx)
           VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
        (data['name'].strip(),
         data['email'].strip(),
         data.get('status', 'Trial'),
         data.get('plan', 'Starter'),
         int(data.get('mrr', 0)),
         int(data.get('score', 50)),
         float(data.get('csat', 3.5)),
         data.get('since', now),
         data.get('city', '').strip(),
         int(data.get('age', 0)),
         data.get('goals', '').strip(),
         data.get('role', 'Member'),
         data.get('username', '').strip() or None,
         int(data.get('am_idx', 0)))
    )
    new_id = cur.lastrowid
    conn.commit()
    conn.close()
    return jsonify({'id': new_id, 'message': 'Customer added successfully'}), 201


@app.route('/api/customers/<int:cid>', methods=['DELETE'])
def remove_customer(cid):
    conn = get_db()
    result = conn.execute('DELETE FROM customers WHERE id = ?', (cid,))
    conn.commit()
    conn.close()
    if result.rowcount == 0:
        return jsonify({'error': 'Customer not found'}), 404
    return jsonify({'message': 'Customer removed successfully'})


@app.route('/api/customers/<int:cid>/flag', methods=['PUT'])
def flag_customer(cid):
    data = request.get_json() or {}
    conn = get_db()
    row = conn.execute('SELECT flagged FROM customers WHERE id = ?', (cid,)).fetchone()
    if not row:
        conn.close()
        return jsonify({'error': 'Customer not found'}), 404

    new_flag = 0 if row['flagged'] else 1
    note = data.get('note', '').strip() if new_flag else None
    conn.execute('UPDATE customers SET flagged = ?, flag_note = ? WHERE id = ?',
                 (new_flag, note, cid))
    conn.commit()
    conn.close()
    action = 'flagged for CS Manager review' if new_flag else 'flag removed'
    return jsonify({'flagged': bool(new_flag), 'message': f'Customer {action}'})


@app.route('/api/metrics', methods=['GET'])
def get_metrics():
    conn = get_db()
    rows = conn.execute(
        'SELECT status, mrr, csat, username, login_age, flagged FROM customers'
    ).fetchall()
    conn.close()
    total = len(rows)
    if total == 0:
        return jsonify({'total': 0, 'mrr': 0, 'web_users': 0,
                        'recent_logins': 0, 'avg_csat': 0.0, 'flagged': 0})
    total_mrr    = sum(r['mrr'] for r in rows)
    web_users    = sum(1 for r in rows if r['username'])
    recent       = sum(1 for r in rows
                       if r['username'] and r['login_age'] is not None
                       and r['login_age'] <= 7)
    avg_csat     = round(sum(r['csat'] for r in rows) / total, 1)
    flagged      = sum(1 for r in rows if r['flagged'])
    return jsonify({'total': total, 'mrr': total_mrr, 'web_users': web_users,
                    'recent_logins': recent, 'avg_csat': avg_csat, 'flagged': flagged})


if __name__ == '__main__':
    init_db()
    print('\n  VitaFlow CRM running at http://localhost:5000\n')
    app.run(debug=True, port=5000)
