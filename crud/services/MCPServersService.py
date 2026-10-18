# This service communicates with MCP Servers-related CRUD endpoints.
import requests

class MCPServersService:
    def __init__(self):
        self.DOMAIN = "http://127.0.0.1:5000"

    # Returns the list of MCP Servers.
    def get_all(self) -> list[str]:
        servers = requests.get(f"{self.DOMAIN}/mcpservers").json()
        return servers

    # Adds a new MCP Server.
    def add(self, data: dict) -> str:
        response = requests.post(f"{self.DOMAIN}/mcpservers", json=data)
        response.raise_for_status()
        return response.json()

    # Edit an existing MCP Server.
    def edit(self, data: dict) -> str:
        response = requests.put(f"{self.DOMAIN}/mcpservers/{data['id']}", json=data)
        response.raise_for_status()
        return response.json()

    # Deletes an existing MCP Server.
    def delete(self, id: str) -> str:
        response = requests.delete(f"{self.DOMAIN}/mcpservers/{id}")
        response.raise_for_status()
        return response.json()