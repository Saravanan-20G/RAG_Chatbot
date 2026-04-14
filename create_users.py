from db import create_user, init_db

init_db()

create_user("finance_user", "1234", "finance")
create_user("hr_user", "12345", "hr")
create_user("marketing_user", "123456", "marketing")
create_user("analyst_user", "1234789", "analyst")
create_user("admin_user", "1234562", "admin")

print("Users created")
