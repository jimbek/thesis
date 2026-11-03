import requests

# Το service αυτό επικοινωνεί με τα endpoints που σχετίζονται με τα Processes.
class ProcessesService:
    def __init__(self):
        self.DOMAIN = "http://api:5000"

    # Επιστρέφει τη λίστα με τα Processes.
    def get_all(self) -> list[str]:
        processes = requests.get(f"{self.DOMAIN}/processes").json()
        return processes

    # Επιστρέφει ένα Process με βάση το ID του.
    def get_by_id(self, id: str) -> dict:
        response = requests.get(f"{self.DOMAIN}/processes/{id}")
        return None if response.status_code == 404 else response.json()

    # Επιστρέφει ένα Process με βάση το ID του AI Agent.
    def get_by_agent_id(self, id: str) -> list[dict]:
        response = requests.get(f"{self.DOMAIN}/processes/agent/{id}").json()
        return response
    
    # Προσθέτει ένα νέο Process.
    def add(self, data: dict) -> str:
        response = requests.post(f"{self.DOMAIN}/processes", json=data)
        return response.json() if response.status_code >= 400 else "OK"

    # Επεξεργάζεται ένα Process.
    def edit(self, id: str, data: dict) -> str:
        response = requests.put(f"{self.DOMAIN}/processes/{id}", json=data)
        return response.json() if response.status_code >= 400 else "OK"

    # Διαγράφει ένα Process.
    def delete(self, id: str) -> str:
        response = requests.delete(f"{self.DOMAIN}/processes/{id}")
        return response

    # Εκτελεί ένα subprocess ενός Process με βάση το PID του.
    def run_process(self, payload: dict) -> str:
        response = requests.post(f"{self.DOMAIN}/processes/execute", json=payload)
        return response.json()

    # Διαγράφει ένα subprocess ενός Process.
    def delete_process(self, pid: int) -> str:
        response = requests.post(f"{self.DOMAIN}/processes/terminate", json={"pid": pid})
        return response.json() if response.status_code >= 400 else "OK"

    # Συνομιλεί με τον AI Agent ενός Process.
    def chat(self, payload: dict) -> str:
        response = requests.post(f"{self.DOMAIN}/processes/chat", json=payload)
        return response.json().get("output", "Δεν έλαβα απάντηση.") if response.status_code == 200 else { "error": f"Σφάλμα: {response.content}" }