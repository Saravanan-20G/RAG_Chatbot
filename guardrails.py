def check_query(query, role):
    sensitive_words = ["salary", "aadhaar"]

    if any(word in query.lower() for word in sensitive_words):
        if role not in ["hr", "admin"]:
            return False

    return True