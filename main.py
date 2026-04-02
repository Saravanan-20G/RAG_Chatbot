from rag import get_answer
from guardrails import check_query

print("Simple RAG Chatbot 🔥")

role = input("Enter your role (finance/hr/marketing): ").lower()

while True:
    query = input("\nAsk a question: ")

    if query == "exit":
        break

    # Guardrails
    if not check_query(query, role):
        print("❌ Access Denied: Sensitive information")
        continue

    answer = get_answer(query, role)
    print(answer)