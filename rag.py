from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from rbac import filter_docs
import os
from dotenv import load_dotenv

# Use Groq via OpenAI-compatible API
from langchain_openai import ChatOpenAI


chat_history = []

def get_answer(query, role):
    global chat_history

    embedding = HuggingFaceEmbeddings()

    db = Chroma(persist_directory="db", embedding_function=embedding)

    docs = db.similarity_search(query, k=3)

    # RBAC filter
    docs = filter_docs(docs, role)

    if not docs:
        return "No access or no relevant data"

    context = " ".join([doc.page_content for doc in docs])

    # LLM setup (Groq)
    load_dotenv()

    api_key = os.getenv("GROQ_API_KEY")

    llm = ChatOpenAI(
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

        Context:
        {context}

        Question: {query}

        Answer:
        """

    response = llm.invoke(prompt)

    confidence = "High" if len(docs) >= 2 else "Medium" if len(docs) == 1 else "Low"

    return f"{response.content}\n\nConfidence: {confidence}"

print(chat_history)