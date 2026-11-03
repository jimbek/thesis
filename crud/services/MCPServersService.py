import requests

# Το service αυτό επικοινωνεί με τα endpoints που σχετίζονται με τους MCP Servers.
class MCPServersService:
    def __init__(self):
        self.DOMAIN = "http://api:5000"

    # Επιστρέφει τη λίστα με τους MCP Servers.
    def get_all(self) -> list[str]:
        mcp_servers = requests.get(f"{self.DOMAIN}/mcpservers").json()
        return mcp_servers

    # Επιστρέφει έναν MCP Server με βάση το ID του.
    def get_by_id(self, id: str) -> dict:
        response = requests.get(f"{self.DOMAIN}/mcpservers/{id}")
        return response.json()
    
    # Προσθέτει έναν νέο MCP Server.
    def add(self, data: dict) -> str:
        response = requests.post(f"{self.DOMAIN}/mcpservers", json=data)
        return response.json() if response.status_code >= 400 else "OK"

    # Επεξεργάζεται έναν MCP Server.
    def edit(self, id: str, data: dict) -> str:
        response = requests.put(f"{self.DOMAIN}/mcpservers/{id}", json=data)
        return response.json() if response.status_code >= 400 else "OK"

    # Διαγράφει έναν MCP Server.
    def delete(self, id: str) -> str:
        response = requests.delete(f"{self.DOMAIN}/mcpservers/{id}")
        return response