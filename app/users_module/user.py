from random_username.generate import generate_username


class User():
    def __init__(self, id):
        self.id = id
        self.name = generate_username(1)