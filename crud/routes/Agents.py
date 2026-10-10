# Describes the routes for the 'Agents' table.
from crud.repos.AgentsRepository import AgentsRepository

from flask import request

# Initialize the AgentsRepository.
repo = AgentsRepository()

# GET /agents - Get all agents.
def get_agents():
    try:
        return repo.get_all(), 200
    except Exception as error:
        return f"Internal server error: {error}", 500

# POST /agents - Create an agent.
def add_agent():
    try:
        data = request.get_json()

        if data is None:
            return "Body is missing", 400
        
        if not data.get("name"):
            return "Invalid parameters", 400
        
        return repo.add(data), 201
    except Exception as error:
        return f"Internal server error: {error}", 500

# PUT /agents/<id> - Update an agent by its ID.
def edit_agent(id):
    try:
        data = request.get_json()

        if data is None:
            return "Body is missing", 400
        
        return repo.edit(id, data), 200
    except Exception as error:
        return f"Internal server error: {error}", 500

# DELETE /agents/<id> - Delete an agent by its ID.
def delete_agent(id):
    try:
        return repo.delete(id), 200
    except Exception as error:
        return f"Internal server error: {error}", 500