from werkzeug.security import safe_str_cmp
from user import User

# User's table (DB Sample)
users = [
    # {
    #     'id': 1,
    #     'username': 'bob',
    #     'password': 'asdf'
    # }
    User(1, 'bob', 'asdf')
]

username_mapping = {
    # 'bob': {
    #     'id': 1,
    #     'username': 'bob',
    #     'password': 'asdf'
    # }
    u.username: u for u in users
}

userid_mapping = {
    # ↓ 1 is the user's ID in this sample
    # 1: {
    #     'id': 1,
    #     'username': 'bob',
    #     'password': 'asdf'
    # }
    u.id: u for u in users
}


def authenticate(username, password):
    # ↓ Default Value = None
    user = username_mapping.get(username, None)
    # safe_str_cmp => safe string compare
    if user and safe_str_cmp(user.password, password):
        return user


# Payload = JWT content
def identity(payload):
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)
