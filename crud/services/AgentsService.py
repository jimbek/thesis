# This service communicates with AI Agents-related CRUD endpoints.
import requests

class AgentsService:
    def __init__(self):
        self.DOMAIN = "http://127.0.0.1:5000"

    # Returns the list of AI Agents.
    def get_all(self) -> list[str]:
        agents = requests.get(f"{self.DOMAIN}/agents").json()
        return agents

    # Adds a new AI Agent.
    def add(self, data: dict) -> str:
        response = requests.post(f"{self.DOMAIN}/agents", json=data)
        response.raise_for_status()
        return response.json()

    # Edit an existing AI Agent.
    def edit(self, data: dict) -> str:
        response = requests.put(f"{self.DOMAIN}/agents/{data['id']}", json=data)
        response.raise_for_status()
        return response.json()

    # Deletes an existing AI Agent.
    def delete(self, id: str) -> str:
        response = requests.delete(f"{self.DOMAIN}/agents/{id}")
        response.raise_for_status()
        return response.json()