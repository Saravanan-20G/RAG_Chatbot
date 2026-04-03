ROLE_ACCESS = {
    "finance": ["finance"],
    "hr": ["hr"],
    "marketing": ["marketing"],
    "analyst": ["finance", "marketing"],
    "admin": ["finance", "hr", "marketing", "admin"]
}

def filter_docs(docs, role):
    if role == "admin":
        return docs   # 🔥 FULL ACCESS (no filtering)

    allowed = ROLE_ACCESS.get(role, [])

    return [
        doc for doc in docs
        if doc.metadata["dept"] in allowed
    ]


# def filter_docs(docs, role):
#     return [doc for doc in docs if doc.metadata["dept"] == role]