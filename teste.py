import re

email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

def is_valid_email(email):
    if re.match(email_regex, email):
        return True
    return False

print(is_valid_email("nicole45@example.net"))