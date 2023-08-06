class Credentials:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret


class InvalidCredentialException(Exception):
    def __str__(self):
        return "The credentials parameter you passed is invalid"

