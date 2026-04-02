def filter_docs(docs, role):
    return [doc for doc in docs if doc.metadata["dept"] == role]