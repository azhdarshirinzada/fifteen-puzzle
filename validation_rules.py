import re


'''

Validation rules by regular expressions
'''


def email_is_valid(email):
    return re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email)


def username_is_valid(username):
    return re.match("^[a-zA-Z0-9_.-]+$", username)


def password_is_valid(password):
    return re.match(r'[A-Za-z0-9@#$%^&+=]{8,}', password)


def name_is_valid(name):
    return re.match(r'^[a-zA-Z ]+$', name)
