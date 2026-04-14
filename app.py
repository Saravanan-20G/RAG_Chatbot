import streamlit as st
from rag import get_answer
from guardrails import check_query
from db import get_history, save_chat, login_user, create_user, init_db

init_db()

# 🔥 RUN ONLY ONCE
# create_user("admin_user", "1234562", "admin")

from db import get_history, save_chat, login_user

# 🔐 Login session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = None

# 🔐 LOGIN SCREEN
# 🔐 Login session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = None

# 🔐 LOGIN / SIGNUP SCREEN
if not st.session_state.logged_in:
    st.markdown("## 🔐 Welcome")

    tab1, tab2 = st.tabs(["🔐 Login", "🆕 Signup"])

    with tab1:
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login"):
            role = login_user(username, password)

            if role:
                st.session_state.logged_in = True
                st.session_state.role = role
                st.success(f"Welcome {username} ({role})")
                st.rerun()
            else:
                st.error("Invalid credentials")

    with tab2:
        st.subheader("Create New Account")

        new_user = st.text_input("New Username", key="signup_username")
        new_pass = st.text_input("New Password", type="password", key="signup_password")
        new_role = st.selectbox("Select Role", ["finance", "hr", "marketing", "analyst"])

        if st.button("Signup"):
            if not new_user or not new_pass:
                st.error("Fill all fields")
            else:
                success = create_user(new_user, new_pass, new_role)

                if success:
                    st.success("Account created successfully. Please login.")
                else:
                    st.error("Username already exists or signup failed.")

    st.stop()
st.set_page_config(page_title="RAG Chatbot", layout="wide")

st.markdown("""
<h2 style='text-align:center; color:#111827;'>
🤖 AI Assistant
</h2>
<p style='text-align:center; color:#6b7280;'>
Ask anything based on your role
</p>
""", unsafe_allow_html=True)
# 🎨 FORCE DARK THEME + BACKGROUND IMAGE
st.markdown("""
<style>

/* 🌟 App Background */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #eef2ff, #f8fafc);
    font-family: 'Segoe UI', sans-serif;
}

/* 🌟 Sidebar Styling */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #ffffff, #f1f5f9);
    border-right: 1px solid #e5e7eb;
}

/* 🌟 Header Styling */
h2 {
    font-size: 34px !important;
    font-weight: 700;
    background: linear-gradient(90deg, #2563eb, #7c3aed);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

p {
    font-size: 15px;
    letter-spacing: 0.5px;
}

/* 🌟 Chat Bubbles (Glass Effect) */
.chat-user {
    background: linear-gradient(135deg, #2563eb, #3b82f6);
    color: white;
    padding: 12px 16px;
    border-radius: 16px;
    margin: 8px 0;
    max-width: 70%;
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
    transition: transform 0.2s ease;
}

.chat-user:hover {
    transform: scale(1.02);
}

.chat-ai {
    background: rgba(255, 255, 255, 0.7);
    backdrop-filter: blur(10px);
    color: #111827;
    padding: 12px 16px;
    border-radius: 16px;
    margin: 8px 0;
    max-width: 70%;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    transition: transform 0.2s ease;
}

.chat-ai:hover {
    transform: scale(1.02);
}

/* 🌟 Buttons */
.stButton button {
    border-radius: 10px;
    background: linear-gradient(90deg, #2563eb, #7c3aed);
    color: white;
    border: none;
    padding: 8px 14px;
    font-weight: 500;
    transition: all 0.2s ease;
}

.stButton button:hover {
    transform: scale(1.05);
    box-shadow: 0 4px 10px rgba(0,0,0,0.15);
}

/* 🌟 Input Box */
[data-testid="stChatInput"] {
    border-radius: 12px;
}

/* 🌟 Tabs */
.stTabs [role="tab"] {
    background: #e5e7eb;
    border-radius: 8px;
    padding: 8px;
    margin-right: 5px;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(90deg, #2563eb, #7c3aed);
    color: white;
}

/* 🌟 Scrollbar (optional) */
::-webkit-scrollbar {
    width: 6px;
}
::-webkit-scrollbar-thumb {
    background: #cbd5f5;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# 🧠 Session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# 📌 Sidebar
with st.sidebar:
    st.header("⚙️ Control Panel")

    role = st.session_state.role
    st.success(f"Logged in as: {role}")

    st.markdown("---")

    if st.button("🧹 Clear Chat"):
        st.session_state.messages = []

    if st.button("⬇️ Download Chat"):
        st.download_button(
            label="Download",
            data=str(st.session_state.messages),
            file_name="chat.txt"
        )

    st.markdown("---")

    st.subheader("📜 Recent History")
    history = get_history()
    for row in history[:5]:
        st.markdown(f"""
        <div style="
            background:#e0f2fe;
            padding:8px;
            border-radius:8px;
            margin-bottom:6px;
            font-size:13px;
        ">
        <b>{row[0]}</b>: {row[1]}
        </div>
        """, unsafe_allow_html=True)

    if st.button("Load History"):
        history = get_history()
        for row in history[-5:]:
            st.write(f"**{row[0]}**: {row[1]}")
    
    st.markdown("---")

    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.role = None
        st.rerun()

# 🎨 Tabs (Interactive UI)
tab1, tab2 = st.tabs(["💬 Chat", "📊 Info"])

# 💬 CHAT TAB
with tab1:

    # Display messages
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(
                f"<div style='display:flex; justify-content:flex-end'>"
                f"<div class='chat-user'>{msg['content']}</div></div>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"<div style='display:flex; justify-content:flex-start'>"
                f"<div class='chat-ai'>{msg['content']}</div></div>",
                unsafe_allow_html=True
            )

    # Input
    user_input = st.chat_input("Ask something...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        st.markdown(f"<div class='chat-user'>👤 {user_input}</div>", unsafe_allow_html=True)

        # Guardrails
        if not check_query(user_input, role):
            response = "❌ Access Denied"
        else:
            with st.spinner("🤖 Thinking..."):
                response = get_answer(user_input, role)

                # 🔥 Save to DB
                save_chat(role, user_input, response)

        st.markdown(f"<div class='chat-ai'>🤖 {response}</div>", unsafe_allow_html=True)

        st.session_state.messages.append({"role": "assistant", "content": response})

# 📊 INFO TAB
with tab2:
    st.markdown("### 🚀 About This Chatbot")

    st.info("""
    This is an enterprise-grade AI chatbot with:

    ✔ RAG (Retrieval-Augmented Generation)  
    ✔ RBAC (Role-Based Access Control)  
    ✔ Guardrails (Security)  
    ✔ LLM (Groq - LLaMA)  
    ✔ Memory + Database  

    Built using Streamlit + LangChain
    """)

    st.markdown("### 🎯 Features")
    st.success("✔ Secure Data Access")
    st.success("✔ Smart AI Responses")
    st.success("✔ Conversation Memory")
