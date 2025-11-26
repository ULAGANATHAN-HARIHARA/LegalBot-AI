# modules/utils/db_utils.py
import sqlite3
import os
from typing import Optional

DB_FILE = os.path.join(os.getcwd(), "legalbot.sqlite3")

def get_conn():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    return conn

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            query TEXT,
            answer TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def register_user(username: str, password: str) -> bool:
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        conn.close()

def login_user(username: str, password: str) -> bool:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE username=? AND password=?", (username, password))
    r = cur.fetchone()
    conn.close()
    return bool(r)

def save_history(username: str, query: str, answer: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO history (username, query, answer) VALUES (?, ?, ?)", (username, query, answer))
    conn.commit()
    conn.close()

def get_history(username: str, limit: int = 50):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT query, answer, created_at FROM history WHERE username=? ORDER BY id DESC LIMIT ?", (username, limit))
    rows = cur.fetchall()
    conn.close()
    return rows
