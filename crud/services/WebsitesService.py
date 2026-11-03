import requests

# Το service αυτό επικοινωνεί με τα endpoints που σχετίζονται με τα Websites.
class WebsitesService:
    def __init__(self):
        self.DOMAIN = "http://api:5000"

    # Επιστρέφει τη λίστα με τα Websites.
    def get_all(self) -> list[str]:
        websites = requests.get(f"{self.DOMAIN}/websites").json()
        return websites

    # Επιστρέφει ένα Website με βάση το ID του.
    def get_by_id(self, id: str) -> dict:
        response = requests.get(f"{self.DOMAIN}/websites/{id}")
        return response.json()
    
    # Προσθέτει ένα νέο Website.
    def add(self, data: dict) -> str:
        response = requests.post(f"{self.DOMAIN}/websites", json=data)
        return response.json() if response.status_code >= 400 else "OK"

    # Επεξεργάζεται ένα Website.
    def edit(self, id: str, data: dict) -> str:
        response = requests.put(f"{self.DOMAIN}/websites/{id}", json=data)
        return response.json() if response.status_code >= 400 else "OK"

    # Διαγράφει ένα Website.
    def delete(self, id: str) -> str:
        response = requests.delete(f"{self.DOMAIN}/websites/{id}")
        return response