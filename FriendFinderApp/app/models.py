class User:
    def __init__(self, username, password, name, email):
        self.username = username
        self.password = password
        self.name = name
        self.email = email

class Friend:
    def __init__(self, user_id, friend_id):
        self.user_id = user_id
        self.friend_id = friend_id