import requests

# Το service αυτό επικοινωνεί με τα endpoints που σχετίζονται με τα REST APIs.
class RestAPIsService:
    def __init__(self):
        self.DOMAIN = "http://api:5000"

    # Επιστρέφει τη λίστα με τα REST APIs.
    def get_all(self) -> list[str]:
        restapis = requests.get(f"{self.DOMAIN}/restapis").json()
        return restapis

    # Επιστρέφει ένα REST API με βάση το ID του.
    def get_by_id(self, id: str) -> dict:
        response = requests.get(f"{self.DOMAIN}/restapis/{id}")
        return response.json()
    
    # Προσθέτει ένα νέο REST API.
    def add(self, data: dict) -> str:
        response = requests.post(f"{self.DOMAIN}/restapis", json=data)
        return response.json() if response.status_code >= 400 else "OK"

    # Επεξεργάζεται ένα REST API.
    def edit(self, id: str, data: dict) -> str:
        response = requests.put(f"{self.DOMAIN}/restapis/{id}", json=data)
        return response.json() if response.status_code >= 400 else "OK"

    # Διαγράφει ένα REST API.
    def delete(self, id: str) -> str:
        response = requests.delete(f"{self.DOMAIN}/restapis/{id}").json()
        return response