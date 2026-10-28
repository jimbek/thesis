# This service communicates with Processes-related CRUD endpoints.
import requests

class ProcessesService:
    def __init__(self):
        self.DOMAIN = "http://api:5000"

    # Returns the list of Processes.
    def get_all(self) -> list[str]:
        processes = requests.get(f"{self.DOMAIN}/processes").json()
        return processes

    # Retrieves a Process by its ID.
    def get_by_id(self, id: str) -> dict:
        response = requests.get(f"{self.DOMAIN}/processes/{id}")
        return None if response.status_code == 404 else response.json()

    # Retrieves a Process by its AI Agent ID.
    def get_by_agent_id(self, id: str) -> list[dict]:
        response = requests.get(f"{self.DOMAIN}/processes/agent/{id}").json()
        return response
    
    # Adds a new Process.
    def add(self, data: dict) -> str:
        response = requests.post(f"{self.DOMAIN}/processes", json=data)
        return response.json() if response.status_code >= 400 else "OK"

    # Edit an existing Process.
    def edit(self, id: str, data: dict) -> str:
        response = requests.put(f"{self.DOMAIN}/processes/{id}", json=data)
        return response.json() if response.status_code >= 400 else "OK"

    # Deletes an existing Process.
    def delete(self, id: str) -> str:
        response = requests.delete(f"{self.DOMAIN}/processes/{id}")
        return response

    # Runs the subprocess of a Process.
    def run_process(self, process: dict, agent_name: str) -> str:
        pass

    # Deletes the subprocess of a Process.
    def delete_process(self, process: dict) -> str:
        pass