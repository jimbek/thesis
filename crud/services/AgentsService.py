import requests

# Το service αυτό επικοινωνεί με τα endpoints που σχετίζονται με τους AI Agents.
class AgentsService:
    def __init__(self):
        self.DOMAIN = "http://api:5000"

    # Επιστρέφει τη λίστα με τους AI Agents.
    def get_all(self) -> list[str]:
        agents = requests.get(f"{self.DOMAIN}/agents").json()
        return agents

    # Επιστρέφει έναν AI Agent με βάση το ID του.
    def get_by_agent_id(self, id: str) -> dict:
        response = requests.get(f"{self.DOMAIN}/agents/{id}")
        return response.json()
    
    # Προσθέτει έναν νέο AI Agent.
    def add(self, data: dict) -> str:
        response = requests.post(f"{self.DOMAIN}/agents", json=data)
        return response.json() if response.status_code >= 400 else "OK"

    # Επεξεργάζεται έναν AI Agent.
    def edit(self, id: str, data: dict) -> str:
        response = requests.put(f"{self.DOMAIN}/agents/{id}", json=data)
        return response.json() if response.status_code >= 400 else "OK"

    # Διαγράφει έναν AI Agent.
    def delete(self, id: str) -> str:
        response = requests.delete(f"{self.DOMAIN}/agents/{id}")
        return response