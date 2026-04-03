import sqlite3

conn = sqlite3.connect("chat.db", check_same_thread=False)
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS chat_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role TEXT,
    question TEXT,
    answer TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()

# Save chat
def save_chat(role, question, answer):
    cursor.execute(
        "INSERT INTO chat_history (role, question, answer) VALUES (?, ?, ?)",
        (role, question, answer)
    )
    conn.commit()

# Get history
def get_history():
    cursor.execute("""
    SELECT role, question, answer, timestamp 
    FROM chat_history 
    ORDER BY id DESC
    """)
    return cursor.fetchall()


# 🔐 Create users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT
)
""")

conn.commit()

# ➕ Add user
def create_user(username, password, role):
    cursor.execute(
        "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
        (username, password, role)
    )
    conn.commit()

# 🔑 Login check
def login_user(username, password):
    cursor.execute(
        "SELECT role FROM users WHERE username=? AND password=?",
        (username, password)
    )
    result = cursor.fetchone()
    return result[0] if result else None