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
        return {'error': f"Internal server error: {error}"}, 500

# GET /mcpservers/<id> - Get an MCP server by its ID.
def get_mcpserver_by_id(id):
    try:
        result = repo.get_by_id(id)

        if result is None:
            return {'error': 'Δεν υπάρχει MCP Server με αυτό το ID.'}, 404

        return result, 200
    except Exception as error:
        return {'error': f"Internal server error: {error}"}, 500

# POST /mcpservers - Create an MCP server.
def add_mcpserver():
    try:
        data = request.get_json()
        result = repo.add(data)

        if isinstance(result, dict) and "error" in result:
            return result, 400
        
        return result, 201
    except Exception as error:
        return {'error': f"Internal server error: {error}"}, 500

# PUT /mcpservers/<id> - Update an MCP server by its ID.
def edit_mcpserver(id):
    try:
        data = request.get_json()
        result = repo.edit(id, data)

        if isinstance(result, dict) and "error" in result:
            return result, 400
        
        return result, 200
    except Exception as error:
        return {'error': f"Internal server error: {error}"}, 500

# DELETE /mcpservers/<id> - Delete an MCP server by its ID.
def delete_mcpserver(id):
    try:
        result = repo.delete(id)
                
        if isinstance(result, dict) and "error" in result:
            return result, 400

        return result, 200
    except Exception as error:
        return {'error': f"Internal server error: {error}"}, 500