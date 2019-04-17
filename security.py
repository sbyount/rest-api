# Import safe string compare to mitigate python version incompatibilities
from werkzeug.security import safe_str_cmp
# Import user class
from user import User

users = [
   User(1, 'bob', 'asdf')
]

# Call a user by name
username_mapping = {u.username: u for u in users}

# Call a user by id
userid_mapping = {u.id: u for u in users}

def authenticate(username, password):
    user = username_mapping.get(username, None)
    if user and safe_str_cmp(user.password, password):
        return user

# From Flask-JWT - extract user id from payload
def identity(payload):
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)
