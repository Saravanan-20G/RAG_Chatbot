import streamlit as st
import psycopg2

conn = psycopg2.connect(
    host=st.secrets["localhost"],
    database=st.secrets["project_rag"],
    user=st.secrets["postgres"],
    password=st.secrets["Saran@123"],
    port=st.secrets["5432"]
)
# import psycopg2

# conn = psycopg2.connect(
#     host="localhost",
#     database="project_rag",
#     user="postgres",
#     password="Saran@123"
# )

cursor = conn.cursor()

# Create users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT UNIQUE,
    password TEXT,
    role TEXT
);
""")

conn.commit()

# Create chat history table
cursor.execute("""
CREATE TABLE IF NOT EXISTS chat_history (
    role TEXT,
    question TEXT,
    answer TEXT
)
""")

conn.commit()

# ➕ Add user
def create_user(username, password, role):
    cursor.execute(
        "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
        (username, password, role)
    )
    conn.commit()

# 🔑 Login
def login_user(username, password):
    cursor.execute("SELECT * FROM users")
    print("All users:", cursor.fetchall())  # DEBUG

    cursor.execute(
        "SELECT role FROM users WHERE username=? AND password=?",
        (username, password)
    )
    result = cursor.fetchone()
    return result[0] if result else None


# def login_user(username, password):
#     cursor.execute(
#         "SELECT role FROM users WHERE username=%s AND password=%s",
#         (username, password)
#     )
#     result = cursor.fetchone()
#     return result[0] if result else None

def save_chat(role, question, answer):
    cursor.execute(
        "INSERT INTO chat_history (role, question, answer) VALUES (%s, %s, %s)",
        (role, question, answer)
    )
    conn.commit()

def get_history():
    cursor.execute("""
        SELECT role, question, answer 
        FROM chat_history 
    """)
    return cursor.fetchall()




# import psycopg2

# conn = psycopg2.connect(
#     host="localhost",
#     database="project_rag",
#     user="postgres",
#     password="Saran@123"
# )

# cursor = conn.cursor()
# # Create table
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS chat_history (
#     id INTEGER PRIMARY KEY ,
#     role TEXT,
#     question TEXT,
#     answer TEXT
    
# )
# """)

# conn.commit()

# # Save chat
# def save_chat(role, question, answer):
#     cursor.execute(
#         "INSERT INTO chat_history (role, question, answer) VALUES (?, ?, ?)",
#         (role, question, answer)
#     )
#     conn.commit()

# # Get history
# def get_history():
#     cursor.execute("""
#     SELECT role, question, answer, timestamp 
#     FROM chat_history 
#     ORDER BY id DESC
#     """)
#     return cursor.fetchall()


# # 🔐 Create users table
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS users (
#     id INTEGER PRIMARY KEY ,
#     username TEXT UNIQUE,
#     password TEXT,
#     role TEXT
# )
# """)

# conn.commit()

# # ➕ Add user
# def create_user(username, password, role):
#     cursor.execute(
#         "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
#         (username, password, role)
#     )
#     conn.commit()

# # 🔑 Login check
# def login_user(username, password):
#     cursor.execute(
#         "SELECT role FROM users WHERE username=? AND password=?",
#         (username, password)
#     )
#     result = cursor.fetchone()
#     return result[0] if result else None
