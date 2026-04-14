import streamlit as st
import psycopg2
import hashlib

@st.cache_resource
def get_connection():
    return psycopg2.connect(st.secrets["DATABASE_URL"])


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


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


def create_user(username, password, role):
    conn = get_connection()
    cur = conn.cursor()

    hashed_password = hash_password(password)

    try:
        cur.execute(
            """
            INSERT INTO users (username, password, role)
            VALUES (%s, %s, %s)
            """,
            (username, hashed_password, role)
        )
        conn.commit()
        return True

    except Exception:
        conn.rollback()
        return False

    finally:
        cur.close()


def login_user(username, password):
    conn = get_connection()
    cur = conn.cursor()

    hashed_password = hash_password(password)

    cur.execute(
        "SELECT role FROM users WHERE username=%s AND password=%s",
        (username, hashed_password)
    )

    result = cur.fetchone()
    cur.close()

    return result[0] if result else None


def save_chat(role, question, answer):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO chat_history (role, question, answer) VALUES (%s, %s, %s)",
        (role, question, answer)
    )

    conn.commit()
    cur.close()


def get_history(limit=20):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT role, question, answer, created_at
        FROM chat_history
        ORDER BY created_at DESC
        LIMIT %s
    """, (limit,))

    rows = cur.fetchall()
    cur.close()
    return rows


def get_all_users():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT username, role FROM users")
    rows = cur.fetchall()

    cur.close()
    return rows
