import requests


class AccessToUsers:

    def get(self, username):
        response = requests.get(f'http://localhost:5000/user/{username}')
        return response

