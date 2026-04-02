import datetime

def log_query(query, role):
    with open("logs.txt", "a") as f:
        f.write(f"{datetime.datetime.now()} | {role} | {query}\n")