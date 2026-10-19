# This service communicates with MCP Servers-related CRUD endpoints.
import requests

class MCPServersService:
    def __init__(self):
        self.DOMAIN = "http://api:5000"

    # Returns the list of MCP servers.
    def get_all(self) -> list[str]:
        mcp_servers = requests.get(f"{self.DOMAIN}/mcpservers").json()
        return mcp_servers

    # Retrieves an MCP server by its ID.
    def get_by_id(self, id: str) -> dict:
        response = requests.get(f"{self.DOMAIN}/mcpservers/{id}")
        return response.json()
    # Adds a new MCP server.
    def add(self, data: dict) -> str:
        response = requests.post(f"{self.DOMAIN}/mcpservers", json=data)
        return response.json() if response.status_code >= 400 else "OK"

    # Edit an existing MCP server.
    def edit(self, id: str, data: dict) -> str:
        response = requests.put(f"{self.DOMAIN}/mcpservers/{id}", json=data)
        return response.json() if response.status_code >= 400 else "OK"

    # Deletes an existing MCP server.
    def delete(self, id: str) -> str:
        response = requests.delete(f"{self.DOMAIN}/mcpservers/{id}")
        return response