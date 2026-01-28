import sqlite3
from datetime import datetime

DB = "lab_logs.db"

def get_conn():
    return sqlite3.connect(DB, check_same_thread=False)

def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            student TEXT,
            experiment TEXT,
            effectiveness REAL,
            time TEXT
        )
    """)
    conn.commit()
    conn.close()

def log_experiment(student, experiment, effectiveness):
    init_db()
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "INSERT INTO logs VALUES (?, ?, ?, ?)",
        (student, experiment, effectiveness, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()
