from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document

def ingest_data():
    with open("data.txt", "r") as f:
        lines = f.readlines()

    docs = []
    for line in lines:
        if "Finance" in line:
            dept = "finance"
        elif "HR" in line:
            dept = "hr"
        else:
            dept = "marketing"

        docs.append(Document(
            page_content=line.strip(),
            metadata={"dept": dept}
        ))

    embedding = HuggingFaceEmbeddings()

    db = Chroma.from_documents(docs, embedding, persist_directory="db")
    db.persist()

if __name__ == "__main__":
    ingest_data()