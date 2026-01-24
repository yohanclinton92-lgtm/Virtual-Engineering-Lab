import sqlite3
from datetime import datetime

DB_PATH = "data/lab.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS experiment_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student TEXT,
            experiment TEXT,
            effectiveness REAL,
            timestamp TEXT
        )
    """)

    conn.commit()
    conn.close()


def log_experiment(student, experiment, effectiveness):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO experiment_logs (student, experiment, effectiveness, timestamp)
        VALUES (?, ?, ?, ?)
    """, (student, experiment, effectiveness, datetime.now().isoformat()))

    conn.commit()
    conn.close()


def fetch_all_logs():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT student, experiment, effectiveness, timestamp
        FROM experiment_logs
        ORDER BY timestamp DESC
    """)

    rows = cur.fetchall()
    conn.close()
    return rows
 
