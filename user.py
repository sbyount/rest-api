# Init user class to store data.  Better than dictionaries.
class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password
