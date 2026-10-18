# This service communicates with REST APIs-related CRUD endpoints.
import requests

class RestAPIsService:
    def __init__(self):
        self.DOMAIN = "http://127.0.0.1:5000"

    # Returns the list of REST APIs.
    def get_all(self) -> list[str]:
        websites = requests.get(f"{self.DOMAIN}/restapis").json()
        return websites

    # Adds a new REST API.
    def add(self, data: dict) -> str:
        response = requests.post(f"{self.DOMAIN}/restapis", json=data)
        response.raise_for_status()
        return response.json()

    # Edit an existing REST API.
    def edit(self, data: dict) -> str:
        response = requests.put(f"{self.DOMAIN}/restapis/{data['id']}", json=data)
        response.raise_for_status()
        return response.json()

    # Deletes an existing REST API.
    def delete(self, id: str) -> str:
        response = requests.delete(f"{self.DOMAIN}/restapis/{id}")
        response.raise_for_status()
        return response.json()