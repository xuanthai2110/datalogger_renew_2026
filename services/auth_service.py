import requests
from config import API_BASE_URL, API_USERNAME, API_PASSWORD

class AuthService:
    def login(self):
        url = f"{API_BASE_URL}/api/auth/login"
        response = requests.post(url, json={
            "username": API_USERNAME,
            "password": API_PASSWORD
        })
        return response.json().get("access_token")