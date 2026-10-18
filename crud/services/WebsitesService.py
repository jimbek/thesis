# This service communicates with Websites-related CRUD endpoints.
import requests

class WebsitesService:
    def __init__(self):
        self.DOMAIN = "http://localhost:5000"

    # Returns the list of websites.
    def get_all(self) -> list[str]:
        websites = requests.get(f"{self.DOMAIN}/websites").json()
        return websites

    # Retrieves a website by its ID.
    def get_by_id(self, id: str) -> dict:
        response = requests.get(f"{self.DOMAIN}/websites/{id}")
        return response.json()
    # Adds a new website.
    def add(self, data: dict) -> str:
        response = requests.post(f"{self.DOMAIN}/websites", json=data)
        return response.json() if response.status_code >= 400 else "OK"

    # Edit an existing website.
    def edit(self, id: str, data: dict) -> str:
        response = requests.put(f"{self.DOMAIN}/websites/{id}", json=data)
        return response.json() if response.status_code >= 400 else "OK"

    # Deletes an existing website.
    def delete(self, id: str) -> str:
        response = requests.delete(f"{self.DOMAIN}/websites/{id}")
        return response