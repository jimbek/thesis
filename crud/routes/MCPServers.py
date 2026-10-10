# Defines the routes for the 'MCPServers' table.
from crud.repos.MCPServersRepository import MCPServersRepository

from flask import request

# Initialize the MCPServersRepository.
repo = MCPServersRepository()

# GET /mcpservers - Get all MCP servers.
def get_mcpservers():
    try:
        return repo.get_all(), 200
    except Exception as error:
        return f"Internal server error: {error}", 500

# POST /mcpservers - Create an MCP server.
def add_mcpserver():
    try:
        data = request.get_json()

        if data is None:
            return "Body is missing", 400
        
        if not data.get("name"):
            return "Invalid parameters", 400
        
        return repo.add(data), 201
    except Exception as error:
        return f"Internal server error: {error}", 500

# PUT /mcpservers/<id> - Update an MCP server by its ID.
def edit_mcpserver(id):
    try:
        data = request.get_json()

        if data is None:
            return "Body is missing", 400
        
        return repo.edit(id, data), 200
    except Exception as error:
        return f"Internal server error: {error}", 500

# DELETE /mcpservers/<id> - Delete an MCP server by its ID.
def delete_mcpserver(id):
    try:
        return repo.delete(id), 200
    except Exception as error:
        return f"Internal server error: {error}", 500