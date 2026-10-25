# This service communicates with AI Agents-related CRUD endpoints.
import requests

class AgentsService:
    def __init__(self):
        self.DOMAIN = "http://api:5000"

    # Returns the list of AI Agents.
    def get_all(self) -> list[str]:
        agents = requests.get(f"{self.DOMAIN}/agents").json()
        return agents

    # Retrieves an AI Agent by its ID.
    def get_by_agent_id(self, id: str) -> dict:
        response = requests.get(f"{self.DOMAIN}/agents/{id}")
        return response.json()
    # Adds a new AI Agent.
    def add(self, data: dict) -> str:
        response = requests.post(f"{self.DOMAIN}/agents", json=data)
        return response.json() if response.status_code >= 400 else "OK"

    # Edit an existing AI Agent.
    def edit(self, id: str, data: dict) -> str:
        response = requests.put(f"{self.DOMAIN}/agents/{id}", json=data)
        return response.json() if response.status_code >= 400 else "OK"

    # Deletes an existing AI Agent.
    def delete(self, id: str) -> str:
        response = requests.delete(f"{self.DOMAIN}/agents/{id}")
        return response