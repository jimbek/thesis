# This service communicates with REST APIs-related CRUD endpoints.
import requests

class RestAPIsService:
    def __init__(self):
        self.DOMAIN = "http://localhost:5000"

    # Returns the list of REST APIs.
    def get_all(self) -> list[str]:
        restapis = requests.get(f"{self.DOMAIN}/restapis").json()
        return restapis

    # Retrieves a REST API by its ID.
    def get_by_id(self, id: str) -> dict:
        response = requests.get(f"{self.DOMAIN}/restapis/{id}")
        return response.json()
    # Adds a new REST API.
    def add(self, data: dict) -> str:
        response = requests.post(f"{self.DOMAIN}/restapis", json=data)
        return response.json() if response.status_code >= 400 else "OK"

    # Edit an existing REST API.
    def edit(self, id: str, data: dict) -> str:
        response = requests.put(f"{self.DOMAIN}/restapis/{id}", json=data)
        return response.json() if response.status_code >= 400 else "OK"

    # Deletes an existing REST API.
    def delete(self, id: str) -> str:
        response = requests.delete(f"{self.DOMAIN}/restapis/{id}")
        return response