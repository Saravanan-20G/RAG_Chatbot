from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from rbac import filter_docs
import os
from dotenv import load_dotenv

# Use Groq via OpenAI-compatible API
from langchain_groq import ChatGroq


chat_history = []

def get_answer(query, role):
    global chat_history

    embedding = HuggingFaceEmbeddings()

    db = Chroma(persist_directory="db", embedding_function=embedding)

    docs = db.similarity_search(query, k=6)

    # Apply RBAC
    docs = filter_docs(docs, role)

    # 🔥 ADMIN SPECIAL HANDLING
    if role == "admin":
        # Separate admin docs
        admin_docs = [d for d in docs if d.metadata.get("dept") == "admin"]

        # If admin has relevant data → use ONLY admin docs
        if admin_docs:
            docs = admin_docs
        else:
            docs = docs

    # 🚫 Remove conflicting HR statements for admin
    if role == "admin":
        docs = [d for d in docs if "confidential" not in d.page_content.lower()]

    if not docs:
        return "No access or no relevant data"

    context = " ".join([doc.page_content for doc in docs])

    # LLM setup (Groq)
    load_dotenv()

    api_key = os.getenv("GROQ_API_KEY")

    llm = ChatGroq(
        base_url="https://api.groq.com/openai/v1",
        api_key=api_key,
        model="llama-3.3-70b-versatile",
        temperature=0
    )

    prompt = f"""
        You are an intelligent company assistant.

        Instructions:
        - Understand the question
        - Answer in a clear and professional way
        - Do NOT copy text directly
        - Summarize and explain if needed
        - Use the most detailed and relevant information
        - If multiple answers exist, prefer detailed data over generic statements
        - Prefer specific numerical answers
        - Do NOT say "confidential" if actual data is available

        Context:
        {context}

        Question: {query}

        Answer:
        """

    response = llm.invoke(prompt)

    confidence = "High" if len(docs) >= 2 else "Medium" if len(docs) == 1 else "Low"

    return f"{response.content}\n\nConfidence: {confidence}"

print(chat_history)
