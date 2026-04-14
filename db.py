import streamlit as st
import psycopg2
from psycopg2.extras import RealDictCursor

# -----------------------------
# 🔌 DB CONNECTION (Neon via URL)
# -----------------------------
@st.cache_resource
def get_connection():
    return psycopg2.connect(
        st.secrets["DATABASE_URL"],
        sslmode="require"
    )


def get_cursor():
    conn = get_connection()
    return conn.cursor(cursor_factory=RealDictCursor)


# -----------------------------
# 🏗️ INIT TABLES (RUN ON START)
# -----------------------------
def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS chat_history (
        id SERIAL PRIMARY KEY,
        role TEXT,
        question TEXT,
        answer TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()
    cur.close()


# -----------------------------
# 👤 CREATE USER
# -----------------------------
def create_user(username, password, role):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
            (username, password, role)
        )
        conn.commit()
    except psycopg2.errors.UniqueViolation:
        conn.rollback()  # prevent crash if user exists

    cur.close()


# -----------------------------
# 🔐 LOGIN USER
# -----------------------------
def login_user(username, password):
    cur = get_cursor()

    cur.execute(
        "SELECT role FROM users WHERE username=%s AND password=%s",
        (username, password)
    )

    result = cur.fetchone()
    cur.close()

    return result["role"] if result else None


# -----------------------------
# 💾 SAVE CHAT
# -----------------------------
def save_chat(role, question, answer):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO chat_history (role, question, answer) VALUES (%s, %s, %s)",
        (role, question, answer)
    )

    conn.commit()
    cur.close()


# -----------------------------
# 📜 GET HISTORY
# -----------------------------
def get_history(limit=20):
    cur = get_cursor()

    cur.execute("""
        SELECT role, question, answer, created_at
        FROM chat_history
        ORDER BY created_at DESC
        LIMIT %s
    """, (limit,))

    results = cur.fetchall()
    cur.close()

    return results
